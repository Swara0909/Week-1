class Circle():

    pi=3.14

    def __init__(self, radius):
        self.radius=radius
        self.area=radius*radius*Circle.pi

    # Method

    def circumference(self):
        return self.radius*Circle.pi*2
    
my_circle=Circle(5)

print(my_circle.radius)
print(my_circle.area)
print(my_circle.circumference())