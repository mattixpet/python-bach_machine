from audio import *;
from chord_type import chord_type;
from chord import chord;

#testing code
numbers = [F4,A4,C5];
number = B4;

print reprNote(findCloseNum(number,numbers,makeScale(C4,'major'),'lo'));

Cmajor = chord_type(C4,'maj',C2);
print Cmajor;
print str(Cmajor.getAllNotes());

Aminor = chord_type(A4,'min',A2);
print 'type',Aminor;
seedChord = chord([A4,C5,F5]);
print 'seed',seedChord;
new = Aminor.makeChord(seedChord,'closeUp',makeScale(A4,'minor'));
print 'new chord',new;

a = makeScale(A4,'minor');
print reprNotes(a);

Gmajor = chord_type(G4,'maj',G2);
print 'type',Gmajor;
seedChord = chord([F4,A4,C5]);
print 'seed',seedChord;
new = Gmajor.makeChord(seedChord,'closeDown',makeScale(C4,'major'));
print 'new chord',new;

a = isBachProgression(chord([G3,G4,Bb4,D5]),chord_type(G4,'min',G3),chord([F3,A4,C5,Eb5]),chord_type(F4,'majb7',F3));
print a;

a = [-5, 2, 80, 1, -10, 20]
print findClosestNumber(1.4999,a)

