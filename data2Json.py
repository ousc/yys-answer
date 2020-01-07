import json
import re
f = open("answer.txt","r")

answer_arr = []

line = f.readline()
while line:
    if(len(line)>2):
        q_and_choices  = line.split("#")[0].split("|")
        q = q_and_choices[0]
        c = q_and_choices[1:]
        c = '、'.join(str(i) for i in c)
        a = re.sub('[\n]+', '', line.split("#")[1])
        data = {"question":q, "answer":a, "choices":c}
        answer_arr.append(data)
    line = f.readline()
f.close()

f2 = open("answer.json","w")
str_json = json.dumps( answer_arr,ensure_ascii=False)
f2.write(str(str_json))
f2.close()
