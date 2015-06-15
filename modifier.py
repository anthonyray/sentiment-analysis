import csv

"""
Filter functions
"""

def is_empty_line(line):
    return line.startswith('\t')

def is_comment(line):
    return line.startswith('#')

def iter_filtered(in_file,*filters):
    for line in in_file:
        if not any(fltr(line) for fltr in filters):
            yield line


"""
Negating Word Reader class
"""

class ModifierWordReader:

    def __init__(self,filename):
        self.filename = filename
        self.words = list()
        self.parse_file()

    def parse_file(self):
        f = open(self.filename, 'rt')
        try:
            iter_clean = iter_filtered(f, is_comment,is_empty_line)
            reader = csv.reader(iter_clean)
            for row in reader:
                line = row[0].split('\t')
                self.words.append(line[0])
        finally:
            f.close()

    def has_modifier(self,w):
        if w in self.words:
            return True
        else:
            return False




if __name__ == '__main__':
    nwr = ModifierWordReader('BoosterWordList.txt')
