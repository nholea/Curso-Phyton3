import math

class Vector2D(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y 
        
    @property
    def module(self):
        return math.sqrt((self.x ** 2) + (self.y ** 2))
        
    def scalar_prod(self, num = 1):
        self.x *= num
        self.y *= num
        
    def __str__(self):
        return "({}, {})".format(self.x, self.y)
        
    @classmethod
    def sum(cls, v1 ,v2):
        return cls(v1.x + v2.x, v1.y + v2.y)
        
    @classmethod
    def subtract(cls, v1 ,v2):
        return cls(v1.x - v2.x, v1.y - v2.y)
        
    @staticmethod
    def dot_product(v1, v2):
        return v1.x*v2.x + v1.y*v2.y
        
    @classmethod
    def distance(cls, v1, v2):
        return cls.subtract(v1,v2).module
        
    def extend_to_3D(self, z =0):
        return Vector3D(self.x, self.y, z)
        
        
        
class Vector3D(Vector2D):
    def __init__(self,x,y,z):
        super().__init__(x,y)
        self.z = z
        
    def __str__(self):
        return super().__str__()[:-1] + ",{})".format(self.z)
        
    @property
    def module(self):
        return math.sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))
    def scalar_prod(self, num = 1):
        super().scalar_prod(num)
        self.z *=num
        
    @classmethod
    def sum(cls, v1 ,v2):
        return cls(v1.x + v2.x, v1.y + v2.y, v1.z + v2.z)
        
    @classmethod
    def subtract(cls, v1 ,v2):
        return cls(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z)
        
    @staticmethod
    def dot_product(v1, v2):
        return super().dot_product(v1,v2) + v1.z*v2.z
        
    @classmethod
    def distance(cls, v1, v2):
        return cls.subtract(v1,v2).module
        
    @classmethod 
    def zero(cls):
        cls(0, 0, 0)
        
    @classmethod 
    def horizontal(cls):
        cls(1, 0, 0)
        
    @classmethod 
    def vertical(cls):
        cls(0, 1, 0)
        
    @classmethod 
    def forward(cls):
        cls(0, 0, 1)
        
        
        
        
        
        
        
        
        
    
    
        
        
        