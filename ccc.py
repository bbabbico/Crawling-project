<<<<<<< HEAD
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

result =[]

url = 'https://www.qoo10.jp/gmkt.inc/Bestsellers/?g=2' #큐텐

options = webdriver.ChromeOptions()
options.add_argument('lang=ko_KR') # 사용언어 한국어

driver = webdriver.Chrome(options=options)
driver.get(url)
driver.implicitly_wait(5) #페이지 로딩 대기

find = driver.find_elements(By.CSS_SELECTOR,".col4 li:nth-child(-n+20) .item") #nth-child(-n+20) 앞에서 20번째 자식까지만 포함
print("item 개수:", len(find))
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
    result.append([href ,img_src, name ,brand , price])

print(result)
=======
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

result =[]

def q10():
    url = 'https://www.qoo10.jp/gmkt.inc/Bestsellers/?g=2' #큐텐

    options = webdriver.ChromeOptions()
    options.add_argument('lang=ko_KR') # 사용언어 한국어

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.implicitly_wait(5) #페이지 로딩 대기

    find = driver.find_elements(By.CSS_SELECTOR,".col4 li:nth-child(-n+20) .item") #nth-child(-n+20) 앞에서 20번째 자식까지만 포함
    print("item 개수:", len(find))
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
        result.append([href ,img_src, name ,brand , price])

    return result

def oli():
    url = 'https://www.qoo10.jp/gmkt.inc/Bestsellers/?g=2' #큐텐

    options = webdriver.ChromeOptions()
    options.add_argument('lang=ko_KR') # 사용언어 한국어

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.implicitly_wait(5) #페이지 로딩 대기
>>>>>>> 975b3dc (커밋)
