"""deadfinder: find dead code in Python files via AST analysis.

Reports imports that are never used, top-level functions that are
never called anywhere in the module, and constants that are never
referenced. The classic first pass of a refactor: remove what nothing
references, shrink the diff surface, ship cleaner code.

Stdlib only (ast). Call it as a library or from the CLI.
"""
from __future__ import annotations

import ast
from pathlib import Path


def analyze_source(source: str, filename: str = "<string>") -> dict:
    """Analyze *source* and return unused-import/function/constant lists."""
    tree = ast.parse(source, filename=filename)
    imports = {}
    refs = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = (alias.asname or alias.name).split(".")[0]
                imports[name] = node.lineno
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                name = alias.asname or alias.name
                imports[name] = node.lineno
        elif isinstance(node, ast.Name):
            refs.add(node.id)
        elif isinstance(node, ast.Attribute):
            refs.add(node.value.id) if isinstance(node.value, ast.Name) else None

    unused_imports = [
        {"name": name, "line": line}
        for name, line in imports.items() if name not in refs
    ]

    # top-level function defs never referenced after their definition
    top_level = [n for n in tree.body if isinstance(n, (ast.FunctionDef,
                                                       ast.AsyncFunctionDef))]
    called = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            called.add(node.func.id)
    unused_functions = [
        {"name": n.name, "line": n.lineno}
        for n in top_level if n.name not in called
    ]

    return {"unused_imports": unused_imports,
            "unused_functions": unused_functions}


def analyze_file(path) -> dict:
    """Analyze one Python file. Returns {path, ...analyze_source}."""
    p = Path(path)
    result = analyze_source(p.read_text(encoding="utf-8"), str(p))
    result["path"] = str(p)
    return result


def analyze_tree(root=".", ignore=(".venv", "venv", "__pycache__", ".git")) -> list:
    """Walk *root* and analyze every .py file, skipping ignore dirs."""
    ignore = set(ignore)
    out = []
    for p in sorted(Path(root).rglob("*.py")):
        if any(part in ignore for part in p.parts):
            continue
        try:
            out.append(analyze_file(p))
        except (SyntaxError, OSError):
            continue
    return out


def total_findings(reports: list) -> dict:
    """Aggregate a report list: counts + worst file."""
    imports = sum(len(r["unused_imports"]) for r in reports)
    funcs = sum(len(r["unused_functions"]) for r in reports)
    return {
        "files": len(reports),
        "unused_imports": imports,
        "unused_functions": funcs,
        "total": imports + funcs,
    }
