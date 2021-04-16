from time import sleep

import random
import pandas as pd

import requests
from bs4 import BeautifulSoup
import re
import json

#from urllib.request import urlopen
#from urllib.error import URLError, HTTPError
import urllib.request
import urllib.parse

import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options


path = 'C:/Users/thekoo/OneDrive - konkuk.ac.kr/song_data.csv'

def make_random_id(): 
    #랜덤으로 8자리 song_id 생성
    #csv 파일과 겹치지 않는 range(song_id, song_id+100) 리스트 생성
    second = "12"
    pool = "0123456789"
    
    song_id = "3"
    song_id += random.choice(second)
    
    
    for i in range(6):
        song_id += random.choice(pool)
    
    song_id = int(song_id)
    
    tmp = set(range(song_id-100, song_id)) | set(range(song_id, song_id+100)) #song_id 기준 앞뒤 총 200개 id 생성
        
    return list(tmp-current)
    
def make_chart_id(g_num,ci):
    URL = 'https://www.melon.com/genre/song_list.htm?gnrCode=GN0{}'
    current_URL = URL.format(g_num) #장르번호, 장르번호, 페이지 시작인덱스
    #res_html = requests.get(current_URL, headers = headers).text 
    
    driver = webdriver.Chrome("C:\chromedriver\chromedriver")
    driver.get(current_URL)
    
    tmp = set()
    
  
    i = 0
    
    while i < ci:
        page = random.randint(0, 200)
        script = 'pageObj.sendPage(%s)' % str(page*50)
        driver.execute_script(script)
        sleep(5)
        
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        for tag in soup.select("#songList a[href*=goSongDetail]"):
                js = tag['href']
                tag = js.index("'")
                js = js[tag+1:-3]
                tmp.add(int(js))
    
        i += 1
        
    
    return list(tmp-current)

"""                
    for page in range(ci):
        script = 'pageObj.sendPage(%s)' % str(1 + page*50)
        driver.execute_script(script)
        sleep(5)
        
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        for tag in soup.select("#songList a[href*=goSongDetail]"):
                js = tag['href']
                tag = js.index("'")
                js = js[tag+1:-3]
    
                tmp.add(int(js))
    
    return list(tmp-current)
"""
   
def crawling(s_id):
    
    #크롤링 막힘 방지, 페이지->F12->console->navigator.userAgent->출력값 User-Agent
    
    URL = 'http://www.melon.com/song/detail.htm?songId=' + str(s_id)
    res_html = requests.get(URL, headers = headers).text 
    
    soup = BeautifulSoup(res_html, 'html.parser')
    
    # 가사    
    lyrics = soup.find(id='d_video_summary') 
    if lyrics == None:
        print("{} 가사 없음" .format(s_id))
        return
    else:
        lyrics = str(lyrics)
        lyrics = lyrics.replace('<div class="lyric" id="d_video_summary">', '').\
            replace('<!-- height:auto; 로 변경시, 확장됨 -->', '').\
            replace('<br/>', '\n').replace('</div>', '').strip()
        dic['song_id'].append(s_id)
        dic['lyrics'].append(lyrics)
        
        
        #print(lyrics)
        #print()
    
    # 제목
    title = soup.find(attrs = {"class": "song_name"}).text.replace('곡명','')
    title = re.sub('^\s*|\s+$','', title)
    dic['title'].append(title)
    
    artist = soup.find(attrs={"class": "artist_name"}).text
    album = soup.select('#downloadfrm > div > div > div.entry > div.meta > dl > dd')[0].text
    release = soup.select('#downloadfrm > div > div > div.entry > div.meta > dl > dd')[1].text
    
    genre = soup.select('#downloadfrm > div > div > div.entry > div.meta > dl > dd')[2].text
    genre = genre.replace(';','')
    
    #like = soup.select('#downloadfrm > div > div > div.entry > div.button d_song_like')[0].text
    #like = soup.find(attrs={"class": "button d_song_like"})
    #print(like)
    
    dic['artist'].append(artist)
    dic['album'].append(album)
    dic['release'].append(release)
    dic['genre'].append(genre)
    
    #print("가수: {}" .format(artist))
    #print("앨범: {}" .format(album))
    #print("발매: {}" .format(release))
    #print("장르: {}" .format(genre))

    
    
if __name__ == '__main__':
    
    headers = {
        'Referer': 'https://www.melon.com/index.htm',
        'User-Agent' : ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36")
        } 
    #make_id()
    
    df = pd.read_csv('C:\\Users\\thekoo\\Desktop\\songs_blues.csv', encoding='utf-8-sig')
    #pd.set_option('display.max_columns', 10) 

    current = set(df['song_id'].values.tolist())
    
    dic = df.to_dict('list') 
    
    #crawling(33239419)
    
    
    new = make_chart_id(800,4)
    
    print(len(new))
    
    for index, n in enumerate(new):
        rand_value = random.randint(2, 7)
        sleep(rand_value) #크롤링 막힘 방지
        crawling(n)  
        print(index)
    
    
    """
    for i in range(1):
        new = make_random_id()
        for n in new:
            rand_value = random.randint(2, 7)
            sleep(rand_value) #크롤링 막힘 방지
            crawling(n)  
    """
    
    new_df = pd.DataFrame(dic)
    #print(new_df)
    new_df.to_csv('C:\\Users\\thekoo\\Desktop\\songs_blues.csv', index = False, encoding='utf-8-sig')
    
