from bs4 import BeautifulSoup
from selenium import webdriver
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import urllib.request  
import asyncio
import requests
import time
from time import sleep
from multiprocessing import Pool, Manager, freeze_support
import json
import os
import sys
sys.path.insert(0, 'F:\cloth_yolo\Clothing-Detection-master')
import new_image_demo as c_yolo
import collections
import pymysql

color_list=[]
url_l=[]
main_url='http://www.ssg.com/search.ssg?target=all&query='
num=0

#key_list=["가디건","니트","베스트","코트","자켓","블라우스","셔츠","티셔츠","원피스","치마","바지","수트","점퍼"] #키워드 이걸로 쓰기
key_list=["티셔츠"]


patterns=["P09", "P01", "P02", "P10","P03","P04","P11"]
textile=["T123", "T113", "T112", "T124","T118","T125"]
necks=["F33", "F32","F38","F37","F31","F36","F42"]
length= ['L152', 'L151', 'L153', 'L154', 'L148', 'L147', 'L149', 'L150']

def get_imgs(i, info_l ,word,pattern,tex,neck,leng):
    """f_url = 'http://www.ssg.com'+url
    req = requests.get(f_url)
    sleep(1)

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    #options.add_argument("disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome('C:/Users/dahee/Downloads/chromedriver_win32/chromedriver.exe',chrome_options=options)  # Optional argument, if not specified will search path.
    driver.get(f_url)
    #time.sleep(10) # Let the user actually see something!
    driver.implicitly_wait(1)

    html = driver.page_source
 
    soup = BeautifulSoup(html,'html.parser')
    img=soup.find("meta",  property="og:image") #이미지 크롤링 코드"""
    img_b=info_l[0][i]
    img_n=info_l[1][i]
    img_p=info_l[2][i]
    img_i=info_l[3][i]
    img_it=info_l[4][i]

    color = ""
    sat = ""
    val = ""
    try:
        color_hsv=c_yolo.cloth_yolo(img_i,word)
    except ValueError:
        pass
    
    if color_hsv:
        color=color_hsv[0]
        sat=color_hsv[1]
        val=color_hsv[2]

    #print(color_hsv)
    #print(img_u)
    #여기다 sql db저장 코드 추가!!
    conn = pymysql.connect(
        host= '211.214.181.77',
        user= 'daye',
        password = '1234',
        db='ClothesInfo',
        charset='utf8'
    )
    
    #컬러 변수 이름: color(색) / sat(채도) / val(명도) --> DB 컬럼 이름 : Color / C_Sat / C_Val 
    cursor = conn.cursor()
    sql = f"insert into tshirt(Id,Brand,Price,Pattern,Material,Neckline,leng,Imgurl,Itemurl, Color, C_Sat, C_Value) values(\"{img_n}\",\"{img_b}\",\"{img_p}\",\"{pattern}\",\"{tex}\",\"{neck}\",\"{leng}\",\"{img_i}\",\"{img_it}\",\"{color}\",\"{sat}\",\"{val}\");"
    cursor.execute(sql)
    conn.commit()
    conn.close()
    
    #다른 것도 크롤링 하기
    
def get_url(i,pat, tex, neck, word,leng, num):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3")
    options.add_argument("--proxy-server=socks5://127.0.0.1:9150")
    driver = webdriver.Chrome("C:/Users/dahee/chromedriver.exe",chrome_options=options)  # Optional argument, if not specified will search path.
    n_url=main_url+word+"&styleFilter="+pat+"^"+tex+"^"+neck+"^"+leng+"&count=100&page="+i
    driver.get(n_url)
    #time.sleep(10) # Let the user actually see something!
    driver.implicitly_wait(1)

    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')

    url_list=[]
    brand_l=[]
    name_l=[]
    price_l=[]
    image_l=[]

    for j in range(0,num+1):
        href= soup.find_all("div", class_="title")[j]
        if(href.find("strong",  class_="brd")is None):
                brand_l.append(" ")
        else:
            b_html=href.find("strong",  class_="brd")
            b_html=b_html.find("em",class_="tx_ko")
            brand_l.append(b_html.text)
        n_html=href.find("a")
        n_html=n_html.find("em",class_="tx_ko")
        name_l.append(n_html.text)
        url_list.append(href.find("a")["href"])
        
        p_html= soup.find_all("div", class_="opt_price")[j]
        p_html=p_html.find("em",class_="ssg_price")
        price_l.append(p_html.text)
        
        i_html= soup.find_all("div", class_="thmb")[j]
        image_l.append(i_html.find("img")["src"])
        
        """t_num=soup.find("div",class_="aside_txt notranslate")
        num=t_num.find("em")
        i_num=num.replace(",","")"""

    brand_l=brand_l[0:100]
    name_l=name_l[0:100]
    price_l=price_l[0:100]
    image_l=image_l[0:100]
    url_list=url_list[0:100]

    info_l=[["."],["."],["."],["."],["."]]
    info_l[0]=brand_l
    info_l[1]=name_l
    info_l[2]=price_l
    info_l[3]=image_l
    info_l[4]=url_list

    print("패턴",pat,"소재",tex,"넥라인",neck,"기장",leng,"\n")
    return info_l

