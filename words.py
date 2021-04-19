alphabet="abcdefghijklmnopqrstuvwxyz"
letterfrequency={'a': 0.1032, 'b': 0.01602, 'c': 0.03807, 'd': 0.0238, 'e': 0.1415,
                 'f': 0.01277, 'g': 0.01811, 'h': 0.01439, 'i': 0.10517, 'j': 0.00194,
                 'k': 0.001, 'l': 0.04619, 'm': 0.02782, 'n': 0.08122, 'o': 0.07062,
                 'p': 0.02523, 'q': 0.00546, 'r': 0.08588, 's': 0.06927, 't': 0.05263,
                 'u': 0.03972, 'v': 0.01021, 'w': 0.00033, 'x': 0.00224, 'y': 0.00545,
                 'z': 0.00178}
total=0
with open("dictionary.txt","r") as file:
    for word in file:
        word=word[:-2]
        for i in word:
            letterfrequency[i.lower()]+=1
            total+=1

for i in letterfrequency:
    letterfrequency[i]=round(letterfrequency[i]/total,5)

print("letterfrequency=%s"%letterfrequency)