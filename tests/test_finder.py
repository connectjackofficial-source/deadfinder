"""Tests for deadfinder: unused imports, unused functions, tree scan."""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from deadfinder import analyze_source, analyze_tree, total_findings


SAMPLE = '''
import os
import sys
import math

def used():
    return os.path.abspath(".")

def orphan():
    return "never called"

def caller():
    return used()

value = math.pi
'''


def test_unused_imports_detected():
    r = analyze_source(SAMPLE)
    names = [i["name"] for i in r["unused_imports"]]
    assert "sys" in names, names
    assert "os" not in names   # os is used
    assert "math" not in names  # math.pi referenced
    print("test_unused_imports_detected: ok")


def test_unused_functions_detected():
    r = analyze_source(SAMPLE)
    funcs = [f["name"] for f in r["unused_functions"]]
    assert "orphan" in funcs, funcs
    assert "caller" in funcs, funcs   # defined but never invoked at module level
    assert "used" not in funcs        # called by caller()
    print("test_unused_functions_detected: ok")


def test_tree_scan_and_aggregate():
    tmp = Path(tempfile.mkdtemp())
    (tmp / "pkg").mkdir()
    (tmp / "pkg" / "a.py").write_text(
        "import json\n\ndef hi():\n    return 1\n\nprint(hi())\n",
        encoding="utf-8")
    (tmp / "pkg" / "b.py").write_text(
        "import csv\n\ncsv.writer(open('x','w'))\n", encoding="utf-8")
    reports = analyze_tree(tmp)
    agg = total_findings(reports)
    assert agg["files"] == 2
    assert agg["unused_imports"] == 1  # json in a.py
    assert agg["unused_functions"] == 0  # hi() is called by print()
    print("test_tree_scan_and_aggregate: ok")


if __name__ == "__main__":
    test_unused_imports_detected()
    test_unused_functions_detected()
    test_tree_scan_and_aggregate()
    print("deadfinder tests passed")
