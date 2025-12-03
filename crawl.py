from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

result =[]

num = 10 # 상품 크롤링 개수

RANKING_URLS = {
    0: "https://www.oliveyoung.co.kr/",
    1: "https://www.qoo10.jp/gmkt.inc/Bestsellers/?g=2", #큐텐 뷰티
    2: "https://www.coupang.com/", #쿠팡 화장품 쿠팡랭킹순 
    3: "https://www.amazon.com/s?i=specialty-aps&bbn=16225010011&rh=n%3A%252116225010011%2Cn%3A3777891&language=ko&ref=nav_em__nav_desktop_sa_intl_personal_care_0_2_17_7", #아마존 퍼스널 케어
}
PLATFORM_NAMES = {
    0: "올리브영",
    1: "큐텐",
    2: "쿠팡",
    3: "아마존"
}
# def crawl_oliveyoung(): #올리브영
#     try:
#         options = webdriver.ChromeOptions()
#         options.add_argument('lang=ko_KR') # 사용언어 한국어

#         driver = webdriver.Chrome(options=options)
#         driver.get(RANKING_URLS[0])
#         driver.implicitly_wait(5) #페이지 로딩 대기

#         # driver.find_element(By.CSS_SELECTOR,"gnb_menu_list li:nth-child(2)>a").click()

#     finally:
#         driver.close()


def crawl_qoo10(): #큐텐
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('lang=ko_KR') # 사용언어 한국어

        driver = webdriver.Chrome(options=options)
        driver.get(RANKING_URLS[1])
        driver.implicitly_wait(5) #페이지 로딩 대기

        find = driver.find_elements(By.CSS_SELECTOR,f".col4 li:nth-child(-n+{num}) .item") #nth-child(-n+20) 앞에서 20번째 자식까지만 포함
        print("큐텐 크롤링 item 개수:", len(find))
        for item in find:
            try:
                brand = item.find_element(By.CSS_SELECTOR,".txt_brand").get_attribute("title")
            except NoSuchElementException:
                # 브랜드도 없는 이상한 블록(광고 등)은 스킵
                brand = "브랜드 표기 없음"

            # 가격 요소가 없는 item은 기본값
            try:
                price_el = item.find_element(By.CSS_SELECTOR, ".dtl .prc strong")
                price = price_el.text.strip()
            except NoSuchElementException:
                price = None
            
            

            el = item.find_element(By.CSS_SELECTOR,".thmb")
            name = el.get_attribute("title")
            href = el.get_attribute("href")

            img = el.find_element(By.TAG_NAME, "img")
            img_src = img.get_attribute("gd_src") or img.get_attribute("src")
            result.append([img_src,href , name ,brand , price])
    finally:
        driver.close()

    return result

def crawl_amazon(): #아마존
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('lang=ko_KR') # 사용언어 한국어

        driver = webdriver.Chrome(options=options)
        driver.get(RANKING_URLS[3])
        driver.implicitly_wait(5) #페이지 로딩 대기

        find = driver.find_elements(By.CSS_SELECTOR,".sg-col-inner div[role='listitem']")

        for item in find:
            href = item.find_element(By.CSS_SELECTOR,".a-link-normal.s-no-outline").get_attribute("href")
            el = item.find_element(By.CSS_SELECTOR,".s-image")
            name = el.get_attribute("alt")
            img_src = el.get_attribute("src")
            
            price = item.find_element(By.CSS_SELECTOR,".a-price-whole").text
            brand = name.split(" ")[0]

            result.append([img_src,href , name ,brand , price])
        
        return result
        

    finally:
        driver.close()


print(crawl_oliveyoung())