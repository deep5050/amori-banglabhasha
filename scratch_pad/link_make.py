from os import walk
import re
f = []

links = open("links.md","w")

mypath = "./stories/prothomalo"
from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

text = ""
for filenames in onlyfiles:
    text=text+f"1. [{filenames.split('.')[0]}]({mypath}/{filenames})\n\n"

links.write(text)
links.close()

data =""
target_md = open("README.md",'r')
data = target_md.read()
data = re.sub(r'<!-- links-start -->.*?<!-- links-end -->', f'<!-- links-start -->\n{text}\n<!-- links-end -->', data,
                      flags=re.DOTALL)

target_md.close()

new_target = open("README.md",'w')
new_target.write(data)
new_target.close()