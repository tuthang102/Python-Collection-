# Author: Thang Tran( tuthang102@gmail.com)

import os
import re
import matplotlib.pylab as plt
import tempfile
import random as rd
import string
import shutil

home = os.path.expanduser("~")
root_dir = os.path.join(home, 'Desktop\AppleTest') # Set the whatever directory you want

# This function finds the keywords in each file


def find_keyword(root_dir, keyword):
    counts = dict()
    for dirpath, dirs, files in os.walk(root_dir):
        for file in files:
            path = os.path.join(dirpath, file)
            data = open(path, 'r')
            counts[path] = 0
            for line in data:
                line = line.strip()
                num = re.findall(keyword, line)
                counts[path] += len(num)
            data.close()
    return counts

# This function plots the result


def plot(counts):
    plt.figure(1)
    plt.title('Counted Values Plot')
    x = plt.array(range(len(counts)))
    y = plt.array(list(counts.values()))
    xticks = list(counts.keys())
    plt.xticks(x, xticks, rotation='vertical')
    plt.plot(x, y, 'ro')
    plt.xlabel('Subdir Name')
    plt.ylabel('Count Values')
    plt.subplots_adjust(bottom=0.5)
    plt.show()

# This function creates temporary files with the keywords in them for testing


def file_creation(path, keyword):
    letters = string.ascii_letters  # a string contains all upper and lower case letters
    puns = string.punctuation  # a string contains punctuationS
    os.chdir(path)
    true_counts = dict()
    for k in range(rd.randrange(1, 5)):
        fp = tempfile.NamedTemporaryFile(mode='w+t', dir=os.getcwd(), delete=False)
        total = 0
        for j in range(rd.randrange(1, 20)):
            rand1 = rd.randrange(0, 5)
            rand2 = rd.randrange(0, 5)
            fp.write(letters[rd.randrange(0, len(letters))] + puns[rd.randrange(0, len(puns))] +
                    keyword * rand1 + str(rd.randrange(100, 200)) + letters[rd.randrange(0, len(letters))] +
                    keyword * rand2 + puns[rd.randrange(0, len(puns))] + '\n' * rd.randrange(0, 3))
            total += rand1 + rand2
        true_counts[fp.name] = total
    return true_counts

# This function creates a tree of directory starting from root_dir and return a dict of true counts


def tree_files(num_of_files):
    true_counts = dict()
    for i in range(num_of_files):
        sub_name = 'sub' + str(i)
        os.mkdir(sub_name)
        os.chdir(os.path.join(os.getcwd(), sub_name))
        if i > 1:
            true_counts.update(file_creation(os.getcwd(), 'Apple'))
    return true_counts


if __name__ == '__main__':
    # Start creating temporary files with keyword in each of them
    true_counts = tree_files(5)

    # Use the function find_keyword on the files just created
    test_counts = find_keyword(root_dir, '(Apple)')

    # Delete all the files that are not part of the testing process in the test_counts dictionary
    for key, val in test_counts.copy().items():
        if key not in true_counts:
            del test_counts[key]

    # Now check to see if true_counts == test_counts
    print('True counts:', true_counts)
    print()
    print('Test counts:', test_counts)
    print()
    print('Compare the two dictionaries give:', true_counts == test_counts)

    # Plot the result
    plot(find_keyword(root_dir, '(Apple)'))

    # Uncomment the 2 lines below and comment everything else in the main part to delete all the created test folder

    # os.chdir(root_dir)
    # shutil.rmtree(os.path.join(os.getcwd(), 'sub0'))