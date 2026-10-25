import copy
import json
import subprocess
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

import imageio_ffmpeg

from avocadoeyes import contracts
from avocadoeyes.inference import LocalChat
from avocadoeyes.runner import Run, default_config
from avocadoeyes.server import make_server
from avocadoeyes.video import sample

FRAMES = [{"id": "f000", "timestamp_s": 0.0, "image": "data:image/jpeg;base64,ZmFrZQ=="}]
OBS = {"people": [{"id": "p1", "identity_uncertain": False,
                   "locations": [{"frame_id": "f000", "box": [0.1, 0.1, 0.3, 0.6]}],
                   "evidence": [{"id": "e1", "frame_id": "f000", "cue": "Body oriented toward group",
                                 "visibility": "present", "alternatives": ["Passing through"]}]}], "unknowns": ["Speech inaudible"]}
RANK = {"status": "ok", "candidates": [{"person_id": "p1", "preference_index": 63,
        "connection": "May fit the goal", "effort": "Unknown", "reason": "Visible group orientation",
        "evidence_ids": ["e1"], "uncertainty": "Sparse frames"}], "unknowns": ["Actual enjoyment unmeasured"]}


class FakeAdapter:
    base_url = "http://127.0.0.1/test"

    def __init__(self):
        self.calls = []
        self.bad = False

    def complete(self, model, prompt, inputs, settings, frames=None):
        self.calls.append(copy.deepcopy({"model": model, "prompt": prompt, "inputs": inputs, "settings": settings, "frames": frames}))
        content = "not JSON" if self.bad else json.dumps(OBS if frames else RANK)
        return {"raw": json.dumps({"model": model, "choices": [{"message": {"content": content, "reasoning": "Backend explanation"}}]})}


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.adapter = FakeAdapter()
        self.run = Run(self.adapter)
        config = default_config()
        config["models"] = {"vision": "local-test", "reasoning": "local-test"}
        self.run.configure(config, {"goals": "Find a small group"}, self.run.rubric)
        self.run.upload(b"synthetic", "test.mp4")
        self.patcher = patch("avocadoeyes.runner.sample", return_value={"frames": FRAMES})
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def execute(self):
        self.assertTrue(self.run.execute("", "all"), self.run.snapshot())

    def test_complete_pipeline_and_exact_inspection(self):
        self.execute()
        self.assertEqual(self.run.results["rank"]["output"], RANK)
        self.assertEqual(len(self.adapter.calls), 2)
        self.assertNotIn("context", self.adapter.calls[0]["inputs"])
        self.assertEqual(self.adapter.calls[0]["frames"], FRAMES)
        self.assertIn("Backend explanation", self.run.results["observe"]["raw"])
        self.assertIn("elapsed_s", self.run.results["rank"])
        self.assertEqual(self.run.snapshot()["frames"], FRAMES)

    def test_preferences_reuse_frozen_observations(self):
        self.execute()
        revision = self.run.results["observe"]["revision"]
        self.run.configure(self.run.config, {"goals": "Quiet conversation"}, self.run.rubric)
        self.assertEqual(self.run.results["rank"]["status"], "stale")
        self.assertEqual(self.run.results["observe"]["status"], "current")
        self.assertTrue(self.run.execute("rank"))
        self.assertEqual(self.run.results["observe"]["revision"], revision)
        self.assertEqual(len(self.adapter.calls), 3)

    def test_correction_preserves_original_and_propagates_lineage(self):
        self.execute()
        original = copy.deepcopy(self.run.histories["observe"][0])
        correction = copy.deepcopy(OBS)
        correction["people"][0]["evidence"][0]["cue"] = "Human correction"
        self.run.correct("observe", correction)
        human = self.run.results["observe"]["revision"]
        self.assertEqual(self.run.histories["observe"][0], original)
        self.assertEqual(self.run.results["rank"]["status"], "stale")
        self.assertTrue(self.run.execute("validate", "from"))
        self.assertEqual(self.run.results["validate"]["lineage"]["$observe"], human)
        self.assertTrue(self.run.results["rank"]["human_assisted"])

    def test_prompt_model_and_sampling_changes_invalidate_suffix(self):
        for target, change in [(1, "prompt"), (0, "settings"), (1, "model")]:
            self.execute()
            config = copy.deepcopy(self.run.config)
            if change == "prompt":
                config["steps"][target]["prompt"] += "\nMore uncertainty."
            elif change == "model":
                config["models"]["vision"] = "other-local-model"
            else:
                config["steps"][target]["settings"]["count"] = 4
            self.run.configure(config, self.run.context, self.run.rubric)
            for step in config["steps"][target:]:
                self.assertEqual(self.run.results[step["id"]]["status"], "stale")

    def test_failed_rerun_retains_raw_and_stales_rank(self):
        self.execute()
        self.adapter.bad = True
        self.assertFalse(self.run.execute("observe", "from"))
        self.assertIn("not JSON", self.run.results["observe"]["raw"])
        self.assertEqual(self.run.results["observe"]["status"], "error")
        self.assertEqual(self.run.results["rank"]["status"], "stale")
        self.assertEqual(len(self.run.histories["rank"]), 1)

    def test_stale_input_cannot_run_or_be_corrected(self):
        self.execute()
        self.run.invalidate(1)
        with self.assertRaises(ValueError):
            self.run.correct("observe", OBS)
        self.assertFalse(self.run.execute("rank"))
        self.assertIn("stale", self.run.results["rank"]["error"])

    def test_insert_step_and_remap_input(self):
        config = copy.deepcopy(self.run.config)
        config["steps"].insert(3, {"id": "review", "kind": "passthrough", "inputs": {"value": "$validate"}, "settings": {}})
        config["steps"][4]["inputs"]["observations"] = "$review"
        self.run.configure(config, self.run.context, self.run.rubric)
        self.execute()
        self.assertEqual(self.run.results["review"]["output"], OBS)

    def test_configuration_rejects_forward_reference_and_context_leak(self):
        config = copy.deepcopy(self.run.config)
        config["steps"][1]["inputs"]["attendee"] = "$context"
        with self.assertRaises(ValueError):
            self.run.configure(config, {}, "")
        config["steps"][1]["inputs"]["attendee"] = "$rank"
        with self.assertRaises(ValueError):
            self.run.configure(config, {}, "")

    def test_weak_ambiguous_and_missing_context_abstain(self):
        self.execute()
        weak = copy.deepcopy(OBS)
        weak["people"][0]["identity_uncertain"] = True
        self.run.correct("observe", weak)
        self.assertTrue(self.run.execute("validate", "from"))
        self.assertEqual(self.run.results["rank"]["output"]["status"], "insufficient_evidence")
        self.assertEqual(len(self.adapter.calls), 2)
        self.run.correct("observe", {"people": [], "unknowns": ["Occluded"]})
        self.assertTrue(self.run.execute("validate", "from"))
        self.assertEqual(self.run.results["rank"]["output"]["candidates"], [])
        self.run.configure(self.run.config, {}, self.run.rubric)
        self.assertTrue(self.run.execute("rank"))
        self.assertEqual(self.run.results["rank"]["output"]["status"], "insufficient_evidence")

    def test_new_clip_clears_old_scene(self):
        self.execute()
        old_id = self.run.id
        self.run.upload(b"new clip", "new.mp4")
        self.assertNotEqual(self.run.id, old_id)
        self.assertEqual(self.run.histories, {})


