""" Python exercise answers

:Author: Jonathan Karr <jonrkarr@gmail.com>
:Date: 2017-07-11
:Copyright: 2017, Karr Lab
:License: MIT
"""

#########################################
#########################################
# a function which computes the volume of a spherical cell with radius 1 :math:`\mu m`
import math


def volume(radius):
    return 4 / 3 * math.pi * radius ** 3
assert volume((3 / 4) ** (1 / 3)) == math.pi


#########################################
#########################################
# Write a function which uses if statements to return the type of a codon (start, stop, other)

def get_codon_type(codon):
    if codon in 'ATG':
        return 'start'
    elif codon in ['TAA', 'TAG', 'TGA']:
        return 'stop'
    else:
        return 'other'

assert get_codon_type('ATG') == 'start'
assert get_codon_type('TAG') == 'stop'
assert get_codon_type('CTT') == 'other'


#########################################
#########################################
# a class which represents RNA, with an attribute that stores the sequence
# of each transcript and a method which uses a dictionary to compute the
# amino acid sequence of the protein coded by the transcript


class Rna(object):
    TRANSLATION_TABLE = {
        'TTT': 'F',
        'TTC': 'F',
        'TTA': 'L',
        'TTG': 'L',
        'CTT': 'L',
        'CTC': 'L',
        'CTA': 'L',
        'CTG': 'L',
        'ATT': 'I',
        'ATC': 'I',
        'ATA': 'I',
        'ATG': 'M',
        'GTT': 'V',
        'GTC': 'V',
        'GTA': 'V',
        'GTG': 'V',
        'TCT': 'S',
        'TCC': 'S',
        'TCA': 'S',
        'TCG': 'S',
        'CCT': 'P',
        'CCC': 'P',
        'CCA': 'P',
        'CCG': 'P',
        'ACT': 'T',
        'ACC': 'T',
        'ACA': 'T',
        'ACG': 'T',
        'GCT': 'A',
        'GCC': 'A',
        'GCA': 'A',
        'GCG': 'A',
        'TAT': 'Y',
        'TAC': 'Y',
        'TAA': '',
        'TAG': '',
        'CAT': 'H',
        'CAC': 'H',
        'CAA': 'Q',
        'CAG': 'Q',
        'AAT': 'N',
        'AAC': 'N',
        'AAA': 'K',
        'AAG': 'K',
        'GAT': 'D',
        'GAC': 'D',
        'GAA': 'E',
        'GAG': 'E',
        'TGT': 'C',
        'TGC': 'C',
        'TGA': '',
        'TGG': 'W',
        'CGT': 'R',
        'CGC': 'R',
        'CGA': 'R',
        'CGG': 'R',
        'AGT': 'S',
        'AGC': 'S',
        'AGA': 'R',
        'AGG': 'R',
        'GGT': 'G',
        'GGC': 'G',
        'GGA': 'G',
        'GGG': 'G',
    }

    def __init__(self, sequence):
        self.sequence = sequence

    def translate(self):
        aa_sequence = ''
        for position in range(int(len(self.sequence) / 3)):
            aa_sequence += self.TRANSLATION_TABLE[self.sequence[3 * position:3 * (position + 1)]]
        return aa_sequence

assert Rna('ATGGTTACTGAACAT').translate() == 'MVTEH'


#########################################
#########################################
# Import the ``csv`` package and use it to read a tab-separated file with
# a header row into a list of dictionaries such as the example provided at
# `https://en.wikipedia.org/wiki/Tab-separated_values
# <https://en.wikipedia.org/wiki/Tab-separated_values>`_
import os
filename = os.path.join(os.path.dirname(__file__), '../../../docs/concepts_skills/software_engineering/example.tsv')
with open(filename, 'w') as file:
    file.write(('Sepal length\tSepal width\tPetal length\tPetal width\tSpecies\n'
                '5.1\t3.5\t1.4\t0.2\tI. setosa\n'
                '4.9\t3.0\t1.4\t0.2\tI. setosa\n'
                '4.7\t3.2\t1.3\t0.2\tI. setosa\n'
                '4.6\t3.1\t1.5\t0.2\tI. setosa\n'
                '5.0\t3.6\t1.4\t0.2\tI. setosa\n'))

import csv
with open(filename, 'r') as file:
    data = list(csv.DictReader(file, delimiter='\t'))

assert len(data) == 5
assert data[0] == {'Sepal length': '5.1', 'Sepal width': '3.5', 'Petal length': '1.4', 'Petal width': '0.2', 'Species': 'I. setosa'}

os.remove(filename)

#########################################
#########################################
# Use the ``print`` and ``format`` methods to write `Hello {your name}!` to standard out
import capturer
with capturer.CaptureOutput() as captured:
    print('Hello {}'.format('reader'))
    stdout = captured.get_text()

# assert stdout == 'Hello reader' # this causes an error in Read the Docs
