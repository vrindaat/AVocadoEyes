"""Ordered registered steps with explicit references and revision provenance."""
import copy
import hashlib
import json
import time
import uuid

from . import contracts
from .inference import LocalChat, parse_response
from .video import sample

REGISTRY = {}


def register(kind):
    """Register fn(run, step, resolved_inputs, attempt) -> JSON-compatible output."""
    def decorate(fn):
        if kind in REGISTRY:
            raise ValueError(f"Step kind already registered: {kind}")
        REGISTRY[kind] = fn
        return fn
    return decorate


def default_config():
    config = json.loads((contracts.ROOT / "config/pipeline.example.json").read_text())
    for step in config["steps"]:
        if step.get("prompt", "").startswith("@"):
            step["prompt"] = (contracts.ROOT / step["prompt"][1:]).read_text()
    return config


def brief(value):
    """Keep exact image bytes separately as frames; don't repeat them in JSON UI."""
    if isinstance(value, bytes):
        return {"bytes": len(value), "sha256": hashlib.sha256(value).hexdigest()}
    if isinstance(value, str) and value.startswith("data:image/"):
        return {"image_sha256": hashlib.sha256(value.encode()).hexdigest()}
    if isinstance(value, list):
        return [brief(v) for v in value]
    if isinstance(value, dict):
        result = {}
        for key, item in value.items():
            if key == "images" and isinstance(item, list) and all(isinstance(s, str) for s in item):
                result[key] = [{"image_sha256": hashlib.sha256(s.encode()).hexdigest()} for s in item]
            else:
                result[key] = brief(item)
        return result
    return value


class Run:
    def __init__(self, adapter=None):
        self.id = str(uuid.uuid4())
        self.adapter = adapter or LocalChat()
        self.config = default_config()
        self.context = {"personality_preferences": "", "goals": "", "current_state": "", "energy_budget": ""}
        self.rubric = ("Hypothesis rubric: distinguish visible engagement/orientation, reciprocal interaction and group context "
                       "from personality and outcome estimates. Explain alternative interpretations. Match explicit attendee "
                       "preferences/goals; assess enjoyment/connection separately from effort/fatigue. No fixed weights. "
                       "Motivation: docs/research/agent-design-and-validation.md and social-fatigue-and-energy.md; "
                       "these sources do not validate individual predictions. Trait-mediated reasoning is optional (off by default).")
        self.video = b""
        self.filename = ""
        self.results = {}
        self.histories = {}
        self.validate_config(self.config)

    @staticmethod
    def validate_config(config):
        contracts.validate(config, "config")
        seen = {"video", "context", "rubric"}
        for step in config["steps"]:
            if step["id"] in seen or step["kind"] not in REGISTRY:
                raise ValueError("Step IDs must be unique; kind must be registered")
            for reference in step["inputs"].values():
                root = reference[1:].split(".")[0]
                if root not in seen:
                    raise ValueError(f"{step['id']}: input must reference an earlier step or external input")
                if step["kind"] == "observe" and root in ("context", "rubric"):
                    raise ValueError("Observation must remain independent of attendee context/rubric")
            if step["kind"] in ("observe", "rank", "model"):
                if step.get("model") not in config["models"] or not step.get("prompt"):
                    raise ValueError("Model steps require a configured model alias and prompt")
            seen.add(step["id"])

    def invalidate(self, index):
        for step in self.config["steps"][index:]:
            if step["id"] in self.results:
                self.results[step["id"]]["status"] = "stale"

    def configure(self, config, context, rubric):
        self.validate_config(config)
        old_steps = self.config["steps"]
        changes = []
        for i, step in enumerate(config["steps"]):
            if i >= len(old_steps) or step != old_steps[i]:
                changes.append(i)
            if step.get("model") and self.config["models"].get(step["model"]) != config["models"].get(step["model"]):
                changes.append(i)
            roots = {ref[1:].split(".")[0] for ref in step["inputs"].values()}
            if (context != self.context and "context" in roots) or (rubric != self.rubric and "rubric" in roots):
                changes.append(i)
        self.config = copy.deepcopy(config)
        self.context, self.rubric = copy.deepcopy(context), str(rubric)
        if changes:
            self.invalidate(min(changes))
        active = {s["id"] for s in config["steps"]}
        for sid in set(self.results) - active:
            self.results[sid]["status"] = "removed"

    def upload(self, video, filename):
        if not video or len(video) > 64 * 1024 * 1024:
            raise ValueError("Clip must be 1 byte to 64 MiB")
        # A new video starts a new run; history containing the previous scene is deleted.
        self.video, self.filename = video, filename
        self.id = str(uuid.uuid4())
        self.results, self.histories = {}, {}

    def resolve(self, reference):
        root, *path = reference[1:].split(".")
        if root in ("video", "context", "rubric"):
            value = getattr(self, root)
            revision = hashlib.sha256((value if isinstance(value, bytes) else json.dumps(value).encode())).hexdigest()
        else:
            result = self.results.get(root, {})
            if result.get("status") != "current":
                raise ValueError(f"Input {root} is missing, stale or failed; run its step first")
            value, revision = result["output"], result["revision"]
        for field in path:
            value = value[field]
        return copy.deepcopy(value), revision

    def execute(self, step_id, mode="step"):
        ids = [s["id"] for s in self.config["steps"]]
        if mode not in ("step", "from", "all"):
            raise ValueError("Unknown execution mode")
        start = 0 if mode == "all" else ids.index(step_id)
        stop = start + 1 if mode == "step" else len(ids)
        for step in self.config["steps"][start:stop]:
            index = ids.index(step["id"])
            self.invalidate(index)
            attempt = {"revision": str(uuid.uuid4()), "source": "execution", "step": copy.deepcopy(step),
                       "model": self.config["models"].get(step.get("model")), "lineage": {}, "status": "error"}
            begin = time.perf_counter()
            try:
                inputs = {}
                for name, reference in step["inputs"].items():
                    inputs[name], attempt["lineage"][reference] = self.resolve(reference)
                attempt["human_assisted"] = any(self.results.get(ref[1:].split(".")[0], {}).get("human_assisted", False)
                                                for ref in step["inputs"].values())
                attempt["inputs"] = copy.deepcopy(inputs)
                attempt["output"] = REGISTRY[step["kind"]](self, step, inputs, attempt)
                attempt["status"] = "current"
            except Exception as exc:
                attempt["error"] = str(exc)
            attempt["elapsed_s"] = round(time.perf_counter() - begin, 4)
            self.histories.setdefault(step["id"], []).append(copy.deepcopy(attempt))
            self.results[step["id"]] = attempt
            if attempt["status"] == "error":
                return False
        return True

    def correct(self, sid, output):
        step = next(s for s in self.config["steps"] if s["id"] == sid)
        current = self.results.get(sid, {})
        if current.get("status") != "current":
            raise ValueError("Only a current output can be corrected; rerun stale steps first")
        inputs = {name: self.resolve(ref)[0] for name, ref in step["inputs"].items()}
        if step["kind"] == "observe":
            contracts.observations(output, inputs["frames"])
        elif step["kind"] == "validate":
            contracts.observations(output, inputs["frames"])
        elif step["kind"] == "rank":
            contracts.ranking(output, inputs["observations"])
        elif step["kind"] == "sample":
            raise ValueError("Edit sampling settings and rerun instead of correcting frame bytes")
        revision = {"revision": str(uuid.uuid4()), "source": "human", "parent_revision": current["revision"],
                    "status": "current", "output": copy.deepcopy(output), "lineage": copy.deepcopy(current["lineage"]), "elapsed_s": 0,
                    "human_assisted": True}
        self.invalidate([s["id"] for s in self.config["steps"]].index(sid) + 1)
        self.results[sid] = revision
        self.histories[sid].append(copy.deepcopy(revision))

    def snapshot(self):
        frames = []
        for step in self.config["steps"]:
            result = self.results.get(step["id"], {})
            if step["kind"] == "sample" and result.get("status") == "current":
                frames = result["output"]["frames"]
        return {"run_id": self.id, "config": self.config, "context": self.context, "rubric": self.rubric,
                "filename": self.filename, "results": brief(self.results), "history": brief(self.histories),
                "frames": frames, "kinds": sorted(REGISTRY), "route": getattr(self.adapter, "base_url", "test adapter")}


