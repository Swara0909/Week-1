# Types of Functions in Python:

# 1. User Defined Functions
# 2. Built-in Functions    

# Based on arguments and return type:

# 1. No arguments and no return type
def greet():
    print("Hello")

greet()


# 2. No arguments and return type
def sumofnos():
    return 10

print(sumofnos())


# 3. Arguments and No return type
def sumofnos(a, b):
    print(a + b)

sumofnos(4, 5)


# 4. Arguments and return type
def sumofnos(a, b):
    return a + b

ans = sumofnos(4, 5)
print(ans)


# Types of Arguments

# 1. Positional Arguments
def add(a, b):
    return a + b

print(add(2, 3))


# 2. Keyword Arguments
def add_nos(c, d):
    return c + d

print(add_nos(c=5, d=3))


# 3. Default Arguments
def greet(name="Guest"):
    print(name)

greet()
greet("Swara")


# 4. Variable-length Arguments

# *args
def total(*numbers):
    print("Numbers:", numbers)
    print("Sum:", sum(numbers))

total(1, 2, 3, 4)


# **kwargs
def details(**info):
    print("Details:", info)

details(name="Swara", age=21, city="Surat")