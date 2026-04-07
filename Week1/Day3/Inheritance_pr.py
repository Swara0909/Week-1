class Animal():

    def __init__(self):
        print("Animal Created")
    
    def eat(self):
        print("Animal eats")

    def walks(self):
        print("Animal walks")

class Dog(Animal):

    def __init__(self):
        Animal.__init__(self)
        print("Dog Created")

    def walks(self):
        print("Dog Walks")

my_animal=Animal()
my_animal.eat()

my_dog=Dog()
my_dog.walks()

