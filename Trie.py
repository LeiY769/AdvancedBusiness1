import string
import os
import random
import sys
import time
import matplotlib.pyplot as plt

class TrieNode:
    def __init__(self, char):
        self.char = char
        self.is_end = False
        self.counter = 0
        self.children = {}

class Trie(object):
    def __init__(self):
        self.root = TrieNode("")
        self.greatest = [{'key': "", 'value': -1} for i in range(10)]
    
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

        found = 0
        for d in self.greatest:
            if word == d['key']:
                d['value'] += 1
                found = 1

        minimum = min(self.greatest, key=lambda x: x['value'])
        if node.counter > minimum['value'] and found == 0:
            min_index = self.greatest.index(minimum)
            self.greatest[min_index] = {'key': word, 'value': node.counter}
    
    def search(self, word):
        node = self.root

        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                return 0
            
        return node.counter
    
    def gettop10(self):
        return self.greatest
    
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
    if nb_files <= 0:
        print("[ERROR] - Usage: python Trie.py (positive integer that represents the number of files to read)")
        sys.exit()

    t = Trie()
    for i in range(nb_files):
        random_file = random.choice(files)
        with open(os.path.join(directory_path, random_file), "r") as file:
            for line in file:
                line = line.strip()
                line = line.lower()
                line = line.translate(line.maketrans("", "", string.punctuation))
                for word in line.split(" "):
                    if word != "":
                        t.insert(word)

    top10 = t.gettop10()
    top10_values = []
    top10_words = []

    for item in top10:
        top10_words.append(item['key'])
        top10_values.append(item['value'])

    end_T_time = time.time()
    total_time = end_T_time - start_time
    print("-------------------------")
    print("Total time for Trie:", total_time, "seconds for", nb_files, "files.")

    labels = [f"{word} ({value})" for word, value in zip(top10_words, top10_values)]
    plt.pie(top10_values, labels=labels, autopct='%1.1f%%')
    plt.title("Pie Chart for the 10 most frequent words")
    end_time = time.time()
    total_time = end_time - end_T_time
    print("Total time to get the 10 most frequent words and display the chart:", total_time, "seconds.")
    print("-------------------------")
    plt.show()
