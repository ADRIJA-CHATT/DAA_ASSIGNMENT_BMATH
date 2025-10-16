#!/usr/bin/env python3
"""
wagner_fischer_fixed.py

wagner_fischer_with_log(s, t) to compute Levenshtein distance and a correct
operation log + transformations (positions adjusted while replaying ops).
"""

from typing import List, Dict, Any
import pprint
import sys


def wagner_fischer_with_log(s: str, t: str) -> Dict[str, Any]:
    m, n = len(s), len(t)
    # Distance matrix
    D = [[0] * (n + 1) for _ in range(m + 1)]
    # choice matrix: "match", "substitute", "delete", "insert", "start"
    choice = [["" for _ in range(n + 1)] for __ in range(m + 1)]

    # base cases
    for i in range(m + 1):
        D[i][0] = i
        choice[i][0] = "start" if i == 0 else "delete"
    for j in range(n + 1):
        D[0][j] = j
        choice[0][j] = "start" if j == 0 else "insert"

    # fill DP with tie-break: prefer diag (match/substitute) > delete > insert
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost_diag = D[i - 1][j - 1] + (0 if s[i - 1] == t[j - 1] else 1)
            cost_del = D[i - 1][j] + 1
            cost_ins = D[i][j - 1] + 1

            best = min(cost_diag, cost_del, cost_ins)
            D[i][j] = best

            # tie-breaking order: diag (match/sub) then delete then insert
            if best == cost_diag:
                if s[i - 1] == t[j - 1]:
                    choice[i][j] = "match"
                else:
                    choice[i][j] = "substitute"
            elif best == cost_del:
                choice[i][j] = "delete"
            else:
                choice[i][j] = "insert"

    # Backtrack from (m,n) to produce reverse-chronological ops (rev_ops).
    i, j = m, n
    rev_ops: List[Dict[str, Any]] = []
    while i > 0 or j > 0:
        op = choice[i][j]
        if op == "match":
            rev_ops.append({"op": "match", "pos": i - 1, "char": s[i - 1]})
            i, j = i - 1, j - 1
        elif op == "substitute":
            rev_ops.append({
                "op": "substitute",
                "pos": i - 1,
                "from": s[i - 1],
                "to": t[j - 1]
            })
            i, j = i - 1, j - 1
        elif op == "delete":
            rev_ops.append({"op": "delete", "pos": i - 1, "char": s[i - 1]})
            i -= 1
        elif op == "insert":
            # pos = i means "insert at index i in current string"
            rev_ops.append({"op": "insert", "pos": i, "char": t[j - 1]})
            j -= 1
        else:
            # safety: if we ever hit "start" or something unexpected, break
            break

    # Reverse to get chronological list of operations (earliest -> latest)
    ops = list(reversed(rev_ops))

    # Helper: adjust a recorded 'original' pos to the current string index
    # given previously applied ops. This prevents index drift.
    def adjusted_pos(original_pos: int, applied_ops: List[Dict[str, Any]]) -> int:
        """
        original_pos: position recorded during backtracking (in terms of original source indices)
        applied_ops: list of ops already applied (chronological), each op has 'op' and 'pos'
        We interpret rules:
          - previous inserts at p_prev <= original_pos shift the effective position by +1
          - previous deletes at p_prev < original_pos shift effective position by -1
        This heuristic matches how positions recorded from backtrace should be adjusted
        when replaying operations left-to-right.
        """
        shift = 0
        for a in applied_ops:
            p = a["pos"]
            if a["op"] == "insert":
                # insert at p_prev shifts indices >= p_prev by +1.
                if p <= original_pos:
                    shift += 1
            elif a["op"] == "delete":
                # delete at p_prev shifts indices > p_prev by -1 (we use < to match typical behavior)
                if p < original_pos:
                    shift -= 1
            # substitute / match don't change length -> no shift
        return original_pos + shift

    # Apply ops forward to build actual transformations, using adjusted positions
    cur: List[str] = list(s)
    transformations: List[str] = ["".join(cur)]
    applied_ops: List[Dict[str, Any]] = []

    for action in ops:
        if action["op"] == "match":
            # match does nothing to the string, but we record it
            pos = adjusted_pos(action["pos"], applied_ops)
            # guard: ensure pos inside range
            if 0 <= pos < len(cur):
                applied_ops.append({"op": "match", "pos": pos, "char": cur[pos]})
            else:
                # out of range match (shouldn't generally happen) -- log anyway
                applied_ops.append({"op": "match", "pos": pos, "char": None})
            transformations.append("".join(cur))

        elif action["op"] == "substitute":
            orig_pos = action["pos"]
            pos = adjusted_pos(orig_pos, applied_ops)
            to_char = action["to"]
            if 0 <= pos < len(cur):
                old = cur[pos]
                cur[pos] = to_char
                applied_ops.append({
                    "op": "substitute",
                    "pos": pos,
                    "from": old,
                    "to": to_char
                })
            else:
                # position outside current string — record a 'failed' substitute
                applied_ops.append({
                    "op": "substitute",
                    "pos": pos,
                    "from": None,
                    "to": to_char
                })
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
            # insert positions are allowed to be at len(cur) (append)
            pos = adjusted_pos(orig_pos, applied_ops)
            # clamp pos
            if pos < 0:
                pos = 0
            if pos > len(cur):
                pos = len(cur)
            cur.insert(pos, action["char"])
            applied_ops.append({"op": "insert", "pos": pos, "char": action["char"]})
            transformations.append("".join(cur))

        else:
            # unknown op; append current string and continue
            transformations.append("".join(cur))

    return {
        "distance": D[m][n],
        "D": D,
        "choice": choice,
        "ops": applied_ops,  # chronological applied operations with adjusted positions
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
    """Ask user for two strings and print result."""
    if argv is None:
        argv = sys.argv[1:]

    if len(argv) < 2:
        s = input("Enter source string: ").strip()
        t = input("Enter target string: ").strip()
    else:
        s, t = argv[0], argv[1]

    result = wagner_fischer_with_log(s, t)
    print_summary(result)
    return 0


if __name__ == "__main__":
    main()
