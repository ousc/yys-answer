import json
import re
f = open("answer.txt","r")

answer_arr = []

line = f.readline()
while line:
    if(len(line)>2):
        q = line.split("#")[0]
        a = re.sub('[\n]+', '', line.split("#")[1])
        data = {"question":q, "answer":a}
        answer_arr.append(data)
    line = f.readline()
f.close()

f2 = open("answer.json","w")
str_json = json.dumps( answer_arr,ensure_ascii=False)
f2.write(str(str_json))
f2.close()