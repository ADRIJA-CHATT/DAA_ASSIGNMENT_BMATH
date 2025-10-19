#!/usr/bin/env python3
"""
wagner_fischer_fixed.py

Compute Levenshtein distance with Wagner-Fischer algorithm, including a correct
operation log and step-by-step transformations. Positions are adjusted when
replaying operations to account for previous inserts/deletes.
"""

from typing import List, Dict, Any
import pprint

def wagner_fischer_with_log(s: str, t: str) -> Dict[str, Any]:
    m, n = len(s), len(t)
    
    # Initialize distance matrix D (size (m+1)x(n+1))
    D = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Initialize choice matrix to store operation types for backtracking
    # Possible values: "match", "substitute", "delete", "insert", "start"
    choice = [["" for _ in range(n + 1)] for __ in range(m + 1)]

    # Base cases: transforming empty prefix of s/t
    for i in range(m + 1):
        D[i][0] = i  # cost of deleting all characters from s[:i]
        choice[i][0] = "start" if i == 0 else "delete"
    for j in range(n + 1):
        D[0][j] = j  # cost of inserting all characters of t[:j]
        choice[0][j] = "start" if j == 0 else "insert"

    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # Cost of substitution or match
            cost_diag = D[i - 1][j - 1] + (0 if s[i - 1] == t[j - 1] else 1)
            # Cost of deletion
            cost_del = D[i - 1][j] + 1
            # Cost of insertion
            cost_ins = D[i][j - 1] + 1

            # Choose minimal cost
            best = min(cost_diag, cost_del, cost_ins)
            D[i][j] = best

            # Tie-breaking: prefer diagonal (match/substitute) > delete > insert
            if best == cost_diag:
                choice[i][j] = "match" if s[i - 1] == t[j - 1] else "substitute"
            elif best == cost_del:
                choice[i][j] = "delete"
            else:
                choice[i][j] = "insert"

    # Backtrack to generate reverse-chronological operation list
    i, j = m, n
    rev_ops: List[Dict[str, Any]] = []
    while i > 0 or j > 0:
        op = choice[i][j]
        if op == "match":
            rev_ops.append({"op": "match", "pos": i - 1, "char": s[i - 1]})
            i, j = i - 1, j - 1
        elif op == "substitute":
            rev_ops.append({"op": "substitute", "pos": i - 1,
                            "from": s[i - 1], "to": t[j - 1]})
            i, j = i - 1, j - 1
        elif op == "delete":
            rev_ops.append({"op": "delete", "pos": i - 1, "char": s[i - 1]})
            i -= 1
        elif op == "insert":
            rev_ops.append({"op": "insert", "pos": i, "char": t[j - 1]})
            j -= 1
        else:
            break

    # Reverse ops to chronological order
    ops = list(reversed(rev_ops))

    # Helper function: adjust original position to current string index
    # considering previously applied insertions and deletions
    def adjusted_pos(original_pos: int, applied_ops: List[Dict[str, Any]]) -> int:
        shift = 0
        for a in applied_ops:
            p = a["pos"]
            if a["op"] == "insert" and p <= original_pos:
                shift += 1
            elif a["op"] == "delete" and p < original_pos:
                shift -= 1
        return original_pos + shift

    # Apply operations step-by-step to reconstruct intermediate strings
    cur: List[str] = list(s)  # current string state
    transformations: List[str] = ["".join(cur)]  # list of string states
    applied_ops: List[Dict[str, Any]] = []  # chronological operations applied

    for action in ops:
        if action["op"] == "match":
            # Match does not modify string
            pos = adjusted_pos(action["pos"], applied_ops)
            applied_ops.append({"op": "match", "pos": pos,
                                "char": cur[pos] if 0 <= pos < len(cur) else None})
            transformations.append("".join(cur))

        elif action["op"] == "substitute":
            orig_pos = action["pos"]
            pos = adjusted_pos(orig_pos, applied_ops)
            to_char = action["to"]
            if 0 <= pos < len(cur):
                old = cur[pos]
                cur[pos] = to_char
                applied_ops.append({"op": "substitute", "pos": pos, "from": old, "to": to_char})
            else:
                applied_ops.append({"op": "substitute", "pos": pos, "from": None, "to": to_char})
            transformations.append("".join(cur))

        elif action["op"] == "delete":
            orig_pos = action["pos"]
            pos = adjusted_pos(orig_pos, applied_ops)
            if 0 <= pos < len(cur):
                removed = cur.pop(pos)
                applied_ops.append({"op": "delete", "pos": pos, "char": removed})
            else:
                applied_ops.append({"op": "delete", "pos": pos, "char": None})
            transformations.append("".join(cur))

        elif action["op"] == "insert":
            orig_pos = action["pos"]
            pos = adjusted_pos(orig_pos, applied_ops)
            pos = max(0, min(pos, len(cur)))  # clamp to valid range
            cur.insert(pos, action["char"])
            applied_ops.append({"op": "insert", "pos": pos, "char": action["char"]})
            transformations.append("".join(cur))

        else:
            # Unknown operation: append current state
            transformations.append("".join(cur))

    return {
        "distance": D[m][n],           # final Levenshtein distance
        "D": D,                        # full DP matrix
        "choice": choice,              # choice matrix for debugging
        "ops": applied_ops,            # chronological operations applied
        "transformations": transformations  # string states after each operation
    }


def print_summary(result: Dict[str, Any]) -> None:
    """Print distance, transformations, and applied operations."""
    pp = pprint.PrettyPrinter(width=120, compact=False)
    print("\nLevenshtein distance:", result["distance"])
    print("\nStep-by-step transformations (initial -> ... -> target):")
    for idx, s in enumerate(result["transformations"]):
        print(f"  [{idx:2d}] {s}")
    print("\nOperations applied (in order):")
    pp.pprint(result["ops"])


def main() -> int:
    """Main entry point: get two strings and display distance and operations."""
    s = input("Enter source string: ").strip()
    t = input("Enter target string: ").strip()

    print(f"Source string: {s}")
    print(f"Target string: {t}")

    result = wagner_fischer_with_log(s, t)
    print_summary(result)
    return 0


if __name__ == "__main__":
    main()
