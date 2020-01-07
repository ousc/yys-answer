from selenium import webdriver
import time
from pyquery import pyquery as pq


options = webdriver.ChromeOptions()
options.add_argument('user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"')
# 模拟iphone6

while True:
    wd = webdriver.Chrome(options=options)

    wd.get("https://act.ds.163.com/93dcd3b7a7f888e6/")    # 打开平安京学历测试

    time.sleep(2)   #等待1秒

    wd.find_element_by_class_name("btn-start").find_element_by_tag_name("img").click() # 点击开始参与
    wd.find_element_by_class_name("dialog").find_element_by_class_name("dialog-inner").find_element_by_class_name("toolbars").find_elements_by_tag_name("div")[0].click() # 点击先随便试试

    while True:
        time.sleep(1)   #等待1秒
        try:
            question = wd.find_element_by_class_name("question").text #题目
            question = question.split("\n")[0]
        except:
            time.sleep(3)   #等待2秒
            question = wd.find_element_by_class_name("question").text #题目
            question = question.split("\n")[0]
        anwser = ""
        f = open("answer.txt","a+")
        line = f.readline()
        exist_flag = False # 是否已经有答案了
        while line:
            q = line.split("-")[0]
            a = line.split("-")[0]
            line = f.readline()
            if(q) == question:
                anwser = a
                exist_flag = True

        anwser_items = wd.find_elements_by_class_name("answer-item")
        if(exist_flag):
            for anwser_item in anwser_items:
                if(anwser_item.text == anwser):
                    anwser_item.click()
        else:
            anwser_items[0].click()
            time.sleep(1)   #等待2秒
            try:
                index = 0
                for anwser_item in anwser_items:
                    print(anwser_item.get_attribute("class"))
                    if(anwser_item.get_attribute("class") == "answer-item correct"):
                        anwser = anwser_item.text
                        print(question+"-"+anwser)
                        f.write(question+"-"+anwser+"\n")
                if(anwser_items[0].get_attribute("class") != "answer-item correct"):
                    break
            except:
                time.sleep(3)   #等待2秒
                index = 0
                for anwser_item in anwser_items:
                    print(anwser_item.get_attribute("class"))
                    if(anwser_item.get_attribute("class") == "answer-item correct"):
                        anwser = anwser_item.text
                        print(question+"-"+anwser)
                        f.write(question+"-"+anwser+"\n")
                if(anwser_items[0].get_attribute("class") != "answer-item correct"):
                    break
        f.close()
        time.sleep(2)   #等待2秒
    wd.quit()   #关闭浏览器