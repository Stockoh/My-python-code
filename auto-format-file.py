import sys
import re

pathfile = r"C:\Users\theod\Downloads\golly\golly-4.0-win-64bit\My Scripts\torulestringOT.py"

otherfile = "file.py" if pathfile != "file.py" else "file1.py"


with open(pathfile, "r") as file:
    with open(otherfile, "w") as new:
        for line in file:
            pattern = re.compile(r"[^\t\n]")
            if not pattern.findall(line[:-1]):
                new.write("\n")
            else:
                new.write(line)


with open(pathfile, "w") as file:
    with open(otherfile, "r") as new:
        for line in new:
            file.write(line)


def formatimport(lines):
    listmodule = []
    importpattern = re.compile(
        r"((import )(\S+)((as )(\S+)?))|((from )(\S+)( import )(\S+))")
    for line in lines:
        if importpattern.findall(line)[2]:
            listmodule.append((line, importpattern.findall(line)[2]))
        else:
            listmodule.append((line, importpattern.findall(line)[9]))
    listmodule.sort(lambda x: x[1])
