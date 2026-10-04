"""Run one explicitly selected v0.2 stage from a source checkout."""

from pathlib import Path
import sys

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / 'src'))

from grounded_reflection.pilot_v02.runner import main

if __name__ == '__main__':
    main(REPO)
