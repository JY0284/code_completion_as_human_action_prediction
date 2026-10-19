"""Print raw actions from a Python file without executing the input program."""

import argparse
import ast
import json
from pathlib import Path
import sys
import tokenize


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "src" / "analysis"))

from call_extractor import CallExtractor


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "source",
        nargs="?",
        type=Path,
        default=REPOSITORY_ROOT / "sample" / "py_demo.py",
        help="Python source to parse (default: sample/py_demo.py)",
    )
    args = parser.parse_args()

    try:
        # Honor Python encoding declarations without importing the input file.
        with tokenize.open(str(args.source)) as source_file:
            tree = ast.parse(source_file.read(), filename=str(args.source))
    except (OSError, SyntaxError, UnicodeError) as error:
        parser.exit(1, "Cannot parse {}: {}\n".format(args.source, error))

    actions = []
    CallExtractor().visit_and_save(tree, actions)
    print(json.dumps(actions, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
