"""Heuristic audit for v0.5 material r2 (no model calls).

Usage: python heuristic_audit.py OUTPUT_DIR
"""

import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
for folder in (REPO / 'src', REPO / 'pilots' / 'v03', HERE.parent):
    sys.path.insert(0, str(folder))

from reflectai_v05.audit import audit, markdown  # noqa: E402

if __name__ == '__main__':
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    result = audit()
    (out / 'heuristic-audit.json').write_text(json.dumps(result, indent=1) + '\n', encoding='utf-8')
    (out / 'heuristic-audit.md').write_text(markdown(result), encoding='utf-8')
    print(markdown(result))
