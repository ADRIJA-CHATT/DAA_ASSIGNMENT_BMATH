# Load data
df <- read.csv("C:/Users/ADRIJA/OneDrive/Documents/SARS COV 2 VARIANTS.csv", stringsAsFactors = FALSE)

variants <- df$Variant
genomes <- df$Genome
n <- length(variants)
dist_matrix <- matrix(0, n, n, dimnames = list(variants, variants))

# Two-row Wagner–Fischer
wagner_fischer_two_row <- function(a, b) {
  if (nchar(a) < nchar(b)) {
    tmp <- a; a <- b; b <- tmp
  }
  m <- nchar(a); n <- nchar(b)
  prev <- 0:n
  for (i in seq_len(m)) {
    curr <- integer(n + 1)
    curr[1] <- i
    for (j in seq_len(n)) {
      cost <- ifelse(substr(a, i, i) == substr(b, j, j), 0, 1)
      curr[j + 1] <- min(
        prev[j + 1] + 1,
        curr[j] + 1,
        prev[j] + cost
      )
    }
    prev <- curr
  }
  return(prev[n + 1])
}

# Compute normalized distances
for (i in seq_len(n)) {
  for (j in seq_len(n)) {
    if (i < j) {
      d <- wagner_fischer_two_row(genomes[i], genomes[j])
      dist_matrix[i, j] <- d / (nchar(genomes[i]) + nchar(genomes[j]))
    }
  }
}
for(i in seq_len(n)){
  for(j in seq_len(n)){
    if(i>j){
      dist_matrix[i,j]<-dist_matrix[j,i]
    }
  }
}
write.csv(dist_matrix, "SARS_COV_2_Variant_Distance_Matrix_R.csv", row.names = TRUE)
