from pynput.mouse import Controller,Button
from time import sleep


mouse = Controller()
coordspinceau = []

for i in range(2):
    input()
    coordspinceau.append(mouse.position)

print("coordspinceau = "+str(coordspinceau))
    
