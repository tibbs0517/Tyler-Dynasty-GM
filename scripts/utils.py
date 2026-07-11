import json
from pathlib import Path

DATA = Path("data")


def load_json(filename):
    with open(DATA / filename, "r") as f:
        return json.load(f)


def save_json(filename, data):
    with open(DATA / filename, "w") as f:
        json.dump(data, f, indent=2)
