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
    while line:
        if (len(line) > 2):
            q = line.split("#")[0]
            a = line.split("#")[1]
            answerMap[q] = a
        line = f.readline()
    f.close()
    print("导入完成")

    poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)



    index = 1 #记录当前题目序号
    while True:
        print("第"+str(index)+"题")
        index += 1
        try: #点击开始按钮，若已经进入做题状态则跳过
            poco("android.widget.LinearLayout").offspring("app").child("android.view.View").child("android.view.View")[
                7].child(
                "android.widget.Image").click()

            time.sleep(2)  # 等待2秒
        except:
            pass

        #获取题目和选项
        question = poco("android.widget.LinearLayout").offspring("app").child("android.view.View")[1].child("android.view.View")[
            1].get_text()
        choice1 = poco("android.widget.LinearLayout").offspring("app").child("android.view.View")[1].child("android.view.View")[
            3]
        choice2 = poco("android.widget.LinearLayout").offspring("app").child("android.view.View")[1].child("android.view.View")[
            4]
        try:
            choice3 = poco("android.widget.LinearLayout").offspring("app").child("android.view.View")[1].child(
                "android.view.View")[5]
        except:
            choice3 = None
        try:
            choice4 = poco("android.widget.LinearLayout").offspring("app").child("android.view.View")[1].child("android.view.View")[
                6]
        except:
            choice4 = None

        # 将选项排序，加入题干
        choices_text = [choice1.get_text().replace("A. ",""),choice2.get_text().replace("B. ","")]
        if(choice3 != None):
            choices_text.append(choice3.get_text().replace("C. ", ""))
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
            if (re.sub('[\n]+', '', str(choice1.get_text())).replace("A. ","")==answer):
                choice1.click()
            if (re.sub('[\n]+', '', str(choice2.get_text())).replace("B. ","")==answer):
                choice2.click()
            if (choice3 != None):
                if (re.sub('[\n]+', '', str(choice3.get_text())).replace("C. ","")==answer):
                    choice3.click()
            if (choice4 != None):
                if (re.sub('[\n]+', '', str(choice4.get_text())).replace("D. ","")==answer):
                    choice4.click()

        else: # 否则默认选第一个，把正确答案加入答案库
            sizeW = [] #记录选项选错后后面图标的长和宽，长/宽较大的为正确答案
            while(len(sizeW)==0): #有时因不明原因choice.click()无效，最终加入这个奇怪的东西保证不会卡住
                choice1 = poco("android.widget.LinearLayout").offspring("app").child("android.view.View")[1].child(
                    "android.view.View")[
                    3]
                choice2 = poco("android.widget.LinearLayout").offspring("app").child("android.view.View")[1].child(
                    "android.view.View")[
                    4]
                try:
                    choice3 = poco("android.widget.LinearLayout").offspring("app").child("android.view.View")[1].child(
                        "android.view.View")[5]
                except:
                    choice3 = None
                try:
                    choice4 = poco("android.widget.LinearLayout").offspring("app").child("android.view.View")[1].child(
                        "android.view.View")[6]
                except:
                    choice4 = None
                choice1.click()
                time.sleep(2)
                which = 0
                if(len(choice1.child("android.view.View"))==2):
                    size = choice1.child("android.view.View")[1].get_size()
                    print(size,choices_text[0])
                    sizeW.append({"name":0,"size":size[0]/size[1]})

                if(len(choice2.child("android.view.View"))==2):
                    size = choice2.child("android.view.View")[1].get_size()
                    print(size,choices_text[1])
                    sizeW.append({"name":1,"size":size[0]/size[1]})

                if(choice3 != None):
                    if(len(choice3.child("android.view.View"))==2):
                        size = choice3.child("android.view.View")[1].get_size()
                        print(size,choices_text[2])
                        sizeW.append({"name":2,"size":size[0]/size[1]})


                if(choice4 != None):
                    if(len(choice4.child("android.view.View"))==2):
                        size = choice4.child("android.view.View")[1].get_size()
                        print(size,choices_text[3])
                        sizeW.append({"name":3,"size":size[0]/size[1]})

            if(sizeW[0]['size']>sizeW[1]['size']):
                which = sizeW[0]['name']
            else:
                which = sizeW[1]['name']

            answer = choices_text[which]

            print("添加：" + question + "#" + answer)

            ff = open("answer.txt", "a+")
            ff.write(question + "#" + answer + "\n") # 写入答案
            ff.close()
            answerMap[str(question)] = str(answer)

            try:#跳过答题结束后的几个对话框
                time.sleep(1)
                poco("android.widget.LinearLayout").offspring("app").child("android.view.View")[2].child("android.view.View").child(
                    "android.view.View")[3].click()
                time.sleep(1)
                poco("android.widget.LinearLayout").offspring("app").child("android.view.View").child("android.view.View")[
                    11].child("android.widget.Image").click()
                time.sleep(1)
                index = 1
            except:
                continue