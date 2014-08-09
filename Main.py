from random import *
from numpy import *
import sys
import pygame
import time
from pygame.mixer import music

soundfileDirectory = "C:\Users\Michael\Desktop\University of Iowa Piano Samples\WAV\AlignedFiles2" +"\\"

pygame.init()
screen = pygame.display.set_mode((400,400))

# For accessing note values
notes = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}

# For accessing note names
inverseNotes = {v: k for k, v in notes.items()}

beatDivisions = {0:1/32, 1:1/16, 2:1/8, 3:1/4, 4:1/2, 5:1, 6:2}



#         1                 2                3        4               5                6                  7
chordTypes = {
          "Major": [0, 4, 7], 
          "Minor": [0, 3, 7], 
          "Diminished": [0, 3, 6], 
          "Add 9": [0, 4, 7, 2], 
          "Major 7": [0, 4, 7, 11], 
          "7": [0, 4, 7, 10]
                
          }

identityMatrix = matrix(identity(12))

pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.mixer.init()
pygame.mixer.set_num_channels(24)

pygame.init()

chan0 = pygame.mixer.Channel(0)
chan1 = pygame.mixer.Channel(1)
chan2 = pygame.mixer.Channel(2)
chan3 = pygame.mixer.Channel(3)
chan4 = pygame.mixer.Channel(4)
chan5 = pygame.mixer.Channel(5)
chan6 = pygame.mixer.Channel(6)
chan7 = pygame.mixer.Channel(7)
chan8 = pygame.mixer.Channel(8)
chan9 = pygame.mixer.Channel(9)
chan10 = pygame.mixer.Channel(10)
chan11 = pygame.mixer.Channel(11)
chan12 = pygame.mixer.Channel(12)
chan13 = pygame.mixer.Channel(13)
chan14 = pygame.mixer.Channel(14)
chan15 = pygame.mixer.Channel(15)
chan16 = pygame.mixer.Channel(16)
    
           
channels = [chan0, chan1, chan2, chan3, chan4, chan5, chan6, chan7, chan8, chan9, chan10, chan11, chan12, chan13, chan14, chan15, chan16]

def initialize():
    
    
    pass
    
    
    
    
    
    #music.load("C:\Users\Michael\Desktop\University of Iowa Piano Samples\Wav" +"\\" + pianoNotes[0])
    #music.load("C:\MY STUFF\MY PROGRAMS\Eclipse\MusicCompose\\backinblack.ogg")   

    #music.play()
    
    #print "just played it"

# Generates a permutation matrix, which has exactly one 1 in every row/column and 0s everywhere else. 
# Used for generating a probability matrix
def generatePermMatrix(size):
    
    # Create the permutation matrix by selecting numbers from the set [0, 1, ..., n] and those will be the columns where we drop the 1s for each row
    
    numbers = []
    
    permArray = zeros((size, size))
    
    #print permArray
    #sys.exit()
    
    for i in range(size): 
        
        numbers.append(i)
        
    for i in range(size): 
        
        index = choice(numbers)
        permArray[i][index] = 1
        numbers.remove(index)
        
    permMatrix = matrix(permArray)
    return permMatrix 
    
# Generates a square Matrix (array) such that the values of the rows and columns all add up to 1. 
# This will be used to probababilistically determine the next chord in the song, based on the previous 3 chords. 

# In order to do this, Max informed me that you need n(n-1)/2 nxn permutation matrices (a single 1 in each column/row and 0 otherwise). Take a linear combination of them
# such that the coefficients SUM to one (normalize them), where the coefficients are generated randomly, and the resulting matrix will be the kind that we require.      
     
def generateCumulativeArray(size):
    
    global identityMatrix
    
    numberOfMatrices = (size * (size - 1)) / 2     
    permMatrices = range(numberOfMatrices)
       
    for i in range(numberOfMatrices): 
        
        permMatrices[i] = generatePermMatrix(size)
    
    # Create and normalize coefficients
    coefficients = []
    
    SUM = 0
    for i in range(numberOfMatrices): 
        newValue = float(randint(0,9))
        coefficients.append(newValue)
        SUM += newValue
    
    for i in range(numberOfMatrices):
        coefficients[i] = coefficients[i] / SUM
        
    probMatrix = matrix(zeros((size, size)))       
               
    for i in range(numberOfMatrices) :  
        
        probMatrix += coefficients[i] * permMatrices[i]
                
    # Generate a cumulative matrix too, which will be used for probability calculations (cumulative density function instead of prob
    # density function
    
    probArray= array(probMatrix)
    cumulativeArray = zeros((size, size))       
    
    for i in range(size):
        SUM = 0
        for j in range(size):
            SUM += probArray[i][j]         
            cumulativeArray[i][j] += SUM
    
    return cumulativeArray

def transitionToNextState(prevState):
    
    
    
    
    nextCumulateiveArray_noteLength = generateCumulativeArray(6)
    nextCumulativeArray_noteValue = generateCumulativeArray(83)
    
    prevNote = prevState.
    
    
def applyStochasticTransition(prevValue, nextCumulativeArray):     
    
    # The random seed determining where we fall in the probability matrix
    randNumber = float(randrange(0, 1000))/1000
    
    # Determine next note value
    nextValue = 0 # Placeholder
    
    for j in range(nextCumulativeArray_noteValue.shape[0]):
                
        if randNumber <= noteValueCumulativeArray[prevValue][j] and randNumber > ( noteValueCumulativeArray[prevValue][j-1] or 0): 
            nextValue = j
            break
        
    
