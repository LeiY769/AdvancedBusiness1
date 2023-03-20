from mrjob.job import MRJob
import string

class WordCount(MRJob):

    def mapper(self, _, line):
        line = line.strip()
        #line = line.lower()
        line = line.translate(line.maketrans("", "", string.punctuation))
        for word in line.split(" "):
            if len(word) > 0:
                yield(word, 1)

    def reducer(self, word, counts):
        yield(word, sum(counts))

if __name__ == '__main__':
    WordCount.run()
    """task = WordCount(args = [])
    with open("Task1/datasetCNNSTORIES/0a0a4c90d59df9e36ffec4ba306b4f20f3ba4acb.story","r") as file:
        output = list(mr.runJob(file, task))"""
