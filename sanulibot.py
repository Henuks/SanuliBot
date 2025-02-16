def colorMatch(x,y,color):
    testcolor=pyautogui.pixel(x,y)
    if testcolor==color:
        return True
    return False
import pyautogui
import time
import random
import keyboard
import os
import requests
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0
if not os.path.isfile(os.path.join(os.path.abspath(os.path.dirname(__file__)),"kaikkisanat.txt")):
    print("Asennetaan...",end="")
    f=open(os.path.join(os.path.abspath(os.path.dirname(__file__)),"kaikkisanat.txt"),'w',encoding="utf-8")
    f.write(requests.get("https://raw.githubusercontent.com/hugovk/everyfinnishword/refs/heads/master/kaikkisanat.txt").text)
    f.close()
                                                           
rawwordlist=open(os.path.join(os.path.abspath(os.path.dirname(__file__)),"kaikkisanat.txt"),"r",encoding="utf-8").read().split("\n")
wordlist=set()
lettercount=5
cancelimport=False
for word in rawwordlist:
    if word.isalpha() and len(word)==lettercount:
        for char in word:
            if not char in "abcdefghijklmnopqrstuvwxyzäö":
                cancelimport=True
        if not cancelimport:
            wordlist.add(word)
nochar=(18, 18, 18)
wrongchar=(62, 62, 62)
possiblechar=(201, 180, 88)
correctchar=(106, 170, 100)

print("Press space to set corner 1 and 2")
while not keyboard.is_pressed('space'):
    time.sleep(0.01)
pos1x, pos1y = pyautogui.position()
while keyboard.is_pressed('space'):
    time.sleep(0.01)
while not keyboard.is_pressed('space'):
    time.sleep(0.01)
pos2x, pos2y = pyautogui.position()
while keyboard.is_pressed('space'):
    time.sleep(0.01)
while not keyboard.is_pressed('space'):
    time.sleep(0.01)
pos3x, pos3y = pyautogui.position()
while keyboard.is_pressed('space'):
    time.sleep(0.01)
possiblewords=set()
grid = [[[0,0],[0,0],[0,0],[0,0],[0,0]],[[0,0],[0,0],[0,0],[0,0],[0,0]],[[0,0],[0,0],[0,0],[0,0],[0,0]],[[0,0],[0,0],[0,0],[0,0],[0,0]],[[0,0],[0,0],[0,0],[0,0],[0,0]],[[0,0],[0,0],[0,0],[0,0],[0,0]]]
for x in range(5):
    for y in range(6):
        grid[y][x][0]=int(pos1x+((pos2x-pos1x)/4)*x)
        grid[y][x][1]=int(pos1y+((pos2y-pos1y)/5)*y)

print("Press space to start")
while not keyboard.is_pressed('space'):
    time.sleep(0.01)
while keyboard.is_pressed('space'):
    time.sleep(0.01)
time.sleep(1)
correct=False
while True:
    wrongchars=[]
    correctchars="*"*lettercount
    possiblechars=[]
    typedwords=[]
    del typedwords[:]
    while True:
        wrongchars=[]
        correctchars="*"*lettercount
        possiblechars=[]
        if keyboard.is_pressed('space'):
            quit()
        word=None
        if len(typedwords)==0:
            word="kaste"
        else:
            for wordi in range(6):
                for chari in range(5):
                    try:
                        if colorMatch(grid[wordi][chari][0],grid[wordi][chari][1],wrongchar):
                            if typedwords[wordi][chari] not in wrongchars:
                                wrongchars.append(typedwords[wordi][chari])
                        elif colorMatch(grid[wordi][chari][0],grid[wordi][chari][1],possiblechar):
                            possiblechars.append((chari,typedwords[wordi][chari]))
                        elif colorMatch(grid[wordi][chari][0],grid[wordi][chari][1],correctchar):
                            correctchars=correctchars[:chari]+typedwords[wordi][chari]+correctchars[chari+1:]
                    except:
                        pass
        possiblewords=set()
        for word in wordlist:
            cancel=False
            word2=word
            for pc in possiblechars:
                if (pc[1] not in word2) or ((pc[1] in word2) and (word2[pc[0]] == pc[1])):
                    cancel=True
            for i in range(5):
                if correctchars[i] != '*':
                    if word2[i] == correctchars[i]:
                        word2=word2[:i]+' '+word2[i+1:]
                    else:
                        cancel=True
            word2=word2.replace(" ","")
            for char in word2:
                if char in wrongchars and char not in [el[1] for el in possiblechars]:
                    cancel=True
            if not cancel:
                possiblewords.add(word)
        word=random.choice(list(wordlist))
        try:
            word=possiblewords.pop()
        except:
            pass
        if word=="":
            print("--------------")
            print("No possible words")
            print(wrongchars)
            print(possiblechars)
            print(correctchars)
            print(len(possiblewords))
            print(word)
            print(typedwords)
            continue
        typedwords.append(word)
        print("--------------")
        print(wrongchars)
        print(possiblechars)
        print(correctchars)
        print(len(possiblewords))
        print(word)
        print(typedwords)
        keyboard.write(word,delay=0.01)
        time.sleep(0.01)
        pyautogui.press('enter')
        time.sleep(0.01)
        try:
            if colorMatch(grid[len(typedwords)][0][0],grid[len(typedwords)][0][1],nochar):
                wordlist.remove(word)
                pyautogui.press(['backspace', 'backspace', 'backspace', 'backspace','backspace'],interval=0.01)
                time.sleep(0.01)
                typedwords.pop()
        except:
            pass
        if colorMatch(pos3x,pos3y,correctchar):
            pyautogui.press('enter')
            print("Correct")
            correct=True

        if correct:
            print("correct")
            correct=False
            del typedwords
            break