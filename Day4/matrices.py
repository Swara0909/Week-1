import numpy as np
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

# Matrix multiplication
print("Matrix multipliction:",np.dot(A, B))

# Scalar Multiplication
print("Scalar multiplication",3*A)

# Transpose
print("Transpose:",A.T)

# Determinant
print("Determinant", np.linalg.det(A))
print("Inversion:", np.linalg.inv(A))

C = np.array([[2, 1],
              [1, 3]])

D = np.array([5, 6])

X = np.linalg.solve(C, D)
print(X)

# Eigen Values and Vectors
A = np.array([[2, 0],
              [0, 3]])

vals, vecs = np.linalg.eig(A)

print("Eigenvalues:", vals)
print("Eigenvectors:\n", vecs)

# No of independent rows 
print(np.linalg.matrix_rank(A))

# Trace of matrix - Sum of diagonal
print(np.linalg.trace(A))

# Norm of a matrix
print(np.linalg.norm(A))

# Z-Score Normalization
data = np.array([10, 20, 30, 40, 50])

z = (data - np.mean(data)) / np.std(data)
print(z)