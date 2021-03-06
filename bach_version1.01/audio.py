# This is supposed to be an audio library capable of writing midi files and making chords.
#might need to use chord and chord_type with this and midi_notes.py

#---------imports---------#
from midiutil.MidiFile import MIDIFile
import sys

#---------initialization of variables---------#
from midi_notes import * #import C4=60 etc and midiNotes[C4]='C4'

#---------object declerations---------#



#---------functions---------#

#write an array of chords to a midi file seperated by duration (default=8) beats with tempo (default=120)
#track # from 0-127 (default 0), channel=0 (default), volume= 100(default) at time (default=0)
#using program (default=19 organ) see general midi

#takes as input a midifile and returns the file with the written chords
def writeChords(chords,MyMIDI,program=19,duration=8,tempo=120,track=0,channel=0,volume=100,time=0):
    
    #changing time, depending on the chords
    timex = time

    # Add track name and tempo.
    MyMIDI.addTrackName(track,time,"Track "+str(track))
    MyMIDI.addTempo(track,time,tempo)

    #write the chord notes of duration duration each
    for chordx in chords:
        for note in chordx.notes:
            MyMIDI.addNote(track,channel,note,timex,duration,volume)
        timex = timex+duration

    #change from piano to organ (or value)
    MyMIDI.addProgramChange(track,channel, time, program)

    return MyMIDI

    #debug
    #print str(chords)
    #print str(duration)
    #print str(tempo)
    #print str(track)
    #print str(channel)
    #print str(volume)

# Usage: a = getChordFrom(note, chordType)
# Pre:   note is a valid note in chordType
# Post:  a is the chord starting from note
#
# Example: note = A3, chordType = Fmajor
#          a == [A3, C4, F4]
def getChordFrom(note, chordType):
    order = getOrderSingle(note)
    base = chordType.getBaseChord()
    # append another chord to basechord
    # for example: base = [0, 4, 7, 10]
    # after loop: base = [0, 4, 7, 10, 12, 16, 19, 22]
    for num in base:
        base.append(num+12)
    realChord = []
    cnt = 0
    for num in base:
        if cnt == 4:
            break
        if num == order or cnt > 0:
            realChord.append(num+note)
            cnt = cnt + 1
    return realChord

# Usage: a = getNextBass(ctype, chBass)
# Pre:   ctype is a chordType, chBass is an array of checked
#        basses of length max 4
# Post:  a is the next bass according to the philosophy
#        if we have for example ctype=Fmajor, chBass = [A3]
#        next bass will be C4
def getNextBass(chordType, checkedBasses):
    chordx = getChordFrom(checkedBasses[-1], chordType)
    return chordx[1]

# Usage: num = findNumSteps(list1, list2)
# Pre:   list1 and list2 are of same length
# Post:  num is the number of step movements
#        between list1 -> list2
#        for example: list1 = [ 1, 2, 3 ] list2 = [ 2, 2, 5 ]
#        num will be 2 (0, 1 and 2 chromatic movements are considered
#        a step)
def findNumSteps(list1, list2):
    numSteps = 0
    for i in range(len(list1)):
        dist = abs(list1[i]-list2[i])
        if dist <= 2:
            numSteps = numSteps + 1
    return numSteps

#takes as an input an array of numbers, and a single number, and finds the number
#in the array closest to the number (according to the scale, for example B is one
#away from A and 1 away from C if its a Cmajor scale)
#Takes the scale as an argument. ALL NOTES IN THE NUMBERS array MUST BELONG TO THE SCALE
#takes as an additional argument
# 'lower' or 'higher' depicting wether it chooses the lower or higher number
#if there are ambiguities (assumes no more than two numbers can have an ambiguity)
def findCloseNum(number, numbers, scale, hilo):
    numbersRepr = [] #array of new location of numbers, according to the scale
    for i,note in enumerate(scale):
        if note in numbers:
            numbersRepr.append(i)

    numberRepr = -1 #representation of our number in this new space
    #go through scale until our number is one of the scale numbers, or between 2
    for i,note in enumerate(scale):
        if i>0:
            if number >= scale[i-1] and number < scale[i]:
                if number > scale[i-1] and number < scale[i]:
                    numberRepr = ((i-1)+i)/2 #average, so it is equally far from both scale notes
                elif number == scale[i-1]:
                    numberRepr = i-1 #its a part of the scale
                else:
                    print 'error in findCloseNum'

    #print 'numbers: ',chord(numbers)
    #print 'new repr: ',numbersRepr
    #print 'number: ',reprNote(number)
    #print 'number Repr: ',numberRepr

    distances = [] #vector of distances from the number
    for num in numbersRepr:
        distances.append(abs(num-numberRepr))
    
    #print 'distances',distances

    #find the smallest or two smallest distances
    minIdx = min2(distances)

    minNum = [] #array of the closest number/s
    minNum.append(numbers[minIdx[0]])
    if (distances[minIdx[0]] == distances[minIdx[1]]): #ambiguity, need both values
        minNum.append(numbers[minIdx[1]])

    if hilo=='lo':
        return min(minNum)
    if hilo=='hi':
        return max(minNum)

    print "error in findCloseNum"
    return -1

