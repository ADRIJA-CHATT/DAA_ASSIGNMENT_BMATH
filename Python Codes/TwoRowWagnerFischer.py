import sys

def levenshtein_distance_two_row(S: str, T: str) -> int:
    """
    Compute the Levenshtein distance between strings S and T
    using the two-row optimization (space-efficient version).
    
    Time Complexity: O(mn)
    Space Complexity: O(min(m, n))
    """
    m, n = len(S), len(T)

    # Ensure T is the shorter string to minimize memory usage
    if n > m:
        S, T = T, S
        m, n = n, m

    # prev: previous row of DP table
    prev = list(range(n + 1))  # base case: distance from empty string
    cur = [0] * (n + 1)        # current row being computed

    # Iterate over each character in S
    for i in range(1, m + 1):
        cur[0] = i  # cost of deleting all characters from S[:i] to match empty T
        for j in range(1, n + 1):
            cost = 0 if S[i - 1] == T[j - 1] else 1
            # Compute minimal cost among substitution/match, deletion, insertion
            cur[j] = min(
                prev[j - 1] + cost,  # substitution or match
                prev[j] + 1,         # deletion
                cur[j - 1] + 1       # insertion
            )
        # Swap rows for next iteration to reuse memory
        prev, cur = cur, prev

    # Final distance is in the last element of prev (after swap)
    return prev[n]


def main(argv=None) -> int:
    """
    Main function to read strings and compute distance.
    Always takes input manually in this version.
    """
    # Ignore command-line args if running in Jupyter / interactive
    argv = []  

    # Take string inputs manually
    S = input("Enter first string: ").strip()
    T = input("Enter second string: ").strip()

    # Compute distance
    dist = levenshtein_distance_two_row(S, T)

    # Print both absolute and normalized Levenshtein distance
    print(f"Levenshtein distance = {dist}")
    print(f"Normalized Levenshtein distance = {dist / (len(S) + len(T))}")
    return 0


if __name__ == "__main__":
    main()
