import os
import sys
from datetime import datetime
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import pymysql

# MySQL 연결
sql =pymysql.connect(
    host='localhost',
    user='user',
    password='(ehgus2003)',
    db='website',
    charset='utf8')

path = sql.cursor()

#DB rankingitem 테이블의 요소 순서는 platform , img , url , name , brand , price
def DBinsert(result):
    for platform in range(4):
        for index in range(len(result[platform])):
            # path.execute(f'insert into rankingitem values(null,{platform},{result[platform][index][0]},{result[platform][index][1]},{result[platform][index][2]},{result[platform][index][3]},{result[platform][index][4]});')
            print(f"insert into rankingitem values(null,{platform},{result[platform][index][0]},{result[platform][index][1]},{result[platform][index][2]},{result[platform][index][3]},{result[platform][index][4]});")

#DB 예외 처리 코드
def safe_DBinsert_with_ui(result):

    try:
        DBinsert(result)
    except pymysql.err.IntegrityError as e:
        messagebox.showerror(
            "DB 오류",
            f"무결성 제약조건 위반(중복키, UNIQUE 제약조건 등)으로 저장에 실패했습니다.\n\n{e}"
        )
        return False

    except pymysql.err.OperationalError as e:
        messagebox.showerror(
            "DB 오류",
            f"DB 연결/접속 관련 오류가 발생했습니다.\n"
            f"DB 서버, 계정, 권한, 네트워크 등을 확인하세요.\n\n{e}"
        )
        return False

    except pymysql.MySQLError as e:
        messagebox.showerror(
            "DB 오류",
            f"MySQL 관련 알 수 없는 오류가 발생했습니다.\n\n{e}"
        )
        return False

    except Exception as e:
        messagebox.showerror(
            "DB 오류",
            f"예상하지 못한 오류가 발생했습니다.\n\n{e}"
        )
        return False

    else:
        return True
    
def on_save_db_click():
    # 현재 result 내용을 DB에 저장
    safe_DBinsert_with_ui(result)
    
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#  전역 데이터 (최종 딕셔너리 result 구조)
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# 0: 올리브영, 1: 큐텐, 2: 쿠팡, 3: 아마존
result = {
    0: [],  # 각 원소: [상품명, 이미지 src, 상품 URL, 브랜드, 가격]
    1: [],
    2: [],
    3: []
}

PLATFORM_NAMES = {
    0: "올리브영",
    1: "큐텐",
    2: "쿠팡",
    3: "아마존"
}

RANKING_URLS = {
    0: "https://www.oliveyoung.co.kr/store/main/getBestList.do?t_page=%ED%99%88&t_click=GNB&t_gnb_type=%EB%9E%AD%ED%82%B9&t_swiping_type=N",
    1: "https://www.qoo10.jp/gmkt.inc/Bestsellers/",
    2: "https://www.coupang.com/np/categories/176522?traceId=miithkrj", #쿠팡 화장품 랭킹순
    3: "https://www.amazon.com/s?i=specialty-aps&bbn=16225010011&rh=n%3A%252116225010011%2Cn%3A3777891&language=ko&ref=nav_em__nav_desktop_sa_intl_personal_care_0_2_17_7", #아마존 퍼스널 케어
}

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#  크롤링 DTO 변환 함수 (예비)
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def crawl_site_generic(site_name: str):
    items = []

    for rank in range(1, 11):
        img_src = f"https://example.com/{site_name}_img_{rank}.jpg"
        url = f"https://example.com/{site_name}_product_{rank}"
        name = f"[더미] {site_name} 상품 {rank}위"
        brand = f"{site_name}브랜드{rank}"
        price = f"{rank * 1000}원"

        items.append([ img_src, url, name,brand, price])

    return items



# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#  사이트별 래퍼 크롤러
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def crawl_oliveyoung():
    """올리브영 랭킹 1~10위 크롤링 구조."""
    site_name = PLATFORM_NAMES[0]
    ranking_url = RANKING_URLS[0]
    """
    하나의 사이트(플랫폼)에 대해 랭킹 1~10위까지 크롤링하는 구조만 구현한 함수.

    실제 구현 시:
        1. ranking_url 로 접속
        2. HTML 파싱 (requests + BeautifulSoup 또는 Selenium 등)
        3. 1등부터 10등까지 반복하면서
           [상품명, 이미지 src, 상품 URL, 브랜드, 가격] 추출

    현재 코드는 구조를 보여주기 위해 더미 데이터를 만들어서 반환한다.
    """

    items = []

    # 현재는 “1위부터 10위까지 반복한다” 구조를 보여주기 위한 더미 루프
    for rank in range(1, 11):
        name = f"[더미] {site_name}"
        img_src = f"https://example.com/{site_name}_img_{rank}.jpg"
        url = f"https://example.com/{site_name}_product_{rank}"
        brand = f"{site_name}브랜드{rank}"
        price = f"{rank * 1000}"

        items.append([ img_src, url,name, brand, price])

    return items #최종적으로 crawl_in_thread 에서 result[idx] = data 로 저장됨


