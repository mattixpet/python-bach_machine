#testan

#Import the library

from midiutil.MidiFile import MIDIFile
from audio import *	
from chord_type import chord_type
from chord import chord
import random

# Create the MIDIFile Object with 1 track
MyMIDI = MIDIFile(1)

random.seed()

Dmajor = chord_type(D4,'maj',D3)
Eminor = chord_type(E4,'min',E3)
Gbminor = chord_type(Gb4,'min',Gb3)
Gmajor = chord_type(G4,'maj',G3)
Amajor = chord_type(A4,'maj',A3)
Bminor = chord_type(B4,'min',B3)

chord_types = [Dmajor,Eminor,Gbminor,Gmajor,Amajor,Bminor]

#initial seed
seedChord = chord([Gb3,Gb4,A4,Db5]) #F# minor

#make a sequence of 8 random chords, hi lo with equal probability
#use last chord as seed chord

chords = [seedChord]
N=10
r = 0
rprev = 0
for i in range(N-1):
    while (r == rprev):
        r = random.randint(0,len(chord_types)-1)
    rprev = r
    r2 = random.randint(0,1)
    r3 = random.randint(0,1)
    if r2 == 0:
        method = 'closeUp'
    else:
        method = 'closeDown'

    newChord = chord_types[r].makeChord(seedChord,method,makeScale(D4,'major'))
    if r3 == 0:
        chords.append(newChord)
    else:
        newChord.notes[0] = chord_types[r].bass
        chords.append(newChord)

    seedChord = newChord

writeChords(chords,MyMIDI,80,1,200)

# And write it to disk.
binfile = open("makeChord_test.mid", 'wb')
MyMIDI.writeFile(binfile)
binfile.close()
