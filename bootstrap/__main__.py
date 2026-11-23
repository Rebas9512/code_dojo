"""python -m bootstrap serve --protocol jsonl"""
import argparse
import sys
from pathlib import Path


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["serve"])
    parser.add_argument("--protocol", required=True, choices=["jsonl"])
    parser.parse_args()
    bundle = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(bundle / "libraries"))
    from .protocol import run
    run(bundle)


if __name__ == "__main__":
    main()
