#!/usr/bin/env python3
"""
main.py

Menu + CLI runner that imports the three algorithms:
 - wagner_fischer_with_log (from WagnerFischer.py)
 - hirschberg_with_log   (from Hirschberg.py)
 - ukkonen_levenshtein  (from Ukkonen.py)
"""

from typing import Optional
import argparse
import pprint
import sys

from WagnerFischer import wagner_fischer_with_log
from Hirschberg import hirschberg_with_log
from Ukkonen import ukkonen_levenshtein


pp = pprint.PrettyPrinter(width=120, compact=False)


def run_wagner(a: str, b: str) -> None:
    res = wagner_fischer_with_log(a, b)
    print("\n==== Wagner–Fischer (full DP) ====")
    print("Levenshtein distance:", res["distance"])
    print("\nOperations (applied, in order):")
    pp.pprint(res["ops"])
    print("\nTransformations (step-by-step):")
    for idx, s in enumerate(res["transformations"]):
        print(f"  [{idx:2d}] {s}")


def run_hirschberg(a: str, b: str) -> None:
    applied, transformations = hirschberg_with_log(a, b)
    print("\n==== Hirschberg (divide & conquer) ====")
    edit_ops = [op for op in applied if op.get("op") in ("insert", "delete", "substitute")]
    print("Edit distance (count of insert/delete/substitute):", len(edit_ops))
    print("\nOperations (applied, in order):")
    pp.pprint(applied)
    print("\nTransformations (step-by-step):")
    for idx, s in enumerate(transformations):
        print(f"  [{idx:2d}] {s}")


def run_ukkonen(a: str, b: str, k: int) -> None:
    print("\n==== Ukkonen (bounded Levenshtein) ====")
    res = ukkonen_levenshtein(a, b, k)
    if res is None:
        print(f"No alignment within distance {k} (distance > {k}).")
    else:
        print(f"Levenshtein distance = {res}")


def interactive_menu() -> None:
    while True:
        print("\n=== Edit Distance Algorithms ===")
        print("1) Wagner–Fischer (full DP, logs)")
        print("2) Hirschberg (divide & conquer, logs)")
        print("3) Ukkonen (bounded Levenshtein)")
        print("4) Exit")
        choice = input("Choose [1-4]: ").strip()
        if choice == "4":
            print("Goodbye!")
            return

        a = input("Enter first string: ")
        b = input("Enter second string: ")

        if choice == "1":
            run_wagner(a, b)
        elif choice == "2":
            run_hirschberg(a, b)
        elif choice == "3":
            try:
                k = int(input("Enter threshold k (non-negative integer): ").strip())
            except ValueError:
                print("Invalid k — must be integer. Returning to menu.")
                continue
            run_ukkonen(a, b, k)
        else:
            print("Invalid choice — try again.")


def cli_run(args: argparse.Namespace) -> int:
    a = args.a
    b = args.b
    mode = args.mode.lower()

    if mode == "wagner":
        run_wagner(a, b)
    elif mode == "hirschberg":
        run_hirschberg(a, b)
    elif mode == "ukkonen":
        if args.k is None:
            print("Error: --k is required for ukkonen mode.", file=sys.stderr)
            return 2
        run_ukkonen(a, b, args.k)
    else:
        print(f"Unknown mode: {args.mode}", file=sys.stderr)
        return 2
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="main.py", description="Run edit-distance algorithms.")
    p.add_argument("--mode", choices=["wagner", "hirschberg", "ukkonen"],
                   help="Run a specific algorithm non-interactively. If omitted, runs interactive menu.")
    p.add_argument("--a", help="First string (required when --mode provided).")
    p.add_argument("--b", help="Second string (required when --mode provided).")
    p.add_argument("--k", type=int, help="Threshold k (required for ukkonen mode).")
    return p


def run() -> int:
    parser = build_parser()
    args = parser.parse_args()

    # If mode provided, require a and b
    if args.mode:
        if not args.a or not args.b:
            parser.error("--a and --b are required when --mode is provided.")
            return 2
        return cli_run(args)

    # interactive
    try:
        interactive_menu()
        return 0
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
        return 1


if __name__ == "__main__":
    raise SystemExit(run())
