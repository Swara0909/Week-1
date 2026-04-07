# def cubes(n):

#     for x in range(n):
#         yield x**3
        
#     # result=[]
#     # for x in range(n):
#     #     result.append(x**3)
    
#     # return result

# # print(cubes(6))

# for x in cubes(6):
#     print (x) 

# print(list(cubes(6)))

# # We can use yield to get same output without making list to store memory


# def fib(n):

#     a=1
#     b=1
#     for x in range(1,n):

#         yield a
#         a,b=b,a+b

# for x in fib(10):
#     print(x)

# g=fib(10)
# print(next(g))

# print(next(g))
# print(next(g))

# This iterates over str but does not predict next letter so we use genertaor func
# that is iter()

name = "Swara"

# for x in name:
#     print(x)

s_iter = iter(name)
print(next(s_iter))  
print(next(s_iter)) 
print(next(s_iter)) 
