from random import *
from numpy import *
import sys
import pygame
import time
from pygame.mixer import music

pygame.init()
screen = pygame.display.set_mode((400,400))

# For accessing note values
notes = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}

# For accessing note names
inverseNotes = {v: k for k, v in notes.items()}

beatDivisions = {0:8, 1:4, 2:2, 3:1.5, 4:1, 5:0.75, 6:0.5, 7:0.25, 8:0.125, 9:0.0625, 10:0.03125}


pianoNotes = {0:"Piano.mf.C3", 1:"Piano.mf.Db3", 2:"Piano.mf.D3", 3:"Piano.mf.Eb3", 4:"Piano.mf.E3", 5:"Piano.mf.F3", 6:"Piano.mf.Gb3",
             7:"Piano.mf.G3", 8:"Piano.mf.Ab3", 9:"Piano.mf.A3", 10:"Piano.mf.Bb3", 11:"Piano.mf.B3", 
             12:"Piano.mf.C4", 13:"Piano.mf.Db4", 14:"Piano.mf.D4", 15:"Piano.mf.Eb4", 16:"Piano.mf.E4", 17:"Piano.mf.F4", 18:"Piano.mf.Gb4",
             19:"Piano.mf.G4", 20:"Piano.mf.Ab4", 21:"Piano.mf.A4", 22:"Piano.mf.Bb4", 23:"Piano.mf.B4"}

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
     
def generateProbMatrix(size):
    
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
    cumulativeMatrix = matrix(cumulativeArray)
    
    return probMatrix, cumulativeMatrix

# Generate the next chord using the next chord probability matrix. 
        
def generateNextChord(prevChord, cumulativeMatrix):
    # Generate a random number between 0 and 1. 
    # For each row in the probability matrix (the current note), each element represents the probability of a particular note being chosen next. 
    # Those probabilities can be interpreted as slots, and the randomly generated number will fall into those slots with the probability
    # distribution specified by the matrix. 
    
    prevChordRoot = prevChord.notes[0]    
    
    randNumber = float(randrange(0, 1000))/1000
    cumulativeArray = array(cumulativeMatrix)
    
    size = cumulativeArray.shape[0]
    
    # Iterate through the cumulative matrix and find which "slot" the random number falls in: that will determine the next chord
    nextChordRoot = 0
    
    for j in range(size):
        
        if randNumber <= cumulativeArray[prevChordRoot][j] and randNumber > ( cumulativeArray[prevChordRoot][j-1] or 0): 
            nextChordRoot = j
            break
    
    # Randomly select the type of the next chord
    nextChordType = choice(chordTypes.keys())
    
    nextChord = Chord(nextChordRoot, nextChordType)
    return nextChord  

def generateNextNote(prevNote, currentChord, noteValueCumulativeMatrix, noteLengthCumulativeMatrix):
    
    # Current Chord may or may not be equal to the previous chord
    
    global beatDivisions
    
    prevNoteIndex = prevNote.parentChord.notes.index(prevNote.value)
    
    # The random seed determining where we fall in the probability matrix
    randNumber = float(randrange(0, 1000))/1000
    noteValueCumulativeArray = array(noteValueCumulativeMatrix)
    noteLengthCumulativeArray = array(noteLengthCumulativeMatrix)
    
       
    # Iterate through the cumulative matrix and find which "slot" the random number falls in: that will determine the next chord
    nextNoteValue = 0 # Placeholder
    
    for j in range(noteValueCumulativeArray.shape[0]):
        
        if randNumber <= noteValueCumulativeArray[prevNoteIndex][j] and randNumber > ( noteValueCumulativeArray[prevNoteIndex][j-1] or 0): 
            nextNoteValue = currentChord.notes[j]
            break
        
    nextNoteValue = 
    
    nextNoteLength = 0 # Placeholder
    
    for j in range(noteLengthCumulativeArray.shape[0]):
        
        if randNumber <= noteLengthCumulativeArray[prevNoteValue][j] and randNumber > ( noteLengthCumulativeArray[prevNoteValue][j-1] or 0): 
            nextNoteLength = beatDivisions[j]
            break
    
    nextNote = Note(nextNoteValue, nextNoteLength, nextNotePosition)
                
            
def main():    
    
    global beatDivisions
    
    initialize()    
   
    nextChordProbMatrix, nextChordCumulativeMatrix = generateProbMatrix(12)
    nextNoteLengthProbMatrix, nextNoteLengthCumulativeMatrix = generateProbMatrix(len(beatDivisions))
    
    # The next note value will be picked from the notes contained in the chord, so we need to generate a different prob matrix for the different possible # of notes in
    # a chord (between 3 and 6). When transitioning to a new, bigger chord we can use the prob matrix for that bigger chord (there will be some extra values in the domain
    # but that's okay). When transitioning to a new, smaller chord, use the previous bigger chord otherwise you will get an index error. 
    
    nextNoteValueProbMatrices = []
    nextNoteValueCumulativeMatrices = []
    
    for i in range(3, 7):
        nextNoteValueProbMatrices[i], nextNoteValueCumulativeMatrices[i] = generateProbMatrix(i)    
    
    firstChord = Chord(0, "Major")
    firstNote = Note(0, 1)
    
    prevChord = generateNextChord(firstChord, nextChordCumulativeMatrix)
    
    prevNote = generateNextNote(firstNote, prevChord, nextNoteValueCumulativeMatrices[len(prevChord.notes)], nextNoteLengthCumulativeMatrix)
    for i in range(10): 
        newChord = generateNextChord(prevChord, nextChordCumulativeMatrix)        
        newNote = generateNextNote(prevNote, newChord, nextNoteValueCumulativeMatrices[len(prevChord.notes)], nextNoteLengthCumulativeMatrix)
        print newChord.notes, newChord.rootNoteName, newChord.type
        
        
        prevChord = newChord
    
       
    
   
    runDisplay()
   
class Note: 
    def __init__(self, value, length, parentChord):
        self.value = value
        self.length = length        
        self.parentChord = parentChord        
        self.positionInChord = value - parentChord.notes[0]
        
    def play(self):    
        global channels        
        
        sounds = pygame.mixer.Sound("C:\Users\Michael\Desktop\University of Iowa Piano Samples\WAV\AlignedFiles2" +"\\" + pianoNotes[note] +" render 001.wav")             
        
        channels[0].stop()           
        channels[0].play(sound)
        
        # Note length determines how long we sleep here
        time.sleep(self.length)

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
