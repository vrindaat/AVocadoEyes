"""Two editable calls: native video to JSON, then JSON to text reasoning."""
import copy
import json
import os

from jsonschema import Draft202012Validator

from .inference import LocalChat, response_parts
from .native_video import NativeVideo


def defaults():
    return {"version": 2, "video": {
        "model": os.environ.get("AVOCADO_VIDEO_MODEL", "models/Qwen3-VL-8B-Instruct"),
        "prompt": "Describe each visible person's stance, clothing, hand gestures, gaze, smile, facial expression, and movements such as nodding. Describe changes over time with timestamps where possible. Distinguish visible observations from uncertain interpretations. Do not invent details or infer personality as fact.",
        "schema": {"type": "object", "properties": {
            "people": {"type": "array", "items": {"type": "object", "properties": {
                "id": {"type": "string"}, "observations": {"type": "array", "items": {"type": "string"}},
                "uncertainty": {"type": "string"}}, "required": ["id", "observations", "uncertainty"]}},
            "unknowns": {"type": "array", "items": {"type": "string"}}}, "required": ["people", "unknowns"]},
        "settings": {"max_frames": 256, "max_pixels": 262144, "max_new_tokens": 2048}},
        "reason": {"model": "qwen3.5:9b", "prompt": "Analyze the supplied video observations. Explain the visible interaction patterns, what the evidence supports, and what remains uncertain. Do not treat observations as proof of personality or intent.",
                   "settings": {"think": True, "num_predict": 4096, "temperature": 0.2}}}


def validate_config(config):
    if not isinstance(config, dict) or set(config) != {"version", "video", "reason"} or config["version"] != 2:
        raise ValueError("Expected a version 2 video/reason configuration")
    for key in ("video", "reason"):
        stage = config[key]
        required = {"model", "prompt", "settings"} | ({"schema"} if key == "video" else set())
        if not isinstance(stage, dict) or set(stage) != required:
            raise ValueError(f"Invalid {key} configuration fields")
        for field in ("model", "prompt"):
            if not isinstance(stage[field], str) or not stage[field].strip():
                raise ValueError(f"{key} {field} must not be empty")
    schema = config["video"]["schema"]
    Draft202012Validator.check_schema(schema)
    def local_refs(value):
        if isinstance(value, dict):
            for key, item in value.items():
                if key in ("$ref", "$dynamicRef") and (not isinstance(item, str) or not item.startswith("#")):
                    raise ValueError("Use only internal JSON Schema references; remote schemas are disabled")
                local_refs(item)
        elif isinstance(value, list):
            for item in value:
                local_refs(item)
    local_refs(schema)
    limits = {"max_frames": (2, 4096), "max_pixels": (131072, 1048576), "max_new_tokens": (64, 8192)}
    settings = config["video"]["settings"]
    if not isinstance(settings, dict) or set(settings) != set(limits):
        raise ValueError("Invalid video settings")
    for key, (low, high) in limits.items():
        if type(settings[key]) is not int or not low <= settings[key] <= high:
            raise ValueError(f"{key} must be an integer between {low} and {high}")
    settings = config["reason"]["settings"]
    if not isinstance(settings, dict) or set(settings) != {"think", "num_predict", "temperature"}:
        raise ValueError("Invalid reasoning settings")
    if type(settings["think"]) is not bool or type(settings["num_predict"]) is not int or not 64 <= settings["num_predict"] <= 16384:
        raise ValueError("Reasoning requires boolean think and num_predict between 64 and 16384")
    if type(settings["temperature"]) not in (int, float) or not 0 <= settings["temperature"] <= 2:
        raise ValueError("Temperature must be between 0 and 2")


class TwoStage:
    def __init__(self, adapter=None, video_adapter=None):
        self.adapter = adapter or LocalChat()
        self.video_adapter = video_adapter or NativeVideo()
        self.config = defaults()
        self.video = None
        self.filename = ""
        self.results = {}

    def fresh(self):
        return TwoStage(self.adapter, self.video_adapter)

    def configure(self, config, *_):
        validate_config(config)
        if config["video"] != self.config["video"]:
            self.invalidate("video")
        elif config["reason"] != self.config["reason"]:
            self.invalidate("reason")
        self.config = copy.deepcopy(config)

    def invalidate(self, step):
        for key in (("video", "reason") if step == "video" else ("reason",)):
            if key in self.results:
                self.results[key]["status"] = "stale"

    def upload(self, video, filename):
        if not video or len(video) > 64 * 1024 * 1024:
            raise ValueError("Choose a nonempty video up to 64 MiB")
        self.video, self.filename, self.results = video, filename, {}

    def execute(self, step="", mode="step"):
        if mode not in ("all", "step") or (mode == "step" and step not in ("video", "reason")):
            raise ValueError("Choose video, reason, or run both")
        for key in (("video", "reason") if mode == "all" else (step,)):
            self.invalidate(key)
            result = self.results[key] = {"status": "running", "output": ""}
            try:
                stage = self.config[key]
                if key == "video":
                    if not self.video:
                        raise ValueError("Upload a video first")
                    prompt = stage["prompt"] + "\n\nReturn ONLY JSON matching this JSON Schema:\n" + json.dumps(stage["schema"])
                    content = self.video_adapter.complete(self.video, stage["model"], prompt, stage["settings"])
                    result["output"] = content
                    text = content.strip()
                    if text.startswith("```") and text.endswith("```"):
                        text = text.split("\n", 1)[1].rsplit("```", 1)[0]
                    parsed = json.loads(text, parse_constant=lambda value: (_ for _ in ()).throw(ValueError(f"Invalid JSON constant {value}")))
                    Draft202012Validator(stage["schema"]).validate(parsed)
                    result["json"] = parsed
                else:
                    source = self.results.get("video", {})
                    if source.get("status") != "current":
                        raise ValueError("Run the video model successfully with the current prompt/schema first")
                    response = self.adapter.complete(stage["model"], stage["prompt"], source["json"],
                                                     {**stage["settings"], "format": None})
                    if response.get("http_status", 200) != 200:
                        raise ValueError(f"Local reasoning model returned HTTP {response['http_status']}")
                    parts = response_parts(response["raw"])
                    result.update(output=parts["content"], reasoning=parts["reasoning"])
                    if not isinstance(result["output"], str) or not result["output"].strip():
                        raise ValueError("No final answer returned; increase the token budget or disable thinking")
                result["status"] = "current"
            except Exception as exc:
                result.update(status="error", error=str(exc)[:500])
                return False
        return True

    def snapshot(self):
        return copy.deepcopy({"mode": "two-stage", "config": self.config, "filename": self.filename,
                              "results": self.results, "has_video": self.video is not None})