#finds the two lowest numbers in a list
#only used by findCloseNum
def min2(numbers):
    intMin = sys.maxint
    intMin2 = intMin
    intMinIdx = 0
    intMin2Idx = 0
    for idx,num in enumerate(numbers):
        if num <= intMin:
            intMin2 = intMin
            intMin2Idx = intMinIdx
            intMin = num
            intMinIdx = idx
    
    return [intMinIdx,intMin2Idx]

#Usage: num = findClosestNumber(a, numbers)
#Pre:   nothing
#Post:  num is the number from numbers that is closest to a
def findClosestNumber(number, numbers):
    distances = [] #vector of distances from the number
    minNum = 0
    max = 500 
    for num in numbers:
        dist = abs(num-number)
        distances.append(dist)
        if dist < max:
            max = dist
            minNum = num
    return minNum    

#returns all possible notes in this scale in ascending order
#tonic is the first note of the scale
#scaleType is the scale type, for example: 'major','harmonic','melodic','natural' 
#need to add more scales
def makeScale(tonic,scaleType):
    notes = [] #notes of this scale, relative to C (=0) (goes from 0-11)
    if scaleType == 'major':
        notes = [0,2,4,5,7,9,11]
    elif scaleType == 'harmonic':
        notes = [0,2,3,5,7,8,11]
    elif scaleType == 'melodic':
        notes = [0,2,3,5,7,9,11]
    elif scaleType == 'natural' or scaleType == 'minor' or scaleType == 'aeolian':
        notes = [0,2,3,5,7,8,10]
    elif scaleType == 'blues':
        notes = [0,3,5,6,7,10]
    elif scaleType == 'penta':
        notes = [0,3,5,7,10]

    shiftedNotes = [] #notes relative to tonic
    for note in notes:
        shiftedNotes.append((note+(tonic%12))%12)

    finalScale = []
    for i in range(21,108+1):
        if (i%12) in shiftedNotes:
            finalScale.append(i)

    return finalScale

#function to return C,Db,D,Eb,E, etc depending on the input note (mod 12)
def reprNote(note):
    #n = [ 'C','Db','D','Eb','E','F','Gb','G','Ab','A','Bb','B' ]
    return midiNotes[note]

#function similar to reprNote, except for a whole array
def reprNotes(notes):
    array = []
    for note in notes:
        array.append(reprNote(note))
    return str(array)

#function to check if there were parallel fifths, unisons or octaves movement
#takes in the two chords to check, assumes 4 notes, voices in correct order
def isParallel(chord1,chord2):
    chord1 = chord1.getNotes()
    chord2 = chord2.getNotes()
    fifth = 7 #space between notes in a fifth
    octave = 0 #whatever number of octaves or unison because %12
    bannedIntervals = [fifth,octave]

    #check all pairs and compare them to all pairs in chord 2, to check for the movement
    for i in range(len(chord1)):
        for j in range(len(chord1)):
            if i != j:
                dist1 = abs(chord1[i]-chord1[j])%12
                dist2 = abs(chord2[i]-chord2[j])%12
                if (dist1 == dist2) and dist1 in bannedIntervals:
                    return True 
                
    return False

#function to get an array a=[x,y,z,w] where x,y,z,w signify what note each voice is.
#for example is the bass is the tonic, tenor is the tonic, alto is the third and soprano is a seventh
#then a = [1,1,3,7]
#assumes only 4 notes in bach configuration (bass, tenor, alto, soprano)
def getOrder(inputChord, chordType):
    baseChord = chordType.getBaseChord().getNotes()
    inputChord = inputChord.getNotes()
    a = [0,0,0,0] #chord to return
    for i in range(len(inputChord)):
        if (inputChord[i]%12) == baseChord[0]:
            a[i] = 1
        elif (inputChord[i]%12) == baseChord[1]:
            a[i] = 3
        elif (inputChord[i]%12) == baseChord[2]:
            a[i] = 5
        elif len(baseChord)==4 and (inputChord[i]%12)==baseChord[3]:
            a[i] = 7
    return a

# similar to get order, but for a single note
def getOrderSingle(inputNote, chordType):
    a = getOrder([inputNote, inputNote, inputNote, inputNote], chordType)
    return a[0]

