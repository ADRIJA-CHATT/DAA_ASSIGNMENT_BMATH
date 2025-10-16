import sys

def levenshtein_distance_two_row(S: str, T: str) -> int:
    """
    Compute the Levenshtein distance between strings S and T
    using the two-row optimization (space-efficient version).
    Time Complexity: O(mn)
    Space Complexity: O(min(m, n))
    """
    m, n = len(S), len(T)

    # Ensure T is the shorter string to minimize space
    if n > m:
        S, T = T, S
        m, n = n, m

    prev = list(range(n + 1))
    cur = [0] * (n + 1)

    for i in range(1, m + 1):
        cur[0] = i
        for j in range(1, n + 1):
            cost = 0 if S[i - 1] == T[j - 1] else 1
            cur[j] = min(
                prev[j - 1] + cost,  # substitution or match
                prev[j] + 1,         # deletion
                cur[j - 1] + 1       # insertion
            )
        prev, cur = cur, prev  # Swap references to reuse memory

    return prev[n]


def main(argv=None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    # Input from command line if given
    if len(argv) >= 2:
        S, T = argv[0], argv[1]
    else:
        S = input("Enter first string: ").strip()
        T = input("Enter second string: ").strip()

    dist = levenshtein_distance_two_row(S, T)
    print(f"Levenshtein distance between '{S}' and '{T}' = {dist}")
    return 0


def main(argv=None) -> int:
    argv = []  # ignore Jupyter’s internal command-line args

    # Always take input manually
    S = input("Enter first string: ").strip()
    T = input("Enter second string: ").strip()

    dist = levenshtein_distance_two_row(S, T)
    print(f"Levenshtein distance between '{S}' and '{T}' = {dist}")
    return 0


if __name__ == "__main__":
    main()