class ContractTests(unittest.TestCase):
    def test_schemas_and_examples(self):
        from jsonschema import Draft202012Validator
        for file in (contracts.ROOT / "docs/contracts").glob("workbench-*.schema.json"):
            Draft202012Validator.check_schema(json.loads(file.read_text()))
        contracts.validate(default_config(), "config")
        contracts.observations(OBS, FRAMES)
        contracts.ranking(RANK, OBS)

    def test_observation_rejects_bad_scene_references(self):
        for change in ("frame", "box", "duplicate", "evidence"):
            obs = copy.deepcopy(OBS)
            person = obs["people"][0]
            if change == "frame":
                person["locations"][0]["frame_id"] = "missing"
            elif change == "box":
                person["locations"][0]["box"] = [0.9, 0.1, 0.3, 0.6]
            elif change == "duplicate":
                obs["people"].append(copy.deepcopy(person))
            else:
                person["evidence"][0]["frame_id"] = "missing"
            with self.subTest(change=change), self.assertRaises(ValueError):
                contracts.observations(obs, FRAMES)

    def test_ranking_rejects_invented_ambiguous_unobservable_and_duplicate(self):
        for change in ("id", "evidence", "ambiguous", "unobservable", "duplicate", "status"):
            ranking, observation = copy.deepcopy(RANK), copy.deepcopy(OBS)
            if change == "id": ranking["candidates"][0]["person_id"] = "invented"
            if change == "evidence": ranking["candidates"][0]["evidence_ids"] = ["invented"]
            if change == "ambiguous": observation["people"][0]["identity_uncertain"] = True
            if change == "unobservable": observation["people"][0]["evidence"][0]["visibility"] = "unobservable"
            if change == "duplicate": ranking["candidates"].append(copy.deepcopy(ranking["candidates"][0]))
            if change == "status": ranking["status"] = "insufficient_evidence"
            with self.subTest(change=change), self.assertRaises(ValueError): contracts.ranking(ranking, observation)


