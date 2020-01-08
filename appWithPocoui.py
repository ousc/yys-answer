# -*- encoding=utf8 -*-
__author__ = "sundaiyue"
import re
from airtest.core.api import *

from poco.drivers.android.uiautomation import AndroidUiautomationPoco

while True:
    # 导入答案
    answerMap = {}
    f = open("answer.txt", "r")
    line = f.readline()
    while line and line != "":
        if (len(line) > 2):
            q = line.split("#")[0]
            a = line.split("#")[1]
            answerMap[q] = a
            line = f.readline()
    f.close()
    print("导入完成")
    ff = open("answer.txt","a+")

    poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)



    while True:
        try:
            poco("android.widget.LinearLayout").offspring("app").child("android.view.View").child("android.view.View")[
                7].child(
                "android.widget.Image").click()

            time.sleep(2)  # 等待2秒
        except:
            pass

        question = poco("android.widget.LinearLayout").offspring("app").child("android.view.View")[1].child("android.view.View")[
            1].get_text()
        choice1 = poco("android.widget.LinearLayout").offspring("app").child("android.view.View")[1].child("android.view.View")[
            3]
        choice2 = poco("android.widget.LinearLayout").offspring("app").child("android.view.View")[1].child("android.view.View")[
            4]
        choice3 = poco("android.widget.LinearLayout").offspring("app").child("android.view.View")[1].child("android.view.View")[
            5]
        try:
            choice4 = poco("android.widget.LinearLayout").offspring("app").child("android.view.View")[1].child("android.view.View")[
                6]
        except:
            choice4 = None
        choices_text = [choice1.get_text().replace("A. ",""),choice2.get_text().replace("B. ",""),choice3.get_text().replace("C. ","")]
        if(choice4 != None):
            choices_text.append(choice4.get_text().replace("D. ",""))

        choices_text = [i.encode("GBK") for i in choices_text]
        choices_text.sort()
        choices_text = [i.decode("GBK") for i in choices_text]

        for choice in choices_text:
            question += "|"
            question += choice
        print(question)

        if(answerMap.get(question) != None): # 如果找到答案，根据答案点击正确答案，继续答下一题
            answer = re.sub('[\n]+', '', answerMap[str(question)])
            print("找到答案，本题答案为" + answerMap[str(question)])

            have = False
            if (str(choice1.get_text()).find(answer) != -1):
                choice1.click()
            if (str(choice2.get_text()).find(answer) != -1):
                choice2.click()
            if (str(choice3.get_text()).find(answer) != -1):
                choice3.click()
            if (choice4 != None):
                if (str(choice4.get_text()).find(answer) != -1):
                    choice4.click()

        else: # 否则默认选第一个，把正确答案加入答案库
            choice1.click()
            time.sleep(1)
            if(len(choice1.child("android.view.View"))==2):
                print(choice1.child("android.view.View").get_size()[0])
                if(choice1.child("android.view.View").get_size()[0] != 0.18055555555555555):
                    answer = choices_text[0]
                    print("添加：" + question + "-" + answer)
                    ff.write(question + "#" + answer + "\n")
                    answerMap[str(question)] = str(answer)
            if(len(choice2.child("android.view.View"))==2):
                print(choice2.child("android.view.View").get_size()[0])
                if(choice2.child("android.view.View").get_size()[0] == 0.18055555555555555):
                    answer = choices_text[1]
                    print("添加：" + question + "-" + answer)
                    ff.write(question+"#"+answer+"\n")
                    answerMap[str(question)] = str(answer)
            if(len(choice3.child("android.view.View"))==2):
                print(choice3.child("android.view.View").get_size()[0])
                if(choice3.child("android.view.View").get_size()[0] == 0.18055555555555555):
                    answer = choices_text[2]
                    print("添加：" + question + "-" + answer)
                    ff.write(question+"#"+answer+"\n")
                    answerMap[str(question)] = str(answer)
            if(choice4 != None):
                if (len(choice4.child("android.view.View")) == 2):
                    print(choice4.child("android.view.View").get_size()[0])
                    if (choice4.child("android.view.View").get_size()[0] == 0.18055555555555555):
                        answer = choices_text[3]
                        print("添加：" + question + "-" + answer)
                        ff.write(question + "#" + answer + "\n")
                        answerMap[str(question)] = str(answer)
            ff.close()
            try:
                time.sleep(1)
                poco("android.widget.LinearLayout").offspring("app").child("android.view.View")[2].child("android.view.View").child(
                    "android.view.View")[3].click()
                time.sleep(1)
                poco("android.widget.LinearLayout").offspring("app").child("android.view.View").child("android.view.View")[
                    11].child("android.widget.Image").click()
                time.sleep(1)
            except:
                continue