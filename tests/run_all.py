"""Run every deadfinder test as a plain script (no pytest needed)."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

import test_finder  # noqa: E402

if __name__ == "__main__":
    test_finder.test_unused_imports_detected()
    test_finder.test_unused_functions_detected()
    test_finder.test_tree_scan_and_aggregate()
    print("ALL DEADFINDER TESTS PASSED")
