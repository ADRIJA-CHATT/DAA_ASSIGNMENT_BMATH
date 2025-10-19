# Load libraries
library(tidyverse)
library(viridis)
library(pheatmap)

# Read the CSV
df <- read.csv("C:/Users/ADRIJA/OneDrive/Documents/Variant_Distance_Matrix.csv", row.names = 1, check.names = FALSE)

# Replace Greek names with their symbols
greek_map <- c(
  "ALPHA" = "\u0391",   # Α
  "BETA" = "\u0392",    # Β
  "GAMMA" = "\u0393",   # Γ
  "DELTA" = "\u0394",   # Δ
  "EPSILO" = "\u0395",  # Ε (typo in file)
  "LAMBDA" = "\u039B",  # Λ
  "ETA" = "\u0397",     # Η
  "OMICRO" = "\u039F"   # Ο
)

# Function to replace Greek words in strings
replace_greek <- function(x) {
  for (name in names(greek_map)) {
    x <- gsub(name, greek_map[[name]], x)
  }
  return(x)
}

# Apply replacements to row and column names
rownames(df) <- replace_greek(rownames(df))
colnames(df) <- replace_greek(colnames(df))

# Convert to matrix
mat <- as.matrix(df)

# Generate a viridis heatmap
pheatmap(
  mat,
  color = viridis(100, begin = 0.5, end = 1.0), 
  cluster_rows = FALSE,
  cluster_cols = FALSE,
  display_numbers = TRUE,
  number_format = "%.3f",
  fontsize = 11,
  fontsize_number = 11,
  main = "Normalized Variant Distance Matrix (Levenshtein)",
  border_color = NA
)

