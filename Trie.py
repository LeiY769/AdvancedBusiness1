class TrieNode:
    def __init__(self, char):
        self.char = char
        self.is_end = False
        self.counter = 0
        self.children = {}

class Trie(object):
    def __init__(self):
        self.root = TrieNode("")
    
    def insert(self, word):
        node = self.root
        
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                new_node = TrieNode(char)
                node.children[char] = new_node
                node = new_node
        
        node.is_end = True
        node.counter += 1
    
    def search(self, word):
        node = self.root

        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                return 0
            
        return node.counter
    
    def printtrie(self):
        self.dfstrie(self.root, "")
    
    def dfstrie(self, node, prefix):
        if node.is_end:
            print(prefix + node.char, node.counter)
        
        for child in node.children.values():
            self.dfstrie(child, prefix + node.char)
    
t = Trie()
with open("Task1/datasetCNNSTORIES/0a0a4c90d59df9e36ffec4ba306b4f20f3ba4acb.story","r") as file:
    for line in file:
        for word in line.split():
            t.insert(word)

t.printtrie()
