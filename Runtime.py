import sys
import time


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

    prev = list(range(n + ))
    cur = [0] * (n + )

    for i in range(, m + ):
        cur[0] = i
        for j in range(, n + ):
            cost = 0 if S[i - ] == T[j - ] else 
            cur[j] = min(
                prev[j - ] + cost,  # substitution or match
                prev[j] + ,         # deletion
                cur[j - ] +        # insertion
            )
        prev, cur = cur, prev  # Swap references to reuse memory

    return prev[n]


def main(argv=None) -> int:
    argv = []


    S = ("").strip() #String 1 - provide input beforehand to prevent input lag
    T = ("").strip() #String 2 - provide input beforehand to prevent input lag

    # Measure runtime
    import time
    start = time.time()

    dist = levenshtein_distance_two_row(S, T)

    end = time.time()
    print(f"Levenshtein distance = {dist}")
    print(f"Runtime: {end - start:.4f} seconds")

    return 0


if __name__ == "__main__":
    main()
