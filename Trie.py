import string
import os
import random
import sys
import time

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
        if node.is_end and prefix + node.char != "":
            print(prefix + node.char, node.counter)
        
        for child in node.children.values():
            self.dfstrie(child, prefix + node.char)


if __name__ == '__main__':
    start_time = time.time()

    directory_path = "Task1/datasetCNNSTORIES"
    file_extension = ".story"
    files = [f for f in os.listdir(directory_path) if f.endswith(file_extension)]

    nb_files = int(sys.argv[1])
    random_nb = random.randint(0, nb_files-1)

    for i in range(nb_files):
        t = Trie()
        random_file = random.choice(files)
        with open(os.path.join(directory_path, random_file), "r") as file:
            for line in file:
                line = line.strip()
                #line = line.lower()
                line = line.translate(line.maketrans("", "", string.punctuation))
                for word in line.split(" "):
                    t.insert(word)

        if i == random_nb:
            print("WordCount for the file", random_file)
            t.printtrie()

    end_time = time.time()
    total_time = end_time - start_time
    print("Total time:", total_time, "seconds for", nb_files, "files.")
