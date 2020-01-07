# 合并去重工具，把两个要合并的答案库复制到answer.txt，去重后的答案库在aa.txt里
f = open("answer.txt","r")

answerMap = {}

line = f.readline()
while line:
    if(len(line)>2):
        print(len(line))
        q = line.split("#")[0]
        a = line.split("#")[1]
        answerMap[q] = a
    line = f.readline()
f.close()

f2 = open("aa.txt","w")
for a in answerMap:
    print(a)
    f2.write(a+"#"+answerMap[a])
f2.close()