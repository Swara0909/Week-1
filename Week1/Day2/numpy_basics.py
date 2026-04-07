
import numpy as np

# 1. Create Arrays
arr = np.array([1, 2, 3, 4])
arr2 = np.array([[1, 2], [3, 4]])

print("1D Array:", arr)
print("2D Array:\n", arr2)

# 2. Properties
print("Shape:", arr.shape)
print("Size:", arr.size)
print("Data Type:", arr.dtype)

# 3. Special Arrays
print("Zeros:\n", np.zeros((2, 3)))
print("Ones:\n", np.ones((2, 2)))
print("Identity Matrix:\n", np.eye(3))

# 4. Range Functions
print("Arange:", np.arange(1, 10, 2))
print("Linspace:", np.linspace(0, 1, 5))

# 5. Indexing & Slicing
print("Element:", arr[1])
print("Slice:", arr[1:3])

# 6. Mathematical Operations
print("Add:", arr + 2)
print("Multiply:", arr * 2)
print("Square:", arr ** 2)

# 7. Aggregate Functions
print("Sum:", np.sum(arr))
print("Mean:", np.mean(arr))
print("Max:", np.max(arr))
print("Min:", np.min(arr))

# 8. Reshape
arr3 = np.array([1, 2, 3, 4, 5, 6])
print("Reshaped:\n", arr3.reshape(2, 3))

# 9. Random
print("Random:", np.random.rand(3))
print("Random Int:", np.random.randint(1, 10, 5))

# 10. Matrix Operations
a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])

print("Addition:\n", a + b)
print("Multiplication:\n", np.dot(a, b))

# 11. Boolean Filtering
arr4 = np.array([10, 20, 30, 40])
print("Filtered (>20):", arr4[arr4 > 20])


