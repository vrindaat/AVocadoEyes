"""Explicit opt-in real Ollama check. Uses synthetic, non-personal inputs only."""
import argparse
import json
import subprocess
import tempfile
import time
from pathlib import Path

import imageio_ffmpeg

from avocadoeyes.inference import LocalChat, parse_response
from avocadoeyes import contracts
from avocadoeyes.runner import Run, default_config


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ranking-only", action="store_true", help="Check real ranking inference against explicit frozen synthetic observations")
    parser.add_argument("--text-stages", action="store_true", help="Check attribute extraction then ranking on frozen synthetic observations")
    args = parser.parse_args()
    adapter = LocalChat()
    if args.text_stages:
        from test_workbench import OBS, FRAMES
        run = Run(adapter)
        run.configure(run.config, {"goals": "Find a small group for a calm conversation"}, run.rubric)
        # Frozen synthetic observations exercise real text models without private footage.
        run.results["sample"] = {"status": "current", "output": {"frames": FRAMES}, "revision": "synthetic-frames"}
        run.results["validate"] = {"status": "current", "output": OBS, "revision": "synthetic-observations"}
        success = run.execute("process", "from")
        print(json.dumps({"text_stages_check": success,
                          "steps": {sid: {k: run.results[sid][k] for k in ("status", "model", "elapsed_s", "error") if k in run.results[sid]}
                                    for sid in ("process", "rank") if sid in run.results},
                          "note": "Frozen synthetic observations; no visual accuracy or outcome-quality claim."}, indent=2), flush=True)
        if not success:
            raise SystemExit(1)
        return
    if args.ranking_only:
        from test_workbench import OBS
        inputs = {"observations": OBS, "context": {"goals": "Find a small group for a calm conversation", "personality_preferences": "Prefer quiet reciprocal interactions"},
                  "rubric": Run().rubric, "additional_inputs": {"test_note": "Synthetic frozen observations for interface testing only, not a real person or measured behavior."}}
        begin = time.perf_counter()
        step = default_config()["steps"][-1]
        schema = contracts.output_schema("ranking")
        response = adapter.complete("qwen3.5:9b", step["prompt"] + "\nRequired output JSON schema:\n" + json.dumps(schema), inputs, {**step["settings"], "format": schema})
        output = contracts.ranking(parse_response(response["raw"]), OBS)
        print(json.dumps({"ranking_check": "passed", "elapsed_s": round(time.perf_counter() - begin, 3), "output": output,
                          "note": "Frozen synthetic observation fixture only; no observation accuracy or outcome-quality claim."}, indent=2), flush=True)
        return
    begin = time.perf_counter()
    text = adapter.complete("qwen3.5:9b", 'Return only the JSON object {"ok":true}.', {}, {"temperature": 0, "max_tokens": 4096})
    parsed = parse_response(text["raw"])
    if parsed != {"ok": True}:
        raise ValueError(f"Unexpected text smoke output: {parsed}")
    print(json.dumps({"text_check": "passed", "elapsed_s": round(time.perf_counter() - begin, 3)}), flush=True)
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "synthetic.mp4"
        subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-hide_banner", "-loglevel", "error", "-f", "lavfi", "-i", "testsrc=size=320x240:rate=10", "-t", "2", "-pix_fmt", "yuv420p", str(path)], check=True, capture_output=True)
        run = Run(adapter)
        config = run.config
        config["steps"][0]["settings"] = {"count": 2, "seconds": 2}
        run.configure(config, {"goals": "Meet a small group"}, run.rubric)
        run.upload(path.read_bytes(), "synthetic.mp4")
        success = run.execute("", "all")
    print(json.dumps({"pipeline_check": success, "steps": {sid: {k: r[k] for k in ("status", "elapsed_s", "error") if k in r} for sid, r in run.results.items()},
                      "ranking": run.results.get("rank", {}).get("output"), "note": "Synthetic clip has no people; expected abstention, no quality/GB10 routing claim."}, indent=2), flush=True)
    if not success:
        raise SystemExit(1)
    if run.results["rank"]["output"]["status"] != "insufficient_evidence":
        raise ValueError("Synthetic empty scene should abstain")


if __name__ == "__main__":
    main()
