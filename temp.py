import json

input_file = open ('url.json')
json_array = json.load(input_file)
store_list = []

# print(len(json_array))
index = 0

result = []
for index in range(2,len(json_array),3):
    link = json_array[index][""]
    if "|" in link:
        link = link.split("|")[0]
    if link not in result:
        result.append(link)

fp = open("result.json","w")
json.dump(result,fp)
fp.close()