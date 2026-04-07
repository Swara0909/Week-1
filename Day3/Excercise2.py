class Cylinder:
    
    pi=4.14

    def __init__(self,height=2,radius=3):
        self.height=height
        self.radius=radius
        
    def volume(self):
        return Cylinder.pi*self.radius*self.radius*self.height
    
    def surface_area(self):
        return 2*Cylinder.pi*self.radius*(self.radius+self.height)

area=Cylinder()
print(area.volume())
print(area.surface_area())