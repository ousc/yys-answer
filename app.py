from selenium import webdriver
import time
from pyquery import pyquery as pq
import re

options = webdriver.ChromeOptions()
options.add_argument('user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"')
# 模拟iphone6

while True:
    index = 0
    #导入答案
    answerMap = {}
    f = open("answer.txt","r")
    line = f.readline()
    while line and line!="":
        if(len(line)>2):
            q = line.split("#")[0]
            a = line.split("#")[1]
            answerMap[q] = a
            line = f.readline()
    f.close()
    print("导入完成")

    ff = open("answer.txt","a+")

    wd = webdriver.Chrome(options=options)
    wd.get("https://act.ds.163.com/93dcd3b7a7f888e6/")    # 打开平安京学力测试

    time.sleep(2)   #等待1秒

    wd.find_element_by_class_name("btn-start").find_element_by_tag_name("img").click() # 点击开始参与
    wd.find_element_by_class_name("toolbars").find_elements_by_tag_name("div")[0].click() # 点击先随便试试

    while True:
        time.sleep(1)   #等待1秒
        try:
            question = wd.find_element_by_class_name("question").text # 获得题目
            question = question.split("\n")[0] # 去除题目作者信息

            choices = []
            answer_items = wd.find_elements_by_class_name("answer-item") # 获取所有选项
            for answer_item in answer_items:
                choices.append(answer_item.text.split(" ")[1])
            choices = [i.encode("GBK") for i in choices]
            choices.sort()
            choices = [i.decode("GBK") for i in choices]
            for choice in choices:
                question = question + "|" + choice
        except:
            continue

        if(answerMap.get(question) != None): # 如果找到答案，根据答案点击正确答案，继续答下一题
            answer = re.sub('[\n]+', '', answerMap[str(question)])
            print("找到答案，本题答案为" + answerMap[str(question)])

            have = False

            for answer_item in answer_items:
                if(str(answer_item.text).find(answer)!= -1 or str(answer_item.text) == answer):
                    have = True
                    try:
                        answer_item.click()
                    except:
                        continue
                    break
            if(not have): # 一题多解情况
                answer_items[0].click()
                answerMap[str(question)] = answer + "&" + str(answer_item.text)


        else: # 否则默认选第一个，把正确答案加入答案库
            answer_items = wd.find_elements_by_class_name("answer-item") # 获取选项
            answer_items[0].click()
            time.sleep(1)   #等待1秒
            try:
                answer_items = wd.find_elements_by_class_name("answer-item") # 获取选项
            except:
                time.sleep(3)   #等待3秒
                answer_items = wd.find_elements_by_class_name("answer-item") # 获取选项
            for answer_item in answer_items:
                if(answer_item.get_attribute("class") == "answer-item correct"):
                    answer = str(answer_item.text).split(" ")[1]
                    print("添加："+question+"-"+answer)
                    ff.write(question+"#"+answer+"\n")
                    answerMap[str(question)] = str(answer)
            if(answer_items[0].get_attribute("class") != "answer-item correct"):
                break
        f.close()
        time.sleep(2)   #等待2秒
        index += 1
        if(index == 10):
            break

    wd.quit()   #关闭浏览器