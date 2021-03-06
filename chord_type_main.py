#testan

from chord import chord;
from chord_type import chord_type;
from midi_notes import *;
from audio import *;

#the key to test
Dmajor = chord_type(D4,'maj',D3);

Dchords = Dmajor.getNativeChords();
Dchords7 = Dmajor.getNativeChords(1);

Fminor = chord_type(F4,'min',F3);

FchordsN = Fminor.getNativeChords(0,'natural');
FchordsH = Fminor.getNativeChords(0,'harmonic');
FchordsM = Fminor.getNativeChords(0,'melodic');

FchordsN7 = Fminor.getNativeChords(1,'natural');
FchordsH7 = Fminor.getNativeChords(1,'harmonic');
FchordsM7 = Fminor.getNativeChords(1,'melodic');

print Dchords;
print Dchords7;
print FchordsN;
print FchordsH;
print FchordsM;
print FchordsN7;
print FchordsH7;
print FchordsM7;

#looks good


#test getbasechord
Amajor = chord_type(A4,'maj',A3);
Fmajor7 = chord_type(F4,'maj7',F3);
Gminor = chord_type(G4,'min',G3);
Gminor7 = chord_type(G4,'minb7',G3);
Gbdim = chord_type(Gb4,'dim',Gb3);
Bbaug = chord_type(Bb4,'aug',Bb3);
Bbaug7 = chord_type(Bb4,'aug7',Bb3);

print 'Amaj',Amajor.getBaseChord();
print 'Fmaj7',Fmajor7.getBaseChord();
print 'Gmin',Gminor.getBaseChord();
print 'Gmin7',Gminor7.getBaseChord();
print 'Gbdim',Gbdim.getBaseChord();
print 'Bbaug',Bbaug.getBaseChord();
print 'Bbaug7',Bbaug7.getBaseChord();

Aa = Amajor.getBaseChord();
FM7 = Fmajor7.getBaseChord();
Gm = Gminor.getBaseChord();
Gm7 = Gminor7.getBaseChord();
Gbd = Gbdim.getBaseChord();
Bba = Bbaug.getBaseChord();
Bba7 = Bbaug7.getBaseChord();

print 'A',Amajor.testChord(Aa);
print 'F7',Fmajor7.testChord(FM7);
print 'Gm',Gminor.testChord(Gm);
print 'Gm7',Gminor7.testChord(Gm7);
print 'Gbd',Gbdim.testChord(Gbd);
print 'Bba',Bbaug.testChord(Bba);
print 'Bba7',Bbaug7.testChord(Bba7);

test1 = chord([A4, Db5, A5]);
print 'A4noFifth',Amajor.testChord(test1);
test2 = chord([G4, Db5, C6]);
print 'rubbish',Amajor.testChord(test2);
test3 = chord([G2, G3, G4, Bb4, D5, F5]);
print 'Gm7all',Gminor7.testChord(test3);
test4 = chord([Bb3, D4, Gb4, Bb4]);
print 'Bba7NO7',Bbaug7.testChord(test4);
test5 = chord([F,A,E]);
print 'Fmaj7noFifth',Fmajor7.testChord(test5);

print test1;
print test2;
print test3;
print test4;
print test5;

print Amajor;
a = Amajor.getCtype();
a = 'loloherp';
b = Amajor.getTonic();
b = 60;
c = Amajor.getBass();
c = 60;
print Amajor; #okay gucci just a problem with the arrays


chord1 = chord([A4, Db5, E5, A5]);
chord2 = chord([G4, B4, Gb5, A5]);

print isParallel(chord1,chord2);

Aminor = chord_type(A4,'dim',A3);
inputChord = chord([C3,A3,Eb4,A4]);

print getOrder(inputChord,Aminor);