def crawl_qoo10():
    """큐텐 랭킹 1~10위 크롤링 구조."""
    site_name = PLATFORM_NAMES[1]
    ranking_url = RANKING_URLS[1]

    items = []
    for rank in range(1, 11):
        name = f"[더미] {site_name} 상품 {rank}위"
        img_src = f"https://example.com/{site_name}_img_{rank}.jpg"
        url = f"https://example.com/{site_name}_product_{rank}"
        brand = f"{site_name}브랜드{rank}"
        price = f"{rank * 1000}원"

        items.append([ img_src, url, name,brand, price])

    return items


def crawl_coupang():
    """쿠팡 랭킹 1~10위 크롤링 구조."""
    site_name = PLATFORM_NAMES[2]
    ranking_url = RANKING_URLS[2]

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
    site_name = PLATFORM_NAMES[3]
    ranking_url = RANKING_URLS[3]

    items = []
    for rank in range(1, 11):
        name = f"[더미] {site_name} 상품 {rank}위"
        img_src = f"https://example.com/{site_name}_img_{rank}.jpg"
        url = f"https://example.com/{site_name}_product_{rank}"
        brand = f"{site_name}브랜드{rank}"
        price = f"{rank * 1000}원"

        items.append([ img_src, url,name, brand, price])

    return items


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#  결과 txt 파일 저장 함수
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def save_result_to_file():
    """
    현재 result 딕셔너리 내용을 txt 파일로 저장.
    - 파일 위치:
        - py로 실행: 현재 .py 파일이 있는 디렉터리의 result 폴더
        - exe로 실행: exe 파일이 있는 디렉터리의 result 폴더
    - 파일명: YYYYMMDD_HHMMSS_크롤링_정상완료.txt
    """
    # 실행 방식에 따라 base path 결정
    # path = os.path.dirname(__file__)  # py로 실행할때만 가능 exe에선 경로 오류남
    if getattr(sys, 'frozen', False):
        # exe로 실행한 경우, exe를 보관한 디렉토리의 full path를 취득
        path = os.path.dirname(os.path.abspath(sys.executable))
    else:
        # python py로 실행한 경우, py를 보관한 디렉토리의 full path를 취득
        path = os.path.dirname(os.path.abspath(__file__))

    result_dir = os.path.join(path, "result")

    # result 폴더 없으면 생성
    os.makedirs(result_dir, exist_ok=True)

    # 현재 시각 포맷팅
    now = datetime.now()
    timestamp_str = now.strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp_str}_크롤링_정상완료.txt"
    file_path = os.path.join(result_dir, filename)

    # 파일 내용 구성
    lines = []
    lines.append(f"크롤링 완료 시각: {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
    lines.append("=" * 50 + "\n\n")

    for key in range(4):
        platform_name = PLATFORM_NAMES.get(key, f"플랫폼{key}")
        items = result.get(key, [])

        lines.append(f"[{platform_name}]\n")

        if not items:
            lines.append("  - 크롤링된 상품이 없습니다.\n\n")
            continue

        for idx, item in enumerate(items, start=1):
            try:
                name, img_src, url, brand, price = item
            except ValueError:
                lines.append(f"  {idx}위: 데이터 형식 오류 (list 길이 5 아님)\n\n")
                continue

            lines.append(f"  {idx}위\n")
            lines.append(f"    상품명 : {name}\n")
            lines.append(f"    브랜드 : {brand}\n")
            lines.append(f"    가격   : {price}\n")
            lines.append(f"    이미지 : {img_src}\n")
            lines.append(f"    URL    : {url}\n\n")

        lines.append("\n")

    # 파일로 저장
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    return file_path


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#  GUI 크롤링 완료시 text 박스에 결과 표현 함수
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def display_top_items():
    """result에서 각 플랫폼별 크롤링된 모든 상품을 GUI 텍스트 영역에 출력."""
    text_output.delete("1.0", tk.END)

    for key in range(4):
        items = result.get(key, [])
        platform_name = PLATFORM_NAMES[key]

        if not items:
            text_output.insert(tk.END, f"[{platform_name}] 크롤링된 데이터가 없습니다.\n\n")
            continue

        # 플랫폼 제목
        text_output.insert(tk.END, f"[{platform_name} 랭킹]\n")

        for rank, item in enumerate(items, start=1):
            try:
                name, img_src, url, brand, price = item
            except ValueError:
                text_output.insert(
                    tk.END,
                    f"  {rank}위: 데이터 형식 오류 (list 길이 5인지 확인 필요)\n\n"
                )
                continue

            text_output.insert(tk.END, f"  {rank}위\n")
            text_output.insert(tk.END, f"    상품명 : {name}\n")
            text_output.insert(tk.END, f"    브랜드 : {brand}\n")
            text_output.insert(tk.END, f"    가격   : {price}\n")
            text_output.insert(tk.END, f"    이미지 : {img_src}\n")
            text_output.insert(tk.END, f"    URL    : {url}\n\n")

        text_output.insert(tk.END, "\n")

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#  크롤링 버튼 클릭시 실행 되는 메인 함수
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def run_crawling():
    """
    버튼 클릭 시 호출:
    - 각 사이트 크롤링 함수를 서로 다른 쓰레드에서 실행 (총 4개)
    - 크롤링 끝나면 GUI 업데이트 및 파일 저장 , DB입력
    """
    status_var.set("크롤링 중...")
    btn_start.config(state="disabled")
    root.update_idletasks()

    def worker():
        threads = []
        errors = []

        def crawl_in_thread(idx, func):
            try:
                data = func()
                result[idx] = data
            except Exception as e:
                errors.append((idx, e))

        # (플랫폼 번호, 크롤러 함수) 매핑
        funcs = [
            (0, crawl_oliveyoung),
            (1, crawl_qoo10),
            (2, crawl_coupang),
            (3, crawl_amazon),
        ]

        # 4개의 쓰레드 생성 및 시작
        for idx, func in funcs:
            t = threading.Thread(target=crawl_in_thread, args=(idx, func), daemon=True)
            t.start()
            threads.append(t)

        # 모든 크롤링 쓰레드 완료 대기
        for t in threads:
            t.join()

        # 여기서부터는 GUI를 만지는 부분이므로 main thread에서 실행하도록 after 사용
        def on_done():
            btn_start.config(state="normal")

            if errors:
                # 어떤 플랫폼에서 에러 났는지 이름으로 표시
                names = ", ".join(PLATFORM_NAMES[idx] for idx, _ in errors)
                status_var.set("에러 발생")
                messagebox.showerror(
                    "에러",
                    f"다음 플랫폼 크롤링 중 오류가 발생했습니다.\n\n{names}\n\n"
                    f"첫 번째 에러: {errors[0][1]}"
                )
            else:
                # 결과 화면 출력 + 파일 저장 + DB 저장 버튼 활성화
                display_top_items()
                file_path = save_result_to_file()
                status_var.set("크롤링 완료")
                messagebox.showinfo("완료",f"크롤링이 정상적으로 완료되었습니다.\n\n결과 파일:\n{file_path}")

                if not btn_save_db.winfo_ismapped():
                    btn_save_db.pack(side=tk.LEFT, padx=10) #크롤링 성공 시점에 버튼 보여줌
                

        root.after(0, on_done) #첫번재 인자 만큼의 ms 시간 후에 두번재 인자 함수 실행

    # worker 자체를 또 하나의 쓰레드에서 실행해서 GUI가 안 멈추게 함
    threading.Thread(target=worker, daemon=True).start()


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#  GUI 구성 (tkinter)
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

root = tk.Tk()
root.title("화장품 랭킹 크롤러 (올리브영 / 큐텐 / 쿠팡 / 아마존)")

# 상단 프레임: 버튼 + 상태 표시
top_frame = ttk.Frame(root, padding=10)
top_frame.pack(side=tk.TOP, fill=tk.X)

btn_start = ttk.Button(top_frame, text="크롤링 시작", command=run_crawling)
btn_start.pack(side=tk.LEFT)
btn_save_db = ttk.Button(top_frame, text="현재 결과 DB 저장", command=on_save_db_click)

status_var = tk.StringVar(value="대기 중")
status_label = ttk.Label(top_frame, textvariable=status_var)
status_label.pack(side=tk.LEFT, padx=10)

# 중앙: 결과 텍스트
text_frame = ttk.Frame(root, padding=10)
text_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

text_output = tk.Text(text_frame, height=20, wrap="word")
text_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(text_frame, command=text_output.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_output.config(yscrollcommand=scrollbar.set)

# 시작
if __name__ == "__main__":
    root.mainloop()