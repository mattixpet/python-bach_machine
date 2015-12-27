# Chord type object

#imports
from audio import reprNote
from audio import reprNotes
from audio import makeScale
from audio import findCloseNum
from audio import findClosestNumber
from audio import isParallel
from audio import getOrder
from audio import isBachProgression
from audio import all_indices
from audio import findNumSteps
from chord import chord
from bachChordError import bachChordError
import random


#variables
from midi_notes import *

#keeps track of what type of chord it is ctype = (maj, min, dim, etc) and its tonic (c,d,e).
#bass is what the bass tone is (lowest tone)
#all this mod 12 so that c is 0, d is 2, eb is 3, etc.
class chord_type:
    def __init__(self, tonic, ctype, bass):
        self.tonic = tonic%12
        self.ctype = ctype
        self.bass  = bass #bass tone
    def __repr__(self): #'tostring method'
        return reprNote(self.tonic)+'\\'+reprNote(self.bass%12)+' '+self.ctype+' chord\n'

    def getTonic(self):
        return self.tonic
    def setTonic(self,newTonic):
        self.tonic = newTonic%12
    def getCtype(self):
        return self.ctype
    def setCtype(self,newCtype):
        self.ctype = newCtype
    def getBass(self):
        return self.bass
    def setBass(self,newBass):
        self.bass = newBass

    #find the notes for a chord based on tonic and ctype, given a seed chord
    #method could be for example: 'closeUp' which means it finds the notes in this chord
    #that are closest to the notes in the seedchord (relative to movement needed from 
    #the seedchord notes) and tries to move up instead of down ('closeDown')
    #also need to supply the appropriate scale for the new chord
    #
    #as of now, the new chord has the same number of notes as seedchord
    def makeChord(self, seedChord, method, scale=[]):
        seedChord = seedChord.getNotes() #make sure to take a copy, getnotes does that
        newChord = []
        possibleNotes = self.getAllNotes()
        if method == 'closeUp' or method == 'closeDown':
            #initial step
            for note in seedChord:
                #find the note corresponding to this seed note
                if method == 'closeUp':
                    num = findCloseNum(note, possibleNotes, scale, 'hi')
                    newChord.append(num)
                elif method == 'closeDown':
                    num = findCloseNum(note, possibleNotes, scale, 'lo')
                    newChord.append(num)

            #iteration algorithm:
            #    if its closeUp, start with the highest note that is double
            #    stick the highest note to that position, and then find the lower
            #    note for the next highest note (the previous duplicate)
            #    then check for duplicates again and reiterate (reversed for closeDown)
            #
            #    for example, seedChord = [G B D]
            #    closeUp, new chord F.
            #    first iter: A C C
            #    second iter: A A C
            #    third iter: F A C done.
            converged = 0
            while (converged == 0):                
                #print 'newDB',chord(newChord)
                #print 'seedDB',chord(seedChord)
                #check to see if there are duplicates
                #start from top go down
                newChordLength = len(newChord)
                if method == 'closeUp':
                    duplicate = 0 #are there any duplicates?
                    for i in range(newChordLength-1,0,-1):
                        if newChord[i] == newChord[i-1]:
                            duplicate = 1
                            newChord[i-1] = findCloseNum(seedChord[i-1], possibleNotes, scale, 'lo')
                            
                    if duplicate == 0:
                        converged = 1

                elif method == 'closeDown':
                    duplicate = 0 #are there any duplicates?
                    for i in range(newChordLength-1):
                        if newChord[i] == newChord[i+1]:
                            duplicate = 1
                            newChord[i+1] = findCloseNum(seedChord[i+1], possibleNotes, scale, 'hi')
                            
                    if duplicate == 0:
                        converged = 1
                else:
                    print 'error, no method chosen'

        return chord(newChord)

    # find a new chord based on Bachs rules.
    # Assumes seedChord has only 4 voices, as per Bachs chorales, bass, tenor, alt and soprano
    #
    # Casts a bachChordError exception everytime it was unsuccessful in creating a chord
    # according to the rules
    #
    # seedChord is the chord to move from
    # seedChordType is the chord_type of the seedChord
    #
    # basic method: move in steps when you can, move to the nearest note in this chord with each 
    # voice in the seedchord. Make sure no parallel movement of fifths and octaves or unison.
    # make sure voices never cross (bass going higher than tenor for example)
    # make sure the final chord contains the root, third, fifth and seventh of the chord
    # make sure to prepare and solve 7ths and minor 5ths
    def makeBachChord(self, seedChord, seedChordType):
        random.seed()
        #get all the stuff we might need
        seedNotes = seedChord.getNotes()
        seedOrder = getOrder(seedChord, seedChordType)
        #get all seed chord notes mod 12
        seedNotesMod12 = []
        for note in seedNotes:
            seedNotesMod12.append(note%12)

        baseChord = self.getBaseChord()
        baseOrder = getOrder(baseChord, self)
        baseNotes = baseChord.getNotes()

        #start by casting exception if there is no way to either prepare a fifth/seventh
        #or resolve one
        if (5 in seedOrder) and ('dim' in seedChordType.getCtype()):
            seedIdx5 = all_indices(5,seedOrder)[0]
            if (not self.isValid(seedNotes[seedIdx5]-1)) and (not self.isValid(seedNotes[seedIdx5]-2)):
                raise bachChordError("Cannot possibly resolve minor fifth in seed chord")
        if (7 in seedOrder):
            seedIdx7 = all_indices(7,seedOrder)[0]
            if (not self.isValid(seedNotes[seedIdx7]-1)) and (not self.isValid(seedNotes[seedIdx7]-2)):
                raise bachChordError("Cannot possibly resolve seventh in seed chord")
        if ('dim' in self.ctype):
            baseIdx5 = all_indices(5,baseOrder)[0]
            if (baseNotes[baseIdx5] not in seedNotesMod12):
                raise bachChordError("Cannot possibly prepare minor fifth in destination chord")
        if (7 in baseOrder):
            baseIdx7 = all_indices(7,baseOrder)[0]
            if (baseNotes[baseIdx7] not in seedNotesMod12):
                raise bachChordError("Cannot possibly prepare seventh in destination chord")

        #try all permutations of the candidate arrays
        bassCans = [] #candidates
        tenoCans = []
        altoCans = []
        soprCans = []
        bachChordCan = []

        #start by adding the closest possible bass note and the one an octave lower
        possibleBasses = []
        for i in range(21,108+1):
            if (i%12) == self.bass%12:
                possibleBasses.append(i)
        
        bassCan = findClosestNumber(self.bass, possibleBasses)
        bassCans.append(bassCan)
        bassCans.append(bassCan-12)

        # for now just try all possibilities...
        allValid = self.getAllNotes()
        tenoCans = list(allValid)
        altoCans = list(allValid)
        soprCans = list(allValid)
        # go through all permutations of the cans
        # first try to get bass, alto, tenor, soprano all in steps
        # then try 3
        # then try to have two of them take steps
        # then try one of them
        # and if none of that works, settle for no steps!
        numStepsGoal = 4
        numSteps = -1
        success = False
        while not success:
            valid = False
            for i in range(len(bassCans)):
                if valid:
                    break
                for j in range(len(tenoCans)):
                    if valid:
                        break
                    for k in range(len(altoCans)):
                        if valid:
                            break
                        for l in range(len(soprCans)):
                            newChord = chord([bassCans[i], tenoCans[j], 
                                              altoCans[k], soprCans[l]])
                            valid = isBachProgression(seedChord, seedChordType,
                                                      newChord, self)
                            numSteps = findNumSteps(newChord.getNotes(),
                                                    seedChord.getNotes())
                            valid = valid and numSteps == numStepsGoal       
                            if valid:
                                success = True
                                bachChordCan = newChord
                                break
            numStepsGoal = numStepsGoal - 1
            if numStepsGoal < 0:
                valid = False
                break

        if not valid:
            raise bachChordError("Couldn't make bach chord: "+
                                 str(self) + " seed "+str(seedChord))
        return bachChordCan
        

    # find if a note is valid for this chord
    # can always add more chord types
    # try to correspond to allowedChordtypes in audio.py
    def isValid(self,note):
        valid = [] # array of valid notes (always mod 12)
        t = self.tonic # basetone
        if   self.ctype == 'maj':
            valid = [t%12, (t+4)%12, (t+7)%12]
        elif self.ctype == 'min':
            valid = [t%12, (t+3)%12, (t+7)%12]
        elif self.ctype == 'dim':
            valid = [t%12, (t+3)%12, (t+6)%12]
        elif self.ctype == 'maj7':
            valid = [t%12, (t+4)%12, (t+7)%12, (t+11)%12]
        elif self.ctype == 'majb7':
            valid = [t%12, (t+4)%12, (t+7)%12, (t+10)%12]
        elif self.ctype == 'minb7':
            valid = [t%12, (t+3)%12, (t+7)%12, (t+10)%12]
        elif self.ctype == 'min7':
            valid = [t%12, (t+3)%12, (t+7)%12, (t+11)%12]
        elif self.ctype == 'dimbb7':
            valid = [t%12, (t+3)%12, (t+6)%12, (t+9)%12]
        elif self.ctype == 'dimb7':
            valid = [t%12, (t+3)%12, (t+6)%12, (t+10)%12]
        elif self.ctype == 'maj6':
            valid = [t%12, (t+4)%12, (t+7)%12, (t+9)%12]
        elif self.ctype == 'sus4':
            valid = [t%12, (t+5)%12, (t+7)%12]
        elif self.ctype == '7sus4':
            valid = [t%12, (t+5)%12, (t+7)%12, (t+10)%12]
        elif self.ctype == 'aug':
            valid = [t%12, (t+4)%12, (t+8)%12]
        elif self.ctype == 'aug7':
            valid = [t%12, (t+4)%12, (t+8)%12, (t+11)%12]
        else:
            print 'error in is valid chord, incorrect chord specification'

        return ((note%12) in valid)

    # test a chord to see if it's valid (contains only notes from this chord)
    def isValidChord(self,inputChord):
        notes = inputChord.getNotes() #make sure we don't change, take a copy
        for note in notes:
            if not self.isValid(note):
                return False
        
        return True
            
    #get all possible notes of this chord (from 21-108)
    def getAllNotes(self):
        notes = []
        for i in range(21,108+1):
            if self.isValid(i):
                notes.append(i)
        return notes

    #fproperty to get all the native chords to this chord type
    #for example 'maj' on C gives you [Cmaj,Dmin,Emin,Fmaj,Gmaj,Amin,Bdim]
    #                                 [I   ,ii  ,iii ,IV  ,V   ,vi  ,vii*]
    #takes as input chord type, a 'do you want sevenths?' (0 or 1) and if its a minor, an input saying
    #                                                              whether its a natural,  harmonic or
    #                                                              melodic 
    def getNativeChords(self, seventh=0, scaleType='major'):
        types = [] #an array with strings of the types of chords, starting with I, then II etc.
        chords = [] #final array to return, the native chords of that chordType
        
        #three possibilities for scaletype
        if scaleType == 'aeolian' or scaleType == 'minor':
            scaleType = 'natural'
            
        if   self.ctype == 'maj':
            if not seventh:
                #       [    I,   ii,  iii,   IV,    V,   vi, vii*]
                types = ['maj','min','min','maj','maj','min','dim']
            else:
                #       [  I-M7,   ii7,    iii7, IV-M7,     V7,    vi7,vii*-b7]
                types = ['maj7','minb7','minb7','maj7','majb7','minb7','dimb7']
        elif self.ctype == 'min':
            if not seventh:
                if   scaleType == 'natural':
                    #       [    i,  ii*,  III,   iv,    v,   VI,  VII]
                    types = ['min','dim','maj','min','min','maj','maj']
                elif scaleType == 'harmonic':
                    #       [    i,  ii*, III+,   iv,    V,   VI,#vii*]
                    types = ['min','dim','aug','min','maj','maj','dim']
                elif scaleType == 'melodic':
                    #       [    i,   ii, III+,   IV,    V,  vi*, vii*]
                    types = ['min','min','aug','maj','maj','dim','dim']
                else:
                    print 'wrong scale type in function getNativeChords'
            else:
                if   scaleType == 'natural':
                    #       [     i7, ii*-b7,III-M7,    iv7,     v7, VI-M7,   VII7]
                    types = ['minb7','dimb7','maj7','minb7','minb7','maj7','majb7']
                elif scaleType == 'harmonic':
                    #       [  i-M7, ii*-b7, III+7,    iv7,     V7, VI-M7,#vii*bb7]
                    types = ['min7','dimb7','aug7','minb7','majb7','maj7','dimbb7']
                elif scaleType == 'melodic':
                    #       [  i-M7,  ii-b7, III+7,    IV7,     V7, #vi*b7,#vii*b7]
                    types = ['min7','minb7','aug7','majb7','majb7','dimb7','dimb7']
                else:
                    print 'wrong scale type in function getNativeChords'
        else:
            print 'error in findNativeChords, wrong chord type, only "maj" and "min" are allowed'
            
        #get corresponding scale (to get all the starting notes of the chords correct)
        scaleNotes = makeScale(self.tonic,scaleType)

        #find starting note of the chord (its mod 12, so we just start from 21)
        startNote = -1
        for i in range(21,108+1):
            if (i%12)==(self.tonic%12):
                startNote = i
                break
            
        #find the index in our scale that is that start note
        scaleIdx = -1
        for i in range(len(scaleNotes)):
            if (startNote)==scaleNotes[i]:
                scaleIdx = i
                break
            
        #now start at our startnote in the scale, and go through our 7 chords (types array)
        #starting with the startnotes depicted by the scale
        typesIdx = 0 #index of types array
        for i in range(scaleIdx,scaleIdx+len(types)):
            #add our chords, reminder: chord_type(tonic, type, bass note)
            #choose the bass note to be the 3rd (A3) by adding 48 to the mod 12 value.
            #for example, C major would get a bass of C%12 = 0 + 48 = C3
            chords.append(chord_type(scaleNotes[i],types[typesIdx],(scaleNotes[i]%12)+48))
            typesIdx = typesIdx + 1 #increment
            
        return chords

    #returns False if chord is not triad (aka it's a seventh chord)
    def isTriad(self):
        if '7' in self.ctype:
            return False
        else:
            return True

    #property to get the triad chord or seventh chord, mod 12 of course.
    #so if for example if we have a Cmajor chord type, Cmajor.getBaseChord() would
    #return a chord with [C,E,G] = [0,4,7]
    #Cmajor7 ==> [C,E,G,B] etc.
    def getBaseChord(self):
        chordArr = [] #chord array to return
        #if some kind of seventh chord
        triad = self.isTriad()
        i = self.tonic
        noteCount = 0 #max 3 for triad chord, 4 for seventh
        while True:
            if self.isValid(i%12):
                chordArr.append(i%12)
                noteCount = noteCount + 1
            if noteCount == 3 and triad:
                break
            if noteCount == 4 and not triad:
                break
            i = i + 1
        return chord(chordArr)

    #test a chord and see if it contains all necessary notes, aka tonic, third and fifth
    #                                                         and or seventh
    #returns 1 if it's missing the tonic, 
    #        3 if it's missing the third 
    #        7 if it's missing the seventh 
    #        0 if it has some notes invalid
    #        10 if it's got all 4 notes (or all three if no seventh)
    #        5 if it's only missing the fifth but has the rest
    def testChord(self, inputChord):
        #before we do anything, make sure this chord has only allowed notes
        if not self.isValidChord(inputChord):
            return 0

        notes = inputChord.getNotes() #as per chord object, make a COPY dont change original, getnotes
                                       #guarantees that supposedly
        for i in range(len(notes)): #move everything down to its basics mod 12
            notes[i] = notes[i]%12

        baseChord = self.getBaseChord().getNotes()

        #now, go through the base chord, one note at a time (tonic, third, fifth and seventh)
        #and check to see which ones we have in our chord
        ton = baseChord[0] in notes
        thi = baseChord[1] in notes
        fif = baseChord[2] in notes
        if not self.isTriad():
            sev = baseChord[3] in notes
        else:
            sev = True #won't affect the triad results, assume it's there

        if (not ton): 
            return 1

        if (not thi):
            return 3

        if (not sev):
            return 7

        if (ton and thi and fif and sev):
            return 10

        if (ton and thi and sev) and (not fif):
            return 5

        print 'error in testChord, i messed up...'
        return -1

 

