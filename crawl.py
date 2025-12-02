from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

result =[]

RANKING_URLS = {
    0: "https://www.oliveyoung.co.kr/store/main/getBestList.do?t_page=%ED%99%88&t_click=GNB&t_gnb_type=%EB%9E%AD%ED%82%B9&t_swiping_type=N",
    1: "https://www.qoo10.jp/gmkt.inc/Bestsellers/?g=2", #큐텐 뷰티
    2: "https://www.coupang.com/np/categories/176522?traceId=miithkrj", #쿠팡 화장품 랭킹순
    3: "https://www.amazon.com/s?i=specialty-aps&bbn=16225010011&rh=n%3A%252116225010011%2Cn%3A3777891&language=ko&ref=nav_em__nav_desktop_sa_intl_personal_care_0_2_17_7", #아마존 퍼스널 케어
}
PLATFORM_NAMES = {
    0: "올리브영",
    1: "큐텐",
    2: "쿠팡",
    3: "아마존"
}
def crawl_qoo10(): #큐텐
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('lang=ko_KR') # 사용언어 한국어

        driver = webdriver.Chrome(options=options)
        driver.get(RANKING_URLS[1])
        driver.implicitly_wait(5) #페이지 로딩 대기

        find = driver.find_elements(By.CSS_SELECTOR,".col4 li:nth-child(-n+10) .item") #nth-child(-n+20) 앞에서 20번째 자식까지만 포함
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

# def crawl_oliveyoung(): #올리브영
#     try:
#         options = webdriver.ChromeOptions()
#         options.add_argument('lang=ko_KR') # 사용언어 한국어

#         driver = webdriver.Chrome(options=options)
#         driver.get(RANKING_URLS[1])
#         driver.implicitly_wait(5) #페이지 로딩 대기

#     finally:
#         driver.close()

# def crawl_coupang(): #쿠팡
#     try:
#         options = webdriver.ChromeOptions()
#         options.add_argument('lang=ko_KR') # 사용언어 한국어

#         driver = webdriver.Chrome(options=options)
#         driver.get(RANKING_URLS[1])
#         driver.implicitly_wait(5) #페이지 로딩 대기

#     finally:
#         driver.close()

# def crawl_amazon(): #아마존
#     try:
#         options = webdriver.ChromeOptions()
#         options.add_argument('lang=ko_KR') # 사용언어 한국어

#         driver = webdriver.Chrome(options=options)
#         driver.get(RANKING_URLS[1])
#         driver.implicitly_wait(5) #페이지 로딩 대기

#     finally:
#         driver.close()

def crawl_oliveyoung():

    items = []
    site_name = PLATFORM_NAMES[0]
    # 현재는 “1위부터 10위까지 반복한다” 구조를 보여주기 위한 더미 루프
    for rank in range(1, 11):
        name = f"[더미] {site_name}"
        img_src = f"https://example.com/{site_name}_img_{rank}.jpg"
        url = f"https://example.com/{site_name}_product_{rank}"
        brand = f"{site_name}브랜드{rank}"
        price = f"{rank * 1000}"

        items.append([ img_src, url,name, brand, price])

    return items 


def crawl_coupang():
    """쿠팡 랭킹 1~10위 크롤링 구조."""
    site_name = PLATFORM_NAMES[2]
    items = []
    for rank in range(1, 11):
        name = f"[더미] {site_name} 상품 {rank}위"
        img_src = f"https://example.com/{site_name}_img_{rank}.jpg"
        url = f"https://example.com/{site_name}_product_{rank}"
        brand = f"{site_name}브랜드{rank}"
        price = f"{rank * 1000}원"

        items.append([ img_src, url, name,brand, price])

    return items


def crawl_amazon():
    """아마존 랭킹 1~10위 크롤링 구조."""
    items = []
    site_name = PLATFORM_NAMES[3]
    for rank in range(1, 11):
        name = f"[더미] {site_name} 상품 {rank}위"
        img_src = f"https://example.com/{site_name}_img_{rank}.jpg"
        url = f"https://example.com/{site_name}_product_{rank}"
        brand = f"{site_name}브랜드{rank}"
        price = f"{rank * 1000}원"

        items.append([ img_src, url,name, brand, price])

    return items

crawl_qoo10()