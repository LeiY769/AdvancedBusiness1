
LIMIT = 0.7


class Node:
    def __init__(self, key, data):
        self.key = key
        self.data = data
        self.value = 0
        self.next = None

    def node_key(self):
        return self.key

    def node_data(self):
        return self.data

    def node_value(self):
        return self.value
    def addnode_key(self, key):
        self.key = key

    def addnode_data(self, data):
        self.data = data

    def addnode_value(self):
        self.value = self.value + 1
    def set_value(self,value):
        self.value = value

    def node_next(self):
        return self.next

class Dict:
    def __init__(self):
        self.size = 20
        self.nbKeys = 0
        self.array = [None] * self.size

    def hashing(self,key):
        length = len(key)
        sum = 0
        base = 1
        mod = 1000000007
        for i in range(length):
            sum = (sum + base * ord(key[i])) % mod
            base = (base * 256) % mod
        return sum

    def nb_keys(self):
        return self.nbKeys
    
    def get_size(self):
        return self.size

    def get(self, key):
        n = self.array[self.hashing(key) % self.size]
        while n and n.node_key() != key:
            n = n.node_next()
        return n
    def contains(self, key):
        return self.get(key) != None
    def resize(self):
        old_size = self.size
        new_size = old_size * 2
        old_array = self.array
        new_array = [None] * new_size

        self.nbKeys = 0
        self.array = new_array
        self.size = new_size
        for i in range(old_size):
            a = old_array[i]
            while a:
                b = a.next
                self.insert2(a.key, a.data,a.value)
                del a.key
                del a
                a = b
        del old_array
    def insert2(self,key,data,value):
        n = self.get(key)

        if n: # Si n est deja présent on va alors en ajouter 1
            n.addnode_value()
        else:
            i = self.hashing(key) % self.size

            n = Node(key, data)
            n.set_value(value)
            n.next = self.array[i]
            self.array[i] = n
            self.nbKeys += 1

    def insert(self, key, data):
        nb_keys = self.nb_keys()
        size_hash = self.zize()
        percentage = nb_keys / size_hash

        if percentage > 0.7:
            self.resize()
        
        n = self.get(key)

        if n: # Si n est deja présent on va alors en ajouter 1
            n.addnode_value()
        else:
            i = self.hashing(key) % self.size

            n = Node(key, data)
            n.addnode_value()
            n.next = self.array[i]
            self.array[i] = n
            self.nbKeys += 1

car = Dict()
def sortLetter(input):
        return ''.join(sorted(input))
car.insert("aab","baa")
car.insert("aab","aba")
car.insert("erz","zer")
car.insert("c", "c")
print(car.nb_keys())
car.insert("aab","baa")

test = []
with open('english.txt','r') as file:
  
    # reading each line   
    for line in file:
  
        # reading each word       
        for word in line.split():
  
            # displaying the words          
            test.append(word)
print(test)
for i in range(100):
    tempo =test.pop()
    car.insert(sortLetter(tempo),tempo)

for i in range(car.zize()):
    n = car.array[i]
    while n:
        print(f"{n.data}: {n.value}")
        n = n.next


