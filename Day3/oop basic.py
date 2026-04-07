class Dog():

    species = "mammal"
    def __init__(self,breed,name,spots):
        self.breed=breed
        self.name=name
        self.spots=spots
    

    def bark(self,number):
        print("Woof! My name is {} and the number is {}".format(self.name,number))

my_dog=Dog(breed="Lab", name="Sheru",spots=False)

print(type(my_dog))
print(Dog.species)
print(my_dog.breed)

my_dog.bark(10)
