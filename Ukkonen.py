import sys

def ukkonen_levenshtein(a: str, b: str, k: int) -> int | None:
    """
    Compute Levenshtein distance between strings a and b up to a threshold k
    using Ukkonen's banded algorithm.
    Returns the distance if it is <= k, else returns None.
    """
    m, n = len(a), len(b)

    # Quick rejection: if length difference exceeds threshold, distance > k
    if abs(m - n) > k:
        return None

    # Initialize previous row of DP table (only within band [0..k])
    prev = list(range(min(n, k) + 1))
    # Current row (initialized later in loop)
    curr = [0] * (n + 1)

    # Infinite value outside band
    INF = k + 1

    # Fill DP table row by row
    for i in range(1, m + 1):
        # Band limits for current row
        low = max(1, i - k)
        high = min(n, i + k)

        # Initialize first column of current row (only valid if low == 1)
        curr[0] = i if low == 1 else INF

        # Compute DP only inside the band [low..high]
        for j in range(low, high + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1

            # Calculate cost for deletion, insertion, substitution
            deletion = prev[j] + 1 if j < len(prev) else INF
            insertion = curr[j - 1] + 1
            substitution = prev[j - 1] + cost if j - 1 < len(prev) else INF

            # Choose minimum
            curr[j] = min(deletion, insertion, substitution)

        # Early termination: if all costs in band > k, distance exceeds threshold
        if min(curr[low:high + 1]) > k:
            return None

        # Prepare for next iteration: swap rows, reset current row to INF
        prev, curr = curr, [INF] * (n + 1)

    # Return final distance if within threshold, else None
    return prev[n] if prev[n] <= k else None


def main(argv=None) -> int:
    """
    Main CLI interface.
    Accepts manual input
    """
    if argv is None:
        argv = sys.argv[1:]

    # Parse input from argv or interactive input
    if len(argv) >= 3:
        a, b, k = argv[0], argv[1], int(argv[2])
    else:
        a = input("Enter string a: ").strip()
        b = input("Enter string b: ").strip()
        k = int(input("Enter threshold k: ").strip())

    # Compute distance
    dist = ukkonen_levenshtein(a, b, k)

    # Output result
    if dist is None:
        print(f"No alignment within distance {k}.")
        return 1
    else:
        print(f"Levenshtein distance = {dist}")
        return 0


if __name__ == "__main__":
    main()
