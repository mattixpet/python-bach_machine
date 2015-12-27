# Bach chord making exception
# called if making a bach chord (chord_type.makeBachChord()) fails

class bachChordError(Exception):
    def __init__(self, value):
        self.value = value;
    def __str__(self):
        return repr(self.value);
