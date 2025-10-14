#!/usr/bin/env python3
from typing import List, Dict, Any, Tuple
import pprint
import sys

def _nw_score(A: str, B: str) -> List[int]:
    n = len(B)
    prev = list(range(n + 1))
    for i in range(1, len(A) + 1):
        cur = [i] + [0] * n
        ai = A[i - 1]
        for j in range(1, n + 1):
            cost = 0 if ai == B[j - 1] else 1
            cur[j] = min(prev[j - 1] + cost, prev[j] + 1, cur[j - 1] + 1)
        prev = cur
    return prev

def _align_base(A: str, B: str) -> List[Dict[str, Any]]:
    m, n = len(A), len(B)
    D = [[0] * (n + 1) for _ in range(m + 1)]
    choice = [[""] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        D[i][0] = i
        choice[i][0] = "start" if i == 0 else "delete"
    for j in range(n + 1):
        D[0][j] = j
        choice[0][j] = "start" if j == 0 else "insert"
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if A[i-1] == B[j-1] else 1
            diag = D[i-1][j-1] + cost
            delete = D[i-1][j] + 1
            insert = D[i][j-1] + 1
            best = min(diag, delete, insert)
            D[i][j] = best
            if best == diag and cost == 0:
                choice[i][j] = "match"
            elif best == diag:
                choice[i][j] = "substitute"
            elif best == delete:
                choice[i][j] = "delete"
            else:
                choice[i][j] = "insert"
    # backtrack
    i, j = m, n
    rev_ops = []
    while i > 0 or j > 0:
        op = choice[i][j]
        if op == "match":
            rev_ops.append({"op": "match", "pos": i - 1, "char": A[i - 1]})
            i, j = i - 1, j - 1
        elif op == "substitute":
            rev_ops.append({"op": "substitute", "pos": i - 1, "from": A[i - 1], "to": B[j - 1]})
            i, j = i - 1, j - 1
        elif op == "delete":
            rev_ops.append({"op": "delete", "pos": i - 1, "char": A[i - 1]})
            i = i - 1
        elif op == "insert":
            rev_ops.append({"op": "insert", "pos": i, "char": B[j - 1]})
            j = j - 1
        else:
            break
    return list(reversed(rev_ops))

def hirschberg_with_log(S: str, T: str) -> Tuple[List[Dict[str, Any]], List[str]]:
    def rec(A: str, B: str) -> List[Dict[str, Any]]:
        if len(A) == 0:
            # insert all chars of B, left-to-right; pos increments as we add
            return [{"op": "insert", "pos": i, "char": B[i]} for i in range(len(B))]
        if len(B) == 0:
            # delete all chars of A. Use pos=0 repeatedly (applies to current string).
            return [{"op": "delete", "pos": 0, "char": A[i]} for i in range(len(A))]
        if len(A) == 1 or len(B) == 1:
            return _align_base(A, B)
        mid = len(A) // 2
        scoreL = _nw_score(A[:mid], B)
        scoreR = _nw_score(A[mid:][::-1], B[::-1])
        nB = len(B)
        best_k = 0
        best_val = None
        for k in range(nB + 1):
            val = scoreL[k] + scoreR[nB - k]
            if best_val is None or val < best_val:
                best_val = val
                best_k = k
        left_ops = rec(A[:mid], B[:best_k])
        right_ops = rec(A[mid:], B[best_k:])
        return left_ops + right_ops

    ops = rec(S, T)

    # Apply ops to S to produce transformations
    cur = list(S)
    transformations = ["".join(cur)]
    applied = []
    for action in ops:
        typ = action["op"]
        if typ == "match":
            applied.append({"op": "match", "pos": action["pos"], "char": action["char"]})
            transformations.append("".join(cur))
        elif typ == "substitute":
            p = action["pos"]
            if 0 <= p < len(cur):
                old = cur[p]
                cur[p] = action["to"]
                applied.append({"op": "substitute", "pos": p, "from": old, "to": action["to"]})
            else:
                applied.append({"op": "substitute", "pos": p, "from": None, "to": action["to"]})
            transformations.append("".join(cur))
        elif typ == "delete":
            p = action.get("pos", 0)
            if 0 <= p < len(cur):
                removed = cur.pop(p)
                applied.append({"op": "delete", "pos": p, "char": removed})
            else:
                applied.append({"op": "delete", "pos": p, "char": None})
            transformations.append("".join(cur))
        elif typ == "insert":
            p = action["pos"]
            if p < 0: p = 0
            if p > len(cur): p = len(cur)
            cur.insert(p, action["char"])
            applied.append({"op": "insert", "pos": p, "char": action["char"]})
            transformations.append("".join(cur))
        else:
            transformations.append("".join(cur))
    return applied, transformations


def print_summary(applied: List[Dict[str, Any]], transformations: List[str]) -> None:
    """Nicely print key parts of the result."""
    pp = pprint.PrettyPrinter(width=120, compact=False)
    # compute edit distance as number of non-match operations
    edit_ops = [op for op in applied if op.get("op") in ("insert", "delete", "substitute")]
    print("\nHirschberg alignment summary")
    print("============================")
    print("Edit distance:", len(edit_ops))
    print("\nStep-by-step transformations (initial -> ... -> target):")
    for idx, s in enumerate(transformations):
        print(f"  [{idx:2d}] {s}")
    print("\nOperations applied (in order):")
    pp.pprint(applied)

def main(argv: List[str] = None) -> int:
    """accepts two strings as input() and prints result.
    Returns exit code 0 on success.
    """
    if argv is None:
        argv = sys.argv[1:]

    if len(argv) >= 2:
        S = argv[0]
        T = argv[1]
    else:
        S = input("Enter source string S: ")
        T = input("Enter target string T: ")

    applied, transformations = hirschberg_with_log(S, T)
    print_summary(applied, transformations)
    return 0

if __name__ == "__main__":
    print("=== Hirschberg Edit/Alignment (log) ===\n")
    main()

