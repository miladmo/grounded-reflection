"""Check replay integrity and output boundaries without model calls."""

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


class ReplayTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="reflection-replay-test-")
        root = Path(self.temporary.name)
        self.source = root / "source"
        self.destination = root / "replay"
        self.script = self.source / "pilots/hr_v01/prepare_replay.py"
        self.script.parent.mkdir(parents=True)
        shutil.copyfile(Path(__file__).resolve().parents[1] / "pilots/hr_v01/prepare_replay.py", self.script)
        self.frozen = {"pilots/hr_v01/tasks.json": b'{"tasks": []}\r\n',
                       "src/grounded_reflection/workflow.py": b"# frozen test fixture\n"}
        self.files = {**self.frozen, **{name: b"replay dependency\n" for name in (
            "pyproject.toml", "README.md", "LICENSE", "src/grounded_reflection/__init__.py",
            "src/grounded_reflection/__main__.py", "src/grounded_reflection/cli.py")}}
        for name, content in self.files.items():
            path = self.source / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        manifest = {"files": {name: hashlib.sha256(content).hexdigest()
                              for name, content in self.frozen.items()}}
        (self.script.parent / "frozen_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        (self.script.parent / "observed_outputs.json").write_text('{"existing_result": true}', encoding="utf-8")

    def tearDown(self):
        self.temporary.cleanup()

    def run_replay(self):
        return subprocess.run([sys.executable, str(self.script), str(self.destination)],
                              capture_output=True, text=True, encoding="utf-8", check=False)

    def test_changed_frozen_file_is_rejected_before_destination_creation(self):
        changed = "src/grounded_reflection/workflow.py"
        (self.source / changed).write_bytes(b"# changed after the experiment\n")
        result = self.run_replay()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Frozen input changed: " + changed, result.stderr)
        self.assertFalse(self.destination.exists())

    def test_verified_replay_copies_exact_bytes_without_previous_results(self):
        result = self.run_replay()
        self.assertEqual(result.returncode, 0, result.stderr)
        copied = {path.relative_to(self.destination).as_posix(): path.read_bytes()
                  for path in self.destination.rglob("*") if path.is_file()}
        self.assertEqual(copied, self.files)


if __name__ == "__main__":
    unittest.main()
