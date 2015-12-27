#testan

from chord import chord
from chord_type import chord_type
from midi_notes import *
from audio import *

Dmajor = chord_type(D4,'maj', Gb3)

seedChord = chord([E3, B4, D5, G5])
seedChordType = chord_type(E3, 'min7', E3)
bachChord = Dmajor.makeBachChord(seedChord, seedChordType)

print 'seed: ',seedChord
print 'result: ',bachChord

