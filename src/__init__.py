"""Prompt-eval-lab evaluator package.

Small, single-responsibility modules:

- ``scoring``           pure scoring math (dimensions, weights, aggregate, classify, flags)
- ``schemas``          jsonschema definitions for test cases and reviewed score files
- ``evaluator``        CLI entry point (``python -m src.evaluator``)
- ``report_generator`` renders evaluated results to ``reports/evaluation_summary.md``

All data in this lab is synthetic and for QA demonstration only.
"""

__all__ = ["scoring", "schemas", "evaluator", "report_generator"]
