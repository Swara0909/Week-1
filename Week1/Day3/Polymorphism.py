class dog():

    def __init__(self,name):
        self.name=name

    def speaks(self):
        return self.name + " Woof"

class cat():

    def __init__(self,name):
        self.name=name

    def speaks(self):
        return self.name + " Meow"

my_animal=dog("Sheru")
animal=cat("Billu")
print(my_animal.speaks())
print(animal.speaks())

    
    