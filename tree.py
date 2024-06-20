class Tree:
    def __init__(self, value):
        self.value=value
        self.children=[]

    # @staticmethod
    def add_children(self, child):
        self.children.append(child)
        return self.children

node1=Tree('node1')
node2=Tree('node2')

print(node1.add_children(node1))
# print(node_test)
