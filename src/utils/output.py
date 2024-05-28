from pathlib import Path

from msgspec.json import encode

root = Path("data/output")

if not root.exists():
    root.mkdir(parents=True)


def save_output(name: str, data):
    (root / name).with_suffix(".json").write_bytes(encode(data))
