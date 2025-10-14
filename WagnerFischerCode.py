#!/usr/bin/env python3
"""
wagner_fischer.py

Provides wagner_fischer_with_log(s, t) to compute Levenshtein distance
and a main() that accepts command-line or interactive input and prints results.
"""

from typing import List, Dict, Any
import pprint
import sys

def wagner_fischer_with_log(s: str, t: str) -> Dict[str, Any]:
    m, n = len(s), len(t)
    D = [[0] * (n + 1) for _ in range(m + 1)]
    choice = [["" for _ in range(n + 1)] for __ in range(m + 1)]

    # base cases
    for i in range(m + 1):
        D[i][0] = i
        choice[i][0] = "start" if i == 0 else "delete"
    for j in range(n + 1):
        D[0][j] = j
        choice[0][j] = "start" if j == 0 else "insert"

    # fill DP with tie-break: match/substitute > delete > insert
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s[i - 1] == t[j - 1]:
                cost_diag = D[i - 1][j - 1]
            else:
                cost_diag = D[i - 1][j - 1] + 1
            cost_del = D[i - 1][j] + 1
            cost_ins = D[i][j - 1] + 1

            best = min(cost_diag, cost_del, cost_ins)
            D[i][j] = best

            # tie-breaking order: prefer diag (match/sub), then delete, then insert
            if best == cost_diag and s[i - 1] == t[j - 1]:
                choice[i][j] = "match"
            elif best == cost_diag:
                choice[i][j] = "substitute"
            elif best == cost_del:
                choice[i][j] = "delete"
            else:
                choice[i][j] = "insert"

    # backtrack to produce forward ops
    i, j = m, n
    rev_ops = []
    while i > 0 or j > 0:
        op = choice[i][j]
        if op == "match":
            rev_ops.append({"op": "match", "pos": i - 1, "char": s[i - 1]})
            i, j = i - 1, j - 1
        elif op == "substitute":
            rev_ops.append({"op": "substitute", "pos": i - 1, "from": s[i - 1], "to": t[j - 1]})
            i, j = i - 1, j - 1
        elif op == "delete":
            rev_ops.append({"op": "delete", "pos": i - 1, "char": s[i - 1]})
            i = i - 1
        elif op == "insert":
            rev_ops.append({"op": "insert", "pos": i, "char": t[j - 1]})
            j = j - 1
        else:
            # safety fallback (shouldn't happen) - break to avoid infinite loop
            break

    ops = list(reversed(rev_ops))

    # apply ops forward to get transformations
    cur = list(s)
    transformations = ["".join(cur)]
    applied_ops = []
    for action in ops:
        if action["op"] == "match":
            applied_ops.append({"op": "match", "pos": action["pos"], "char": action["char"]})
            transformations.append("".join(cur))
        elif action["op"] == "substitute":
            pos = action["pos"]
            if 0 <= pos < len(cur):
                old = cur[pos]
                cur[pos] = action["to"]
                applied_ops.append({"op": "substitute", "pos": pos, "from": old, "to": action["to"]})
            else:
                # defensive: if pos out of range, skip substitute but log it
                applied_ops.append({"op": "substitute", "pos": pos, "from": None, "to": action["to"]})
            transformations.append("".join(cur))
        elif action["op"] == "delete":
            pos = action["pos"]
            if 0 <= pos < len(cur):
                removed = cur.pop(pos)
                applied_ops.append({"op": "delete", "pos": pos, "char": removed})
            else:
                applied_ops.append({"op": "delete", "pos": pos, "char": None})
            transformations.append("".join(cur))
        elif action["op"] == "insert":
            pos = action["pos"]
            if pos < 0: pos = 0
            if pos > len(cur): pos = len(cur)
            cur.insert(pos, action["char"])
            applied_ops.append({"op": "insert", "pos": pos, "char": action["char"]})
            transformations.append("".join(cur))
        else:
            transformations.append("".join(cur))

    return {
        "distance": D[m][n],
        "D": D,
        "choice": choice,
        "ops": applied_ops,
        "transformations": transformations
    }


def print_summary(result: Dict[str, Any]) -> None:
    """Nicely print key parts of the result."""
    pp = pprint.PrettyPrinter(width=120, compact=False)
    print("\nLevenshtein distance:", result["distance"])
    print("\nStep-by-step transformations (initial -> ... -> target):")
    for idx, s in enumerate(result["transformations"]):
        print(f"  [{idx:2d}] {s}")
    print("\nOperations applied (in order):")
    pp.pprint(result["ops"])


def main(argv: List[str] = None) -> int:
    """Entry point: accepts two strings either as argv or via input() and prints result."""
    if argv is None:
        argv = sys.argv[1:]

    if len(argv) >= 2:
        s = argv[0]
        t = argv[1]
    else:
        s = input("Enter source string s: ")
        t = input("Enter target string t: ")

    result = wagner_fischer_with_log(s, t)
    print_summary(result)
    return 0


if __name__ == "__main__":
    main()
