# Chord object

#imports
from audio import reprNotes;

#chord object, contains an array of notes
class chord:
    def __init__(self, notes):
        self.notes = notes;
    def __repr__(self): #'tostring method'
        return reprNotes(self.notes)+'\n';

    #function to get the notes, make sure to return a copy so the user cannot alter it
    def getNotes(self):
	return list(self.notes);

    #basic set function
    def setNotes(self,newNotes):
	self.notes = list(newNotes); #make sure we don't just point to newNotes, take a copy

    #make a copy and return it
    def copy(self):
	return chord(list(self.notes));

