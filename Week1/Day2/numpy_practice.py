import numpy as np

# # printing array
# arr1=np.array([1,2,3,4,5,6,7,8,9,10])
# print(arr1)

# # printing sum and mean
# total=np.sum(arr1)
# avg=np.mean(arr1)(
# print("sum is:",total)
# print("avg is:",avg)

# # printing even numbers
# arr2=np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
# for num in arr2:
#     if num%2==0:
#         print(num)

# # Squaring elements
# square=arr1**2
# print(square)


# arr3=arr2.reshape(5,4)
# print(arr3)

# arr4=np.random.randint(1,10,5)
# print(arr4)

# arr5=np.dot(arr4,arr3)
# print(arr5)

# Student Marks
marks = [
    [85, 78, 92],
    [70, 88, 80],
    [90, 95, 85],
    [60, 65, 70],
    [75, 85, 90]
]
marks=np.array(marks)
print("List is: \n",list(marks))
avg_per_student=np.mean(marks,axis=1)

avg=np.mean(marks)
print(avg)

result=marks[avg_per_student>80]
print(result)

A1=marks[avg_per_student>90]
print(A1)




    