class VideoTests(unittest.TestCase):
    def test_real_decode_has_ordered_source_timestamps(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "synthetic.mp4"
            subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-hide_banner", "-loglevel", "error", "-f", "lavfi", "-i", "testsrc=size=320x240:rate=10", "-t", "2", "-pix_fmt", "yuv420p", str(path)], check=True, capture_output=True)
            frames = sample(path.read_bytes(), {"count": 4, "seconds": 2})["frames"]
        self.assertEqual(len(frames), 4)
        self.assertEqual([f["timestamp_s"] for f in frames], [0, 0.5, 1, 1.5])
        self.assertTrue(all(f["image"].startswith("data:image/jpeg;base64,") for f in frames))

    def test_invalid_video_and_sampling_fail(self):
        with self.assertRaises(ValueError): sample(b"invalid", {})
        with self.assertRaises(ValueError): sample(b"", {})
        with self.assertRaises(ValueError): sample(b"clip", {"count": 100})


class HTTPTests(unittest.TestCase):
    def setUp(self):
        self.server = make_server(0, Run(FakeAdapter()))
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base = f"http://127.0.0.1:{self.server.server_address[1]}"
        self.opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        with self.opener.open(self.base + "/api/state") as response:
            self.state = json.load(response)

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()

    def post(self, path, body, headers=None):
        data = body if isinstance(body, bytes) else json.dumps(body).encode()
        req = urllib.request.Request(self.base + path, data, {"X-Avocado-Token": self.state["token"], **(headers or {})})
        return self.opener.open(req)

    def test_static_controls_consent_and_reset(self):
        with self.opener.open(self.base) as response:
            self.assertIn(b"Run all", response.read())
            self.assertIn("no-store", response.headers["Cache-Control"])
        with self.assertRaises(urllib.error.HTTPError) as exc:
            self.post("/api/upload", b"clip")
        self.assertEqual(exc.exception.code, 400)
        with self.post("/api/upload", b"clip", {"X-Upload-Consent": "yes"}) as response:
            self.assertNotEqual(json.load(response)["run_id"], self.state["run_id"])
        with self.post("/api/reset", {}) as response:
            state = json.load(response)
            self.assertEqual(state["history"], {})
            self.assertEqual(state["frames"], [])

    def test_reject_cross_origin_wrong_host_and_missing_token(self):
        for headers in ({"Origin": "https://attacker.example"}, {"Host": "attacker.example"}, {"X-Avocado-Token": ""}):
            with self.subTest(headers=headers), self.assertRaises(urllib.error.HTTPError) as exc:
                self.post("/api/reset", {}, headers)
            self.assertEqual(exc.exception.code, 403)


class AdapterTests(unittest.TestCase):
    def test_requires_explicit_route_and_refuses_public_route(self):
        adapter = LocalChat()
        adapter.base_url = ""
        with self.assertRaisesRegex(ValueError, "no route"):
            adapter.complete("local", "test", {}, {})
        adapter.base_url = "http://8.8.8.8"
        with self.assertRaisesRegex(ValueError, "local/private"):
            adapter.complete("local", "test", {}, {})
        adapter.base_url = "http://example.com"
        with self.assertRaisesRegex(ValueError, "external DNS"):
            adapter.complete("local", "test", {}, {})
        adapter.base_url = "http://127.0.0.1:11434/v1"
        with self.assertRaisesRegex(ValueError, "native Ollama"):
            adapter.complete("local", "test", {}, {})

    def test_real_local_chat_image_text_and_http_error(self):
        captured = []

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                payload = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                if self.path == "/api/show":
                    self.send_response(200)
                    self.end_headers()
                    manifest = {"model_info": {"general.architecture": "test"}, "capabilities": ["vision", "completion"]}
                    if payload["model"] == "remote-model":
                        manifest["remote_host"] = "https://example.com"
                    if payload["model"] == "text-only":
                        manifest["capabilities"] = ["completion"]
                    self.wfile.write(json.dumps(manifest).encode())
                    return
                captured.append(payload)
                if payload["model"] == "bad":
                    self.send_response(503)
                    self.end_headers()
                    self.wfile.write(b'{"error":"route unavailable"}')
                    return
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps({"message": {"content": "{}"}, "done": True}).encode())

            def log_message(self, *args): pass

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            adapter = LocalChat()
            adapter.base_url = f"http://127.0.0.1:{server.server_address[1]}"
            adapter.complete("local", "Observe", {}, {"temperature": 0.2}, FRAMES)
            adapter.complete("local", "Rank", {}, {})
            self.assertEqual(captured[0]["messages"][0]["images"][0], FRAMES[0]["image"].split(",", 1)[1])
            self.assertNotIn("images", captured[1]["messages"][0])
            self.assertFalse(captured[0]["think"])
            self.assertEqual(captured[0]["format"], "json")
            self.assertEqual(adapter.complete("bad", "test", {}, {})["http_status"], 503)
            with self.assertRaisesRegex(ValueError, "remote/cloud"):
                adapter.complete("remote-model", "test", {}, {})
            with self.assertRaisesRegex(ValueError, "vision"):
                adapter.complete("text-only", "test", {}, {}, FRAMES)
            with self.assertRaisesRegex(ValueError, "Cloud"):
                adapter.complete("model:cloud", "test", {}, {})
        finally:
            server.shutdown()
            server.server_close()
            thread.join()


if __name__ == "__main__":
    unittest.main()
