class Bird:
    def sound(self):
        print("Some sound")

class Parrot(Bird):
    def sound(self):
        print("Parrot speaks")

class Crow(Bird):
    def sound(self):
        print("Crow caws")

p = Parrot()
c = Crow()

p.sound()
c.sound()