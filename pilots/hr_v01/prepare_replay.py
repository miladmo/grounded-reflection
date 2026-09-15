"""Create a clean local checkout for a repeat; does not make model calls."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path, help="New, nonexistent directory")
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[2]
    destination = args.destination.resolve()
    if destination.exists():
        raise SystemExit("Destination already exists; nothing was changed")
    if destination == source or source in destination.parents:
        raise SystemExit("Use a destination outside this repository")
    manifest = json.loads((source / "pilots/hr_v01/frozen_manifest.json").read_text(encoding="utf-8"))
    paths = list(manifest["files"]) + ["pyproject.toml", "README.md", "LICENSE",
        "src/grounded_reflection/__init__.py", "src/grounded_reflection/__main__.py",
        "src/grounded_reflection/cli.py"]
    for name in paths:
        path = (source / name).resolve()
        if source not in path.parents or not path.is_file() or path.is_symlink():
            raise SystemExit(f"Unexpected source: {name}")
        if name in manifest["files"] and hashlib.sha256(path.read_bytes()).hexdigest() != manifest["files"][name]:
            raise SystemExit(f"Frozen input changed: {name}; nothing was copied")
    for name in paths:
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source / name, target)
    print(f"Prepared clean replay at {destination}. No model calls made.")
    print("From that directory install with: python -m pip install .")
    print("Then run: python pilots/hr_v01/run_pilot.py freeze")
    print("Then run stages prepare, generate, judge, report in that order.")
    print("Those stages use 27 Codex model calls through your own authenticated account.")


if __name__ == "__main__":
    main()
