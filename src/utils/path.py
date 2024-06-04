from pathlib import Path

root = Path(__file__).parent.parent.parent

if not root.exists():
    root.mkdir(parents=True)
