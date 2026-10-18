"""deadfinder: AST-based dead code detector for Python."""
from .finder import analyze_source, analyze_file, analyze_tree, total_findings

__version__ = "0.1.0"
__all__ = ["analyze_source", "analyze_file", "analyze_tree",
           "total_findings"]
