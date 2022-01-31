class Tree():
    def __init__(self,name,height,diameter,talkative = False):
        self.name = name
        self.height = height
        self.diameter = diameter
        self.talkative = talkative
        
    def __str__(self):
        if self.talkative:
            t = ""
        else:
            t = "no"
        return "{} {} es un árbol parlante que mide {}cm de altura y {}cm de diámetro".format(self.name, t, self.height, self.diameter)
        
    def talk(self, message):
        if self.talkative:
            print(message)
        else:
            print("Este árbol no es parlante")
            
    def grow(self, add_height = 0,add_diameter = 0):
        self.height += add_height
        self.diameter += add_diameter
        
        
trees = []


def born_tree(tree_object):
    trees.append(tree_object)
    print("{} acaba de nacer".format(tree_object.name))
    print(tree_object)
    
def dead_tree(tree_object):
    if tree_object in trees:
        trees.remove(tree_object)
        print("Descansa en paz", tree_object.name)
    else:
        print("El árbol {} no está en la lista".format(tree_object.name))