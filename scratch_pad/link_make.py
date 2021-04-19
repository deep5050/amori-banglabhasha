from os import walk

f = []

links = open("links.md","w")

mypath = "./stories/prothomalo"
from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]


for filenames in onlyfiles:
    links.write(f"1. [{filenames.split('.')[0]}]({mypath}/{filenames})\n\n")
links.close()
