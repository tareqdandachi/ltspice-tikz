from enum import Enum

class LineStyle(Enum):
    solid  = 0
    dashed = 1
    dotted = 2


class Color:
    
    def __init__(self, p1=None, p2=None, p3=None, name=None) -> None:
        
        self.name = name if name else "Color"
        
        if type(p1)==str and p1[0] == "#" and p2 == None and p3 == None:
            self.color = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
            
        elif p1 != None and p2 != None and p3 != None:
            self.color = (p1, p2, p3)
            
        else:
            raise KeyError(f"You declared an instance of color incorrectly by specifying: \n{p1}, {p2}, {p3}")
        
    def hex(self):
        return '#%02x%02x%02x' % self.color
    
    def rgb(self): return self.color
    
    def r(self):   return self.color[0]
    def g(self):   return self.color[1]
    def b(self):   return self.color[2]

    def __str__(self) -> str:
        return "COLOR OBJECT: \t" + self.name + "\t\t" + self.hex() + "\t\t" + str(self.rgb())

class Colors(Enum):
    black = Color(0, 0, 0, name="Black")
    
    def __call__(self):
        return self.value