import csv
from pathlib2 import Path

class CSVwriter:
    def __init__(self, filename, directory, fields):
        self.filename = filename
        self.directory = directory
        self.filepath = directory + filename
        self.fields = fields
        self.check_is_file(self.filepath)

    def check_is_file(self, filepath):
        fh = Path(filepath)
        if not(fh.is_file()):
            Path(filepath).touch()

    def append(self, fields):
        with open(self.filepath, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fields)
            writer.writerow({self.fields[0]: fields[0], self.fields[1]: fields[1]})

'''
if __name__ == '__main__':
    writer = CSVwriter("stats.csv", "stat/", ['time', 'temprature'])
    writer.append(['10','29'])
    writer.append(['99','01'])
'''
