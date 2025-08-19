import sys
from pathlib import Path

# put src/ at front of sys.path so "import visualapi" works
ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))