@register("sample")
def sample_step(run, step, inputs, attempt):
    return sample(inputs["video"], step["settings"])


def model_step(run, step, inputs, attempt, frames=None):
    model = run.config["models"][step["model"]]
    if model == "SET_LOCAL_MODEL":
        raise ValueError("Set the model alias to an installed local model in configuration")
    text_inputs = {**inputs, "additional_inputs": step.get("extra", {})}
    if frames is not None:
        text_inputs["frames"] = [{k: v for k, v in f.items() if k != "image"} for f in frames]
    settings = copy.deepcopy(step["settings"])
    prompt = step["prompt"]
    definition = {"observe": "observation", "rank": "ranking"}.get(step["kind"])
    if definition:
        schema = contracts.output_schema(definition)
        prompt += "\n\nRequired output JSON schema:\n" + json.dumps(schema)
        if settings.get("format", "json") == "json":
            settings["format"] = schema
    attempt["effective_prompt"], attempt["effective_settings"] = prompt, settings
    response = run.adapter.complete(model, prompt, text_inputs, settings, frames)
    attempt.update(response)  # Preserve exact envelope, including backend explanation fields.
    if response.get("http_status", 200) >= 400:
        raise ValueError(f"Local inference returned HTTP {response['http_status']}; inspect the original response")
    attempt["parsed"] = parse_response(response["raw"])
    return attempt["parsed"]


@register("observe")
def observe_step(run, step, inputs, attempt):
    frames = inputs["frames"]
    output = model_step(run, step, inputs, attempt, frames)
    return contracts.observations(output, frames)


@register("validate")
def validate_step(run, step, inputs, attempt):
    return contracts.observations(inputs["observations"], inputs["frames"])


@register("rank")
def rank_step(run, step, inputs, attempt):
    observation = inputs["observations"]
    frames = []
    for source in run.config["steps"]:
        result = run.results.get(source["id"], {})
        if source["kind"] == "sample" and result.get("status") == "current":
            frames.extend(result["output"]["frames"])
    contracts.observations(observation, frames)
    eligible = [p for p in observation["people"] if not p["identity_uncertain"] and
                any(e["visibility"] != "unobservable" for e in p["evidence"])]
    context = inputs.get("context", {})
    if not eligible or not isinstance(context, dict) or not any(context.get(k) for k in ("goals", "personality_preferences")):
        return {"status": "insufficient_evidence", "candidates": [],
                "unknowns": ["Need identifiable people with usable evidence and explicit attendee goals/preferences."]}
    # A custom mapping cannot bypass the scene contract.
    for person in observation["people"]:
        if "identity_uncertain" not in person:
            raise ValueError("Rank requires validated observations")
    return contracts.ranking(model_step(run, step, inputs, attempt), observation)


@register("model")
def generic_model_step(run, step, inputs, attempt):
    """Optional JSON processing step; map frames to include images."""
    return model_step(run, step, inputs, attempt, inputs.get("frames"))


@register("passthrough")
def passthrough_step(run, step, inputs, attempt):
    """Small extension example: map value=$validate then rank from this step."""
    return inputs["value"]
