# python-bach_machine

## Summary:
* This is an unfinished project of mine. 
* The idea was to make a program which could generate chords in progressions similar to Bach's chorales (usage possibilities are e.g. composition).
* Capabilities so far: 
  * Can make random chords in the same key, given a seed chord and given a final cadence. 
  * Writes this to a MIDI file.
* Capabilities missing: 
  * Modulation.
  * More robust chord generation (less chord progressions the program fails on).
  * Automatic seed chord.
  * Automatic cadence.
  * Something other than random chords perhaps, at least need to get rid of how common it is that it uses the same chord (and same notes) alternating.
* Check out a couple of resulting MIDI files in the **samples/** folder!

## Usage:
* `python bach.py`
The bach.py script when run once, tries only one sequence of random chords between the given seed and the cadence, and throws an error if unsuccessful.
* A more practical usage is to use either the **bach.bat** or **bach.sh** script which invokes the main file, **bach.py**, and continuously tries making chords, and saving successful creations to **'bachMidis/bachTest'+randomnumber0-20000000+'.mid'**. Takes maybe a couple of minutes to get a few successful progressions.
* Editable values to look out for. Most rest in the "main code" in **bach.py**. For example
  * `numChords` - number of chords in the progression (roughly)
  * `aug`,`dim`,`notSev` - probabilities of this type of chord to appear. `notSev` meaning not a seventh chord.
  * `seedChord`
  * and the cadence at the end

## Info:
* So far uses python 2.7 (but only due to the print commands), this is written purely from scratch by me except for the [MIDI tool](http://www.emergentmusics.org/midiutil).
* This was one of my first python projects, so the code organization is.. not optimal.

###### Written in 2014.