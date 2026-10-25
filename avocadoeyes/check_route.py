"""Run real image + text inference using an authorized clip, without saving data."""
import argparse
import importlib.metadata
import json
import platform
import sys
import time
from pathlib import Path

from .runner import Run


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video", required=True)
    parser.add_argument("--model", default="qwen3.5:9b")
    parser.add_argument("--goals", required=True)
    parser.add_argument("--consent", action="store_true", required=True, help="Confirm permission to process the clip locally")
    args = parser.parse_args()
    path = Path(args.video)
    if path.stat().st_size > 64 * 1024 * 1024:
        parser.error("Clip exceeds 64 MiB")
    run = Run()
    config = run.config
    config["models"] = {"vision": args.model, "reasoning": args.model}
    run.configure(config, {"goals": args.goals}, run.rubric)
    run.upload(path.read_bytes(), path.name)
    begin = time.perf_counter()
    ok = run.execute("", "all")
    report = {"execution_succeeded": ok, "python": platform.python_version(), "platform": platform.platform(),
              "packages": {name: importlib.metadata.version(name) for name in ("imageio-ffmpeg", "jsonschema")},
              "route": run.adapter.base_url, "requested_model": args.model,
              "elapsed_s": round(time.perf_counter() - begin, 3), "steps": {},
              "note": "Local image/text execution evidence only; independently verify GB10 GPU and routing. No outcome-quality claim."}
    for sid, result in run.results.items():
        report["steps"][sid] = {k: result[k] for k in ("status", "elapsed_s", "error", "model") if k in result}
        if "raw" in result:
            try:
                report["steps"][sid]["returned_model"] = json.loads(result["raw"]).get("model")
            except (ValueError, AttributeError):
                pass
    report["ranking_status"] = run.results.get("rank", {}).get("output", {}).get("status")
    print(json.dumps(report, indent=2))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
