import csv


"""
Filters for the CSV file
"""
def is_empty_line(line):
    return line.startswith('\t')

def is_comment(line):
    return line.startswith('#')

"""
Filters aggregation
"""

def iter_filtered(in_file,*filters):
    for line in in_file:
        if not any(fltr(line) for fltr in filters):
            yield line

"""
Impedance adaptation for NLTK functions

"""

def nltk_impedance_adaptation(synset,pos):
    pound_index = synset.find('#')
    if pound_index > 0:
        return synset[:pound_index] + '.' + pos +'.' + format_number(int(synset[pound_index + 1:]))

def format_number(i):
    return "%02d" % i

"""
Classes of the SentiSynset
"""

class SentiSynset:
    def __init__(self,pos,id,PosScore,NegScore,Synset,Gloss):
        self.pos = pos
        self.id = id
        self.PosScore = PosScore
        self.NegScore = NegScore
        self.synset = Synset
        self.Gloss = Gloss

    def __repr__(self):
        return self.synset + ' PosScore: ' + str(self.PosScore) + ' NegScore: ' + str(self.NegScore)


class SentiWordNetCorpusReader:
    """
    This class parses a sentiwordnet file
    """

    def __init__(self,filename):
        self.filename = filename
        self.synsets = dict()
        self.parse()

    def parse(self):
        f = open(self.filename, 'rt')
        try:
            iter_clean = iter_filtered(f, is_comment,is_empty_line)
            reader = csv.reader(iter_clean)
            for row in reader:
                line = row[0].split('\t')
                for synset in line[4].split():
                    sentisynset = SentiSynset(line[0],
                                                line[1],
                                                float(line[2].strip()),
                                                float(line[3].strip()),
                                                nltk_impedance_adaptation(synset,line[0]),
                                                line[5])
                    self.synsets[nltk_impedance_adaptation(synset,line[0])] = sentisynset

        finally:
            f.close()

    def senti_synset(self,sentisynset):
        if self.synsets.has_key(sentisynset):
            return self.synsets[sentisynset]
        else:
            return None
