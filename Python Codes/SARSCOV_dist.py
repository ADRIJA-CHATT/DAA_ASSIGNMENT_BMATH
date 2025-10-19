import pandas as pd
import numpy as np

# ---------- Step 1: Read Data ----------
df = pd.read_csv("C:/Users/ADRIJA/OneDrive/Documents/SARS-COV 2 VARIANTS.csv")

# Assuming columns are named "Variant" and "Full_Genome"
variants = df["Variant"].tolist()
genomes = df["Genome"].tolist()

n = len(variants)
matrix = np.zeros((n, n))

# ---------- Step 2: Two-row Wagner–Fischer Algorithm ----------
def wagner_fischer_two_row(a: str, b: str) -> int:
    """Compute Levenshtein distance using O(min(len(a), len(b))) space."""
    if len(a) < len(b):
        a, b = b, a  # ensure a is the longer string
    prev = list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        curr = [i] + [0] * len(b)
        for j in range(1, len(b) + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            curr[j] = min(prev[j] + 1, curr[j - 1] + 1, prev[j - 1] + cost)
        prev = curr
    return prev[-1]

# ---------- Step 3: Compute Normalized Distance Matrix ----------
for i in range(n):
    for j in range(n):
        if i == j:
            matrix[i, j] = 0.0
        else if i<j:
            d = wagner_fischer_two_row(genomes[i], genomes[j])
            matrix[i, j] = d / (len(genomes[i]) + len(genomes[j]))
for i in range(n):
    for j in range(i):
        matrix[i,j]=matrix[j,i]
# ---------- Step 4: Create and Save Matrix ----------
distance_df = pd.DataFrame(matrix, index=variants, columns=variants)
distance_df.to_csv("Variant_Distance_Matrix.csv", index=True)

print(distance_df)