def get_num(pat, tex, neck, word,leng):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--proxy-server=socks5://127.0.0.1:9150")
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome("C:/Users/dahee/chromedriver.exe",chrome_options=options)  # Optional argument, if not specified will search path.
    n_url=main_url+word+"&styleFilter="+pat+"^"+tex+"^"+neck+"^"+leng+"&count=100"
    driver.get(n_url)
    #time.sleep(10) # Let the user actually see something!
    driver.implicitly_wait(1)

    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    i_num=0

    try:
        t_num=soup.find("div",class_="aside_txt notranslate")
        num=t_num.find("em")
        num=num.text
        i_num=num.replace(",","")

    except(IndexError,TypeError,AttributeError):
        pass

    return(int(i_num))

def do_process_with_thread_crawl(i: str, word):
    for pattern in patterns:
        for tex in textile:
            for neck in necks:
                for leng in length:
                    #take_limit(pattern,tex,neck,word,leng)
                    if (pattern=='P09' or pattern=='P01'):
                        pass
                    elif (pattern=='P02'):
                        if (tex=='T123' or tex=='T113' or tex=='T112'):
                            pass
                        elif (tex=='T124'):
                            if (neck=='F33' or neck=='F32'):
                                take_limit(pattern,tex,neck,word,leng)
                            else:
                                pass
                        else:
                            take_limit(pattern,tex,neck,word,leng)
                    else:
                        take_limit(pattern,tex,neck,word,leng)
                    """if (pattern=='P09'):
                        if(tex=='T123'):
                            if(neck=='F33' or neck=='F32'):
                                pass
                    elif (pattern=='P09'):
                        if(tex=='T123'):
                            if(neck=='F38'):
                                if(leng=='L152' or leng=='L151' or leng=='L153' or leng=='L154'):
                                    pass
                    else:
                        take_limit(pattern,tex,neck,word,leng)"""
                    """num=get_num(pattern,tex,neck,word,leng)
                    num=num//100
                    if num>0 and num<10:
                        for j in range(1,num):
                            print(j)
                            do_thread_crawl(get_url(str(j),pattern,tex,neck,word,leng),word,pattern,tex,neck,leng)
                    elif num>0 and num>=10:
                        for j in range(1,10):
                            print(j)
                            do_thread_crawl(get_url(str(j),pattern,tex,neck,word,leng),word,pattern,tex,neck,leng)"""
def take_limit(pattern,tex,neck,word,leng):
    num_i=get_num(pattern,tex,neck,word,leng)
    num=num_i//100
    if num_i>0 and num<4:
        for j in range(1,num+2):
            if j == num+1 and num_i%100 != 0:
                do_thread_crawl(get_url(str(j),pattern,tex,neck,word,leng, num_i%100),word,pattern,tex,neck,leng)
                print(j)
                print(num_i%100)
            else:
                do_thread_crawl(get_url(str(j),pattern,tex,neck,word,leng, 100),word,pattern,tex,neck,leng)
    elif num>0 and num>=3:
        for j in range(1,4):
            print(j)
            do_thread_crawl(get_url(str(j),pattern,tex,neck,word,leng,100),word,pattern,tex,neck,leng)

def do_thread_crawl(info_l: list, word,pattern,tex,neck,leng):
    thread_list = []
    with ThreadPoolExecutor(max_workers=3) as executor:
        if info_l:
            if info_l[3]:
                for i in range(0,len(info_l[3])):
                    thread_list.append(executor.submit(get_imgs, i, info_l, word,pattern,tex,neck,leng))
                for execution in concurrent.futures.as_completed(thread_list):
                    execution.result()

if __name__ == '__main__':
    freeze_support()
    with Pool(processes=3) as pool:  
        #mylist = Manager().list()
        for word in key_list: #검색어 입력
            for i in range(1,2): #크롤링 페이지
                pool.starmap(do_process_with_thread_crawl,[(str(i),word)])
        #pool.map(do_process_with_thread_crawl, mylist,main_url)
        pool.close()
        pool.join()
    #print("실행 시간 : %s초" % (time.time() - start_time))