# function to check to see if the progression between two chords is legal
# according to bach's rules, from chord1-->chord2
# chord_types are related to their respective chords
#
# assumes chord1 and chordType1 are compatible and everything good
#
# example input: isBachProgression(chord([A4,Db5,E5,A5]),chord_type(A4,'maj',A3),chord([G3,D5,D5,B5]),chord_type(G4,'maj',G3)) would return true
def isBachProgression(chord1,chordType1,chord2,chordType2):
    #get the orders [1,1,3,7] for example
    order1 = getOrder(chord1,chordType1)
    order2 = getOrder(chord2,chordType2)
    #get the note array
    notes1 = chord1.getNotes()
    notes2 = chord2.getNotes()
    #check for parallel fifths,octaves,unisons
    if isParallel(chord1,chord2):
        return False
    #for now allow only all notes to be a part of the next chord (tonic,third,fifth and seventh)
    if chordType2.testChord(chord2) != 10: #and chordType2.testChord(chord2) != 5:
        return False
    #check distances between voices
    #no more than 12th between tenor and soprano and no more than an octave between tenor-alto
    #and alto-soprano in chord2
    #Note: 12th is 19 notes (chromatically)
    #      8th is  12 notes
    distTenSop = abs(notes2[3]-notes2[1])
    distTenAlt = abs(notes2[2]-notes2[1])
    distAltSop = abs(notes2[3]-notes2[2])
    if (distTenSop > 19) or (distTenAlt > 12) or (distAltSop > 12):
        return False
    #check to see if any voices crossed
    #for now, none of that is allowed
    #equivalent to see if the notes aren't in ascending order
    prevNote = notes2[0]
    for note in notes2:
        if not (note >= prevNote):
            return False
        prevNote = note
    #check for double thirds, for now don't allow them at all
    if len(all_indices(3,order2)) > 1:
        return False
    #now check to see if suspensions were prepared/resolved
    #for now, assume only suspenses are minor fifths and sevenths
    #start with chord1
    #check fifths, assume only one fifth at most and 1 seventh
    if (5 in order1) and ('dim' in chordType1.getCtype()):
        idx5 = all_indices(5,order1)[0]
        #the fifth must be resolved by going one step down
        if not isResolved(idx5,chord1,chord2):
            return False
    if (7 in order1):
        idx7 = all_indices(7,order1)[0]
        if not isResolved(idx7,chord1,chord2):
            return False
    #now to chord2, check to see if everything wasn't prepared
    if (5 in order2) and ('dim' in chordType2.getCtype()):
        idx5 = all_indices(5,order2)[0]
        #the fifth must be resolved by staying at the same spot or going one step down
        if not isPrepared(idx5,chord1,chord2):
            return False
    if (7 in order2):
        idx7 = all_indices(7,order2)[0]
        if not isPrepared(idx7,chord1,chord2):
            return False  
    #limit the voicing jumps to max fifth unless octave, except for the bass
    jumps = findDistances(notes1, notes2)
    #ignore the bass (jumps[0])
    for jump in jumps[1:]:
        # more than 7 means more than a fifth, lets not
        # unless it's an octave, == 12
        if jump > 7 and jump != 12: 
            return False
    return True #whoop!
    
#Usage: a = findDistances(c,d)
#Pre:   c and d are arrays of same length with numbers
#Post:  a is an array of same length as c&d containing the distances
#       between their numbers
def findDistances(c, d):
    distances = [] #vector of distances from the number
    for i, num in enumerate(c):
        distances.append(abs(num-d[i]))
    return distances

#function to return all indices of value in qlist
#taken from: http://stackoverflow.com/questions/176918/finding-the-index-of-an-item-given-a-list-containing-it-in-python
#from Hongbo Zhu
def all_indices(value, qlist):
    indices = []
    idx = -1
    while True:
        try:
            idx = qlist.index(value, idx+1)
            indices.append(idx)
        except ValueError:
            break
    return indices
    
#function to check to see if the note at index was resolved going from chord1-->chord2
#resolved means that the note moved one step down
#
# attention: maybe resolved also means stay put?
def isResolved(idx,chord1,chord2):
    notes1 = chord1.getNotes()
    notes2 = chord2.getNotes()
    if (notes2[idx]!=(notes1[idx]-1)) and (notes2[idx]!=(notes1[idx]-2)):
        return False    
    return True

#function to check to see if the note at index was prepared 
#prepared means that the note appeared first in the same voice in chord1, before it became
#a suspension in chord2
def isPrepared(idx,chord1,chord2):
    notes1 = chord1.getNotes()
    notes2 = chord2.getNotes()
    if notes1[idx]!=notes2[idx]:
        return False 
    return True

#---------main code---------#

#lol, no code, just a class for importing.
#test code in seperate files