def main():    
    
    global beatDivisions
    
    initialize()    
   
   
    runDisplay()


class state: 
    
    # State contains all the relevant variables at time = t. 
    
    def __init__(self, t, chord, instruments):
        
        self.instruments = instruments
        self.t = t
        self.notes = notes
        self.chord = chord
        
    def updateState(self):
        for instrument in self.instruments: 
            instrument.play()
            
            
class Instrument: 
    
    # Contains the names of the soundfiles used for that instrument, and a boolean variables which says whether the instrument is currently playing or not, and
    # a list of the notes it is currently playing. 
    
    def __init__(self, instrumentType, t):
        self.instrumentType = instrumentType
        self.t = t
        self.playing = False
        self.notesBeingPlayed = []
        
        if self.instrumentType == "Piano": 
            self.notes = {0:"Piano.mf.C1", 1:"Piano.mf.Db1", 2:"Piano.mf.D1", 3:"Piano.mf.Eb1", 4:"Piano.mf.E1", 5:"Piano.mf.F1", 6:"Piano.mf.Gb1",
             7:"Piano.mf.G1", 8:"Piano.mf.Ab1", 9:"Piano.mf.A1", 10:"Piano.mf.Bb1", 11:"Piano.mf.B1", 
             12:"Piano.mf.C2", 13:"Piano.mf.Db2", 14:"Piano.mf.D2", 15:"Piano.mf.Eb2", 16:"Piano.mf.E2", 17:"Piano.mf.F2", 18:"Piano.mf.Gb2",
             19:"Piano.mf.G2", 20:"Piano.mf.Ab2", 21:"Piano.mf.A2", 22:"Piano.mf.Bb2", 23:"Piano.mf.B2", 
             24:"Piano.mf.C3", 25:"Piano.mf.Db3", 26:"Piano.mf.D3", 27:"Piano.mf.Eb3", 28:"Piano.mf.E3", 29:"Piano.mf.F3", 30:"Piano.mf.Gb3",
             31:"Piano.mf.G3", 32:"Piano.mf.Ab3", 33:"Piano.mf.A3", 34:"Piano.mf.Bb3", 35:"Piano.mf.B3", 
             36:"Piano.mf.C4", 37:"Piano.mf.Db4", 38:"Piano.mf.D4", 39:"Piano.mf.Eb4", 40:"Piano.mf.E4", 41:"Piano.mf.F4", 42:"Piano.mf.Gb4",
             43:"Piano.mf.G4", 44:"Piano.mf.Ab4", 45:"Piano.mf.A4", 46:"Piano.mf.Bb4", 47:"Piano.mf.B4", 
             48:"Piano.mf.C5", 49:"Piano.mf.Db5", 50:"Piano.mf.D5", 51:"Piano.mf.Eb5", 52:"Piano.mf.E5", 53:"Piano.mf.F5", 54:"Piano.mf.Gb5",
             55:"Piano.mf.G5", 56:"Piano.mf.Ab5", 57:"Piano.mf.A5", 58:"Piano.mf.Bb5", 59:"Piano.mf.B5", 
             60:"Piano.mf.C6", 61:"Piano.mf.Db6", 62:"Piano.mf.D6", 63:"Piano.mf.Eb6", 64:"Piano.mf.E6", 65:"Piano.mf.F6", 66:"Piano.mf.Gb6",
             67:"Piano.mf.G6", 68:"Piano.mf.Ab6", 69:"Piano.mf.A6", 70:"Piano.mf.Bb6", 71:"Piano.mf.B6", 
             72:"Piano.mf.C7", 73:"Piano.mf.Db7", 74:"Piano.mf.D7", 75:"Piano.mf.Eb7", 76:"Piano.mf.E7", 77:"Piano.mf.F7", 78:"Piano.pp.Gb7",
             79:"Piano.mf.G7", 80:"Piano.mf.Ab7", 81:"Piano.mf.A7", 82:"Piano.mf.Bb7", 83:"Piano.mf.B7"}
    def playNotes(self, notes):
        
        for note in notes: 
            note.play()
        self.notesBeingPlayed.append(notes)
        
        

class Note: 
    
    # Remaining time: counts down the time left until the note expires (as the result of its length)
    
    def __init__(self, value, length, parentInstrument):
        self.value = value
        self.length = length
        self.parentInstrument = parentInstrument
        self.remainingTime = 0   
        self.playing = False   
            
    def play(self):    
        global channels, soundfileDirectory  
        
        self.remainingTime = length
        self.playing = True
    
        
        sound = pygame.mixer.Sound(soundfileDirectory + self.parentInstrument.notes[self.value] +" render 001.wav")             
        
        channels[0].stop()           
        channels[0].play(sound)
               
        
    def updateNote(self):
        if self.remainingTime - 1/32 > 0: 
                  
            self.remainingTime -= 1/32
        else: 
            self.playing = False

class Chord:
    global notes
        
    # rootNote can either be a letter note ("C") or the integer corresponding to that note, as defined by the global dictionary "notes"
    def __init__(self, rootNote, chordType):
        
        self.type = chordType
        
        self.rootNote = rootNote
        
        self.notes = []
        
        self.relativeNotes = chordTypes[chordType]
        
        for step in self.relativeNotes: 
            self.notes.append(self.rootNote + step)   
               
            
def refreshScreen():
    
    screen.fill((255, 255, 255))
    #drawBackground()
    pygame.display.flip()  
   
        
def runDisplay():
    
    running = True
    
    while (running == True): 
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                running = False
                print("QUIT")
        
            refreshScreen()

        
if __name__ == '__main__':
    main()
