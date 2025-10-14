import sys

def ukkonen_levenshtein(a: str, b: str, k: int) -> int | None:
    """
    Compute Levenshtein distance up to threshold k using Ukkonen's algorithm.
    Returns the distance if <= k, else None.
    """
    m, n = len(a), len(b)

    # rejection
    if abs(m - n) > k:
        return None

    prev = list(range(min(n, k) + 1))
    curr = [0] * (n + 1)

    INF = k + 1

    for i in range(1, m + 1):
        low = max(1, i - k)
        high = min(n, i + k)

        curr[0] = i if low == 1 else INF

        for j in range(low, high + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1

            deletion = prev[j] + 1 if j < len(prev) else INF
            insertion = curr[j - 1] + 1
            substitution = prev[j - 1] + cost if j - 1 < len(prev) else INF

            curr[j] = min(deletion, insertion, substitution)

        # Early termination
        if min(curr[low:high + 1]) > k:
            return None

        prev, curr = curr, [INF] * (n + 1)

    return prev[n] if prev[n] <= k else None


def main(argv=None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    if len(argv) >= 3:
        a, b, k = argv[0], argv[1], int(argv[2])
    else:
        a = input("Enter string a: ").strip()
        b = input("Enter string b: ").strip()
        k = int(input("Enter threshold k: ").strip())

    dist = ukkonen_levenshtein(a, b, k)

    if dist is None:
        print(f"No alignment within distance {k}.")
        return 1
    else:
        print(f"Levenshtein distance = {dist}")
        return 0


if __name__ == "__main__":
    main()
