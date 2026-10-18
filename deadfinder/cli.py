#!/usr/bin/env python3
"""CLI for deadfinder: report dead code in a project.

Usage:
    python -m deadfinder [path]            # analyze a dir or file
    python -m deadfinder --summary         # counts only, no listing
"""
import argparse
import sys

from .finder import analyze_file, analyze_tree, total_findings


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path", nargs="?", default=".", help="file or dir")
    ap.add_argument("--summary", action="store_true",
                    help="print aggregate counts instead of findings")
    args = ap.parse_args(argv)

    import os
    if os.path.isdir(args.path):
        reports = analyze_tree(args.path)
    else:
        reports = [analyze_file(args.path)]

    if args.summary:
        s = total_findings(reports)
        print(f"{s['files']} files, {s['unused_imports']} unused imports, "
              f"{s['unused_functions']} unused functions "
              f"(total {s['total']})")
        return 0

    for r in reports:
        for item in r["unused_imports"]:
            print(f"{r['path']}:{item['line']} unused import "
                  f"{item['name']}")
        for item in r["unused_functions"]:
            print(f"{r['path']}:{item['line']} unused function "
                  f"{item['name']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
