"""Versioned JSON contracts plus scene/evidence referential integrity."""
import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def output_schema(definition):
    schema = json.loads((ROOT / "docs/contracts/workbench-output.schema.json").read_text())
    schema["$ref"] = f"#/$defs/{definition}"
    return schema


def validate(value, contract, definition=None):
    schema = json.loads((ROOT / "docs/contracts" / f"workbench-{contract}.schema.json").read_text())
    if definition:
        schema["$ref"] = f"#/$defs/{definition}"
    Draft202012Validator(schema).validate(value)


def observations(value, frames):
    validate(value, "output", "observation")
    frame_ids = {f["id"] for f in frames}
    people, evidence = set(), set()
    for person in value["people"]:
        if person["id"] in people:
            raise ValueError("Duplicate person ID")
        people.add(person["id"])
        locations = set()
        for location in person["locations"]:
            x, y, w, h = location["box"]
            if location["frame_id"] not in frame_ids or w <= 0 or h <= 0 or x + w > 1.000001 or y + h > 1.000001:
                raise ValueError("Invalid scene frame or normalized [x,y,width,height] box")
            locations.add(location["frame_id"])
        for cue in person["evidence"]:
            if cue["id"] in evidence or cue["frame_id"] not in locations:
                raise ValueError("Duplicate evidence ID or evidence without person location")
            evidence.add(cue["id"])
    return value


def ranking(value, observation):
    validate(value, "output", "ranking")
    people = {p["id"]: p for p in observation["people"]}
    seen = set()
    if (value["status"] == "ok") != bool(value["candidates"]):
        raise ValueError("Ranking status must match candidate availability")
    for candidate in value["candidates"]:
        pid = candidate["person_id"]
        if pid not in people or pid in seen or people[pid]["identity_uncertain"]:
            raise ValueError("Unknown, duplicate or ambiguous candidate ID")
        seen.add(pid)
        usable = {e["id"] for e in people[pid]["evidence"] if e["visibility"] != "unobservable"}
        if not set(candidate["evidence_ids"]) <= usable:
            raise ValueError("Ranking cites absent, unobservable or another person's evidence")
    return value
