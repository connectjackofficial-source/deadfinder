# deadfinder

Find dead code in Python projects with a pure-AST analysis: imports
that are never used, top-level functions that are never called,
aggregated across a whole tree. The fast, dependency-free first pass
of any refactor — remove what nothing references, shrink the diff,
ship cleaner code.

```
deadfinder . --summary
# 42 files, 7 unused imports, 3 unused functions (total 10)
```

## Use

```python
from deadfinder import analyze_source, analyze_tree, total_findings

r = analyze_source(open("module.py").read())
print(r["unused_imports"])   # [{"name": "sys", "line": 3}]
print(r["unused_functions"]) # [{"name": "orphan", "line": 12}]

reports = analyze_tree("src")
print(total_findings(reports))
```

CLI:

```
python -m deadfinder path/to/project
python -m deadfinder path/to/file.py --summary
```

## What it detects

- **unused imports** — imported names never referenced anywhere in the
  module (by Name or Attribute)
- **uncalled top-level functions** — `def`/`async def` at module scope
  whose name never appears as a call target

It is deliberately conservative: no cross-module reachability, no
heuristic guessing — only findings that are provably dead within the
file itself.

## License

MIT — see [LICENSE](LICENSE).
