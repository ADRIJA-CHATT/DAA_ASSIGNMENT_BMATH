# DAA_ASSIGNMENT_BMATH  
Calculating the Levenshtein Distance between any two strings using multiple algorithms & analysing their space and time complexities  

![Python 3+](https://img.shields.io/badge/Python-3%2B-blue?logo=python&logoColor=white)
![License: GPL v3](https://img.shields.io/badge/License-GPLv3-green.svg)


##  Project Overview  
This project implements and analyses the problem of computing the **Levenshtein distance** (edit distance) between two strings, using the following algorithms:  
- Wagner–Fischer algorithm  
- Hirschberg’s algorithm  
- Ukkonen’s algorithm  

The aim is to compare these methods in terms of performance (time complexity), memory usage (space complexity) and practicality when applied to strings of different lengths and from various language corpora.

##  Repository Contents  
Here’s a quick rundown of the key files and folders:

- `WagnerFischer.py` — Implementation of the standard Wagner–Fischer algorithm.  
- `TwoRowWagnerFischer.py` — Optimised version of Wagner–Fischer using only two rows of matrix storage.  
- `Hirschberg.py` — Implementation of Hirschberg’s algorithm (divide‑and‑conquer) to reduce space usage.  
- `Ukkonen.py` — Implementation of Ukkonen’s algorithm (banded dynamic programming) for efficient approximate string matching.  
- `main.py` — Driver script to run the algorithms, compare results and measure performance.  
- `requirements.txt` — List of Python package dependencies required by the project.  
- Language corpora `.csv` files (e.g., `Hindi‑Corpus.csv`, `Marathi‑Corpus.csv`, `Tamil‑Corpus.csv`, etc) used for testing/benchmarking string pairs.  
- Additional scripts (e.g., `Spell_Correction.py`) and R variants (`SARS‑COV2_HEATMAP.R`, `SARS‑COV2_dist.R`) for specific experiments.  
- `LICENSE` — Licensed under the **GNU GPL v3**.  

##  Getting Started  
### Prerequisites  
- Python 3.x  
- Standard libraries: `typing`, `pprint`, `sys`  
- Install dependencies via `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Running the project  
1. Clone the repository:
   ```bash
   git clone https://github.com/ADRIJA-CHATT/DAA_ASSIGNMENT_BMATH.git
   cd DAA_ASSIGNMENT_BMATH
   ```

2. Run the main driver script:
   ```bash
   python main.py
   ```
   ***PS: Do not forget to change the location of the corresponding datast if you are willing to use it.***
##  Analysis  
- **Time complexity:** $\Theta(nm)$ for Wagner–Fischer, lower for approximate/bounded methods.  
- **Space complexity:** reduced in two‑row and Hirschberg’s versions.  
- **Correctness:** all algorithms yield identical edit distance results.  
- **Scalability:** Ukkonen’s algorithm performs best when edit distance is small.  

##  Applications  
Edit distance computation is vital in spell checking, DNA sequence alignment, NLP, and data cleaning.  
This project highlights algorithmic design trade‑offs and performance scaling with input size and script.

##  Insights  
- Wagner–Fischer: $\Theta(nm)$ time and space.  
- Two‑Row: $\Theta(\min(n,m))$ space.  
- Hirschberg: $\mathcal{O}(n + m)$ output space (divide‑and‑conquer).  
- Ukkonen: best for small edit bounds.  

##  Licence  
Released under **GNU GPL v3**.  
You may use, modify, and redistribute under the same license.

##  Contact & Contribution  
- **Author:** Adrija Chatterjee, Suryansh Shirbhate
- Contributions are welcome — performance improvements, corpus additions, or visual analytics are encouraged!
