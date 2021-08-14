import requests
import json
import time
from wordcloud import WordCloud
import PIL.Image as image
import jieba
import jieba.posseg
import numpy as np
import stylecloud
import palettable
import re
import collections

def get_info(roomid):
    url = "https://api.live.bilibili.com/xlive/web-room/v1/dM/gethistory?roomid=" + roomid
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67",
        "referer": "https://live.bilibili.com/"
    }
    data = {
        "roomid": roomid
    }
    req = requests.post(url, data=data, headers=headers)
    obj = json.loads(req.text)['data']['room']
    for msg in obj:
        line = msg['text'] + ' === ' + msg['nickname'] + ' === ' + msg['timeline'] + '\n'
        with open('./message/' + roomid + '_msg.txt', 'a+', encoding='utf-8') as log:
            log.seek(0)
            lines = log.readlines()
            if line not in lines:
                log.write(line)
                with open('./message/' + roomid + '_danmu.txt', 'a+', encoding='utf-8') as f:
                    f.write(msg['text']+'\n')


def get_word_list(roomid):
    with open('./message/' + roomid + '_danmu.txt', 'r', encoding='utf-8') as f:
        string_data = f.read()
        # 文本预处理
        pattern = re.compile(u'\t|\n|\.|-|:|;|\)|\(|\?|"') # 定义正则表达式匹配模式（空格等）
        string_data = re.sub(pattern, '', string_data)     # 将符合模式的字符去除
        jieba.suggest_freq('艾露露', True)
        jieba.suggest_freq('我爱你', True)

        # 文本分词
        seg_list_exact = jieba.cut(string_data, cut_all=False, HMM=True)    # 精确模式分词+HMM
        object_list = []
        for word in seg_list_exact:         # 循环读出每个分词
            object_list.append(word)    # 分词追加到列表
        # 词频统计
        word_counts = collections.Counter(object_list)       # 对分词做词频统计
        return word_counts


def show_img(roomid):
    word_count = get_word_list(roomid)
    # print(word_count)
    mask = np.array(image.open('./image/111.jpg'))
    wdcld = WordCloud(
        mask = mask,
        scale = 5,
        font_path= './fonts/汉仪PP体简.ttf',
        colormap='hot',
        max_words=1000,
        background_color='#070707',
        min_font_size=4
    ).generate_from_frequencies(word_count)
    img = wdcld.to_image()
    img.save(roomid + '_img.jpg')

def use_stylecloud_show_img(roomid):
    word_count = get_word_list(roomid)
    print(word_count)
    stylecloud.gen_stylecloud(
        text = word_count,
        icon_name = 'fas fa-paw',
        font_path = './fonts/汉仪PP体简.ttf',
        output_name = roomid + '_wordcloud.png',

        background_color= 'black',
        size = 1024,
        max_words=200,
        stopwords=True,
        # gradient='vertical',
    )

if __name__ == '__main__':
    roomid = input("请输入直播间ID:")
    choose = input("是否获取直播间弹幕[Y/N]:")
    if(choose == 'Y' or choose == 'y'):
        while True:
            get_info(roomid)
            time.sleep(5)

    if(choose == 'N' or choose == 'n'):
        style = input("选择生成模式[1/2]:")
        if(style == '1'):
            show_img(roomid)
        elif(style == '2'):
            use_stylecloud_show_img(roomid)
    else:
        pass
