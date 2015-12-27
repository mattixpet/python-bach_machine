#testan

#Import the library

from midiutil.MidiFile import MIDIFile;
from audio import *;	

# Create the MIDIFile Object with 1 track
MyMIDI = MIDIFile(1)

a = chord([A1, A3, C4 ,E4]);
b = chord([F1, A3, C4, F4]);
c = chord([C2, G3, C4, E4]);
d = chord([G1, G3, B3, D4]);
chords = [a,b,c,d];
writeChords(chords,MyMIDI,80);

# And write it to disk.
binfile = open("chord_test.mid", 'wb')
MyMIDI.writeFile(binfile)
binfile.close()
