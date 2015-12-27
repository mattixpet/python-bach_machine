# This is supposed to be a program that makes random chords 
# according to Bach's rules. Needs a seed chord.probles for deciding chords:
#
#
#

#---------imports---------#
from midiutil.MidiFile import MIDIFile
from chord_type import chord_type
from bachChordError import bachChordError
from audio import writeChords
from chord import chord
import random

#---------initialization of variables---------#
from midi_notes import * #import C4=60 etc and midiNotes[C4]='C4'
random.seed()
# Create the MIDIFile Object with 1 track
MyMIDI = MIDIFile(1)

#---------object declerations---------#

#---------functions---------#

# Usage: ctypes = makeRandomChordtypes(l1, l2, p1, aug, dim)
# Pre:   0 <= aug + dim <= 1, 0 <= prob1 <= 1
#        l1, l2 are lists of chord_types
#        aug and dim are probabilities of their respective chord_types
#        num is number of chords to make
# Post:  ctypes is the random chord types (num count) from l1 or l2. 
#        chord from l1 is chosen with probability p1, 
#        otherwise l2. aug and dim chords chosen with probability aug and dim.
def makeRandomChordtypes(list1, list2, prob1, aug, dim, num):
	chordTypes = []
	chordx = list1[0]
	for i in range(num):
		prob = random.random()
		if prob < prob1:
			chordx = makeRandomChord(list1, aug, dim)
		else:
			chordx = makeRandomChord(list2, aug, dim)
		chordTypes.append(chordx)
	return chordTypes

#similar to makeRandomChordtypes, except only does a single list
def makeRandomChord(list1, aug, dim):
	reg = 1 - aug - dim
	prob = random.random();
	if prob < reg:
		#regular chord
		r = random.randint(0, len(list1)-1)
		ctype = list1[r].getCtype()
		while ('aug' in ctype or 'dim' in ctype):
			r = random.randint(0, len(list1)-1)
			ctype = list1[r].getCtype()
		chordx = list1[r]
	elif prob >= reg and prob < (reg + dim):
		#dim
		r = random.randint(0, len(list1)-1)
		ctype = list1[r].getCtype()
		while ('dim' not in ctype):
			r = random.randint(0, len(list1)-1)
			ctype = list1[r].getCtype()
		chordx = list1[r]
	else:
		#aug
		r = random.randint(0, len(list1)-1)
		ctype = list1[r].getCtype()
		while ('aug' not in ctype):
			r = random.randint(0, len(list1)-1)
			ctype = list1[r].getCtype()
		chordx = list1[r]
	return chordx

#---------main code---------#
numChords = 8

# quick initial test, do a couple of random chords, and then end
# with a cadence

Aminor = chord_type(A4, 'min', A3)
Anative = Aminor.getNativeChords(0, 'harmonic')
Anative7 = Aminor.getNativeChords(1, 'harmonic')

seedChord = chord([A3, E4, A4, C5])
seedChordType = Aminor

chordTypes = [seedChordType]

#0.7 chance of regular chord
#0.3 chance of seventh
#   0.05 chance of aug
#   0.25 chance of dim
#   0.7 chance of regular
aug = 0.05
dim = 0.25
reg = 1 - dim - aug
notSev = 0.7
tempChordtypes = makeRandomChordtypes(Anative, Anative7, 
	                                  notSev, aug, dim, 
	                                  numChords)

chordTypes.extend(tempChordtypes) #append tempChordtypes to chordTypes

#cadence, let it just be Dminor, Emajor7, Amajor
chordTypes.append(chord_type(D3, 'min', D3))
chordTypes.append(chord_type(E3, 'majb7', E3))
chordTypes.append(chord_type(A3, 'maj', A3))

print chordTypes

#now for the actual chord making
chords = []
chords.append(seedChord)

prevChord = seedChord
checkedBasses = []
for i in range(len(chordTypes)-1):
	print prevChord
	try:
		thisChord = chordTypes[i+1].makeBachChord(prevChord, chordTypes[i])
	except bachChordError as e:
		raise bachChordError(e.value)
		#have we tried all different bass notes possible?
		checkedBasses.append(chordTypes[i+1].getBass())
		print "bachChordError: ", e.value
		print "Trying different bass note"
		newBass = getNextBass(chordTypes[i+1], checkedBasses)
		chordTypes[i+1].setBass(newBass)
		if len(checkedBasses) < 4:
			i = i - 1
		else:
			raise bachChordError("Tried all basses, still failed to make chord " +
				                  str(chordTypes[i+1]) + " seed " + str(prevChord))
	chords.append(thisChord)
	prevChord = thisChord

#shitmix for the cadence
#chords.append(chord([D3, A3, D4, F4]))
#chords.append(chord([E3, B3, D4, Ab4]))
#chords.append(chord([A3, E3, Db4, A4]))

print chords
writeChords(chords, MyMIDI, 80, 4, 120)

# And write it to disk.
post = random.randint(0,200000)
binfile = open("bachMidis/bachTest" + str(post) + ".mid", 'wb')
MyMIDI.writeFile(binfile)
binfile.close()