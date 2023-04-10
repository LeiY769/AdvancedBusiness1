import random
import sys
import os
import time
import subprocess
import matplotlib.pyplot as plt

if __name__ == '__main__':
    start_time = time.time()

    directory_path = "Task1/datasetCNNSTORIES"
    file_extension = ".story"
    files = [f for f in os.listdir(directory_path) if f.endswith(file_extension)]

    nb_files = int(sys.argv[1])
    input_files = random.sample(files, nb_files)
    for i in range(len(input_files)):
        input_files[i] = os.path.join(directory_path, input_files[i])

    cmd = ['python', 'WordCount.py'] + input_files
    with open("output_file", 'w') as outfile:
        subprocess.run(cmd, stdout=outfile)

    end_MR_time = time.time()
    total_time = end_MR_time - start_time
    print("-------------------------")
    print("Total time for MapReduce:", total_time, "seconds for", nb_files, "files.")

    with open("output_file", 'r') as outfile:
        lines = outfile.readlines()

    sorted_lines = sorted(lines, key=lambda line: int(line.strip().split("\t")[1]), reverse=True)

    with open("output_file", "w") as outfile:
        outfile.writelines(sorted_lines)

    with open("output_file", "r") as outfile:
        top10_words = []
        top10_values = []
        for i in range(10):
            line = outfile.readline()
            word, count = line.split()
            count = int(count)
            top10_words.append(word)
            top10_values.append(count)

        plt.pie(top10_values, labels=top10_words, autopct='%1.1f%%')
        plt.title("Pie Chart for the 10 most frequent words")
        plt.show()

    end_time = time.time()
    total_time = end_time - end_MR_time
    print("Total time to get the 10 most frequent words and display the chart:", total_time, "seconds.")
    print("-------------------------")
