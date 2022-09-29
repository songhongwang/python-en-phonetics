import fileinput
import eng_to_ipa as p 
import pyttsx3
import re
import html
from urllib import parse
import requests
import os

# data.txt 格式如下
# 英文 翻译或者注释
# one 一个
# good luck 祝你好运

# data2.txt 添加音标以后的数据
# one 一个
# good luck 祝你好运

GOOGLE_TRANSLATE_URL = 'http://translate.google.cn/m?q=%s&tl=%s&sl=%s'
def translate(text, to_language="auto", text_language="auto"):
    text = parse.quote(text)
    url = GOOGLE_TRANSLATE_URL % (text,to_language,text_language)
    print("***" + url)
    response = requests.get(url)
    data = response.text
    expr = r'(?s)class="(?:t0|result-container)">(.*?)<'
    result = re.findall(expr, data)
    if (len(result) == 0):
        return ""
    return html.unescape(result[0])


def savePhonetics(phonetics):
    f = open("data2.txt","a+",encoding='utf-8')
    f.writelines(phonetics + "\n")
    f.close()

if __name__=='__main__':
    if os.path.exists('data2.txt'):
        print('data2.txt已经存在')


    print("\033[0;32;40m\tPlease put your sentences in data.txt.\033[0m")
    engine = pyttsx3.init()

    # 设置语速
    engine.setProperty("rate", 195)


    i = 0
    for line in open('data.txt',encoding='utf-8'):
        if line[0] != '-' and line != '\n':
            i += 1
            arr = re.split(r'\s',line)
            sentence = arr[0]
            extra = arr[1]
            print("===" + sentence + " == " + extra)
            phonetics = p.convert(sentence)
            print("\033[0;35;40m\t"+sentence+"\033[0m",'    ',i)
            print("\033[0;37;40m\t"+phonetics+"\033[0m")
            print("\033[0;36;40m\t"+translate(sentence,"zh-CN","en")+"\033[0m")
            savePhonetics(sentence + " [" +phonetics + "] " + extra)
            engine.say(sentence)
            engine.runAndWait()
            # input()
            print('-----------------------------------------------------------Press Enter')

main()