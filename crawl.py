from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

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

def crawl_oliveyoung():
    site_name = PLATFORM_NAMES[0]

    items = []

    # 현재는 “1위부터 10위까지 반복한다” 구조를 보여주기 위한 더미 루프
    for rank in range(1, 11):
        name = f"[더미] {site_name} 상품 {rank}위"
        img_src = "https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/400/10/0000/0023/A00000023633808ko.jpg?l=ko"
        url = "https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000236338&dispCatNo=90000010009&trackingCd=Best_Sellingbest&t_page=%EB%9E%AD%ED%82%B9&t_click=%ED%8C%90%EB%A7%A4%EB%9E%AD%ED%82%B9_%EC%A0%84%EC%B2%B4_%EC%83%81%ED%92%88%EC%83%81%EC%84%B8&t_number=1"
        brand = f"{site_name}브랜드{rank}"
        price = f"{rank * 1000}원"

        items.append([img_src, url, name, brand, price])

    return items

def crawl_coupang():
    site_name = PLATFORM_NAMES[2]

    items = []
    for rank in range(1, 11):
        name = f"[더미] {site_name} 상품 {rank}위"
        img_src = "https://image.oliveyoung.co.kr/cfimages/cf-goods/uploads/images/thumbnails/400/10/0000/0023/A00000023633808ko.jpg?l=ko"
        url = "https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=A000000236338&dispCatNo=90000010009&trackingCd=Best_Sellingbest&t_page=%EB%9E%AD%ED%82%B9&t_click=%ED%8C%90%EB%A7%A4%EB%9E%AD%ED%82%B9_%EC%A0%84%EC%B2%B4_%EC%83%81%ED%92%88%EC%83%81%EC%84%B8&t_number=1"
        brand = f"{site_name}브랜드{rank}"
        price = f"{rank * 1000}원"

        items.append([ img_src, url, name,brand, price])

    return items




def crawl_qoo10(): #큐텐
    result =[]
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

    return result #최종적으로 crawl_in_thread 에서 result[idx] = data 로 저장됨

def crawl_amazon(): #아마존
    result = []
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
