"""
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('main')
"""
import csv

results = []
with open('test.csv', newline='') as inputfile:
    for row in csv.reader(inputfile):
        results.append(row[0])

print(results)