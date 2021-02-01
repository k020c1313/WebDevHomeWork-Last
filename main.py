from flask import Flask, render_template,request
import random
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route('/')
def index():
    cpuWord = "りんご"
    SaveAlreadyWordData(["りんご"])
    return render_template(
        "index.html",
        cpuWord = cpuWord,
        wordImage = Image("りんご")
    )


@app.route("/result", methods = ["POST","GET"])  #追加
def result():
    word = request.form["result"]
    cpuWord,message,wordImage = Main(word)
    return render_template(
        "index.html",
        cpuWord = cpuWord,
        message = message,
        wordImage = wordImage
        )

def Main(word):
    message = ""
    cpuWord = ""
    wordImage = ""
    jadge,alreadyWord_list = Jadge(word)
    if jadge == 0:
        alreadyWord_list.append(word)
        cpuWord,wordImage = wordChoice(word)
        alreadyWord_list.append(cpuWord)
        SaveAlreadyWordData(alreadyWord_list)
    else:
        message_list = ["","存在しない単語です。あなたの負けです。","しりとりが成立していません。あなたの負けです。","既出の単語です。あなたの負けです。","「ん」で終わりました。あなたの負けです。"]
        message = message_list[jadge]
    
    return cpuWord,message,wordImage


##単語データを取得
def GetWordData():
    word_dic = {}
    with open("static/word/word.txt", "r", encoding="utf-8") as f:
        file_data = f.readlines()
        for i in file_data:
            key = i[0]
            words = i[2:-1].split(',')
            word_dic[key] = words

    return word_dic


##既出の単語を取得
def GetAlreadyWordData():
    alreadyWord_list = []
    with open("static/word/already.txt") as f:
        file_data = f.readlines()
        for i in file_data:
            alreadyWord_list.append(i.strip())

    return alreadyWord_list
    

##既出の単語を保存
def SaveAlreadyWordData(list):
    with open("static/word/already.txt", mode = "w") as f:
        for i in range(len(list) - 1):
            f.write(list[i] + ",")
        f.write(list[-1])
    

##判定
def Jadge(word):
    convWord = WordConvert(word)
    flag = 0
    ##単語が存在していなかったら
    if SerchWord(word):
        flag = 1
    alreadyWord_list = GetAlreadyWordData()
    ##しりとりが成立していなかったら
    if convWord[0] != WordConvert(alreadyWord_list[-1])[-1]:
        flag = 2
    ##既出の単語だったら
    if word in alreadyWord_list:
        flag = 3
    ##「ん」で終わっていたら
    if convWord[-1] == "ん":
        flag = 4

    return flag,alreadyWord_list


##入力された単語が存在するか確認する
def SerchWord(word):
    flag = False
    url = "https://kotobank.jp/word/" + word
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    a = soup.find('h3')
    if "アクセスしたページが見つかりませんでした" in a.text:
        flag = True

    return flag


##単語をひらがなに変換する
def WordConvert(word):
    from pykakasi import kakasi
    kakasi = kakasi()
    kakasi.setMode('J', 'H')
    kakasi.setMode("K", "H")
    conv = kakasi.getConverter()

    return conv.do(word)  


##相手が出す単語を選択
def wordChoice(word):
    word_dic = GetWordData()
    word = WordConvert(word)
    word_list = word_dic[word[-1]]
    randomNum = random.randint(0,len(word_list) - 1)
    cpuWord = word_list[randomNum]
    wordImage = Image(cpuWord)

    return cpuWord,wordImage


##相手が選択した単語の画像をgoogle画像を検索の結果からスクレイピング
def Image(word):
    Res = requests.get("https://www.google.com/search?hl=jp&q=" + word + "&btnG=Google+Search&tbs=0&safe=off&tbm=isch")
    Soup = BeautifulSoup(Res.text,'html.parser')
    temp = Soup.find_all("img")
    temp.pop(0)
    url = random.choice(temp).get("src")
    
    return url


app.run(host = "0.0.0.0", debug = True)