import requests
import pandas as pd
from datetime import datetime
from collections import defaultdict
from copy import deepcopy
import pymysql

sql =pymysql.connect(
    host='localhost',
    user='root',
    password='ehgus2003',
    db='tulipmetric',
    charset='utf8')

path = sql.cursor()

market = ['음식료·담배','섬유·의류','기타제조','종이·목재','화학','제약','비금속',
          '금속','기계·장비','전기·전자','의료·정밀기기','운송장비·부품','유통',
          '전기·가스','건설','운송·창고','통신','증권','보험','일반서비스','부동산',
          'IT 서비스','오락·문화']

params ={'serviceKey':'9k9a3/dWfMNnVqG9mRPMQQ28gKPieL/zP8QrxRrOr6gP71ukyqvL7voKvS6fYOooEJiA1/UjQ/SS0sg49nZEUA==',
            'numOfRows' : 958,
            'resultType':'json',
            'basDt'     :'20251229',
            'mrktCls'   :'KOSPI'

             }

def fill_missing_markets(market_list, resp_list, name_key="C1_NM"):
    """
    - market_list 순서대로 resp_list를 맞춰 정렬
    - 누락된 업종은 '가까운 이웃(앞 우선, 없으면 뒤)' dict를 복사해서
      name_key(C1_NM)만 누락 업종명으로 바꿔 채움
    """
    # 응답을 C1_NM 기준으로 빠르게 찾기 위한 맵 (중복이면 첫 번째만 사용)
    by_name = {}
    for item in resp_list:
        nm = item.get(name_key)
        if nm is not None and nm not in by_name:
            by_name[nm] = item

    result = []
    missing = []

    # 뒤에서 가져와야 할 때를 대비해: market_list에서 "다음으로 존재하는 항목" 미리 찾기 함수
    def next_existing_template(start_idx):
        for j in range(start_idx + 1, len(market_list)):
            nm2 = market_list[j]
            if nm2 in by_name:
                return by_name[nm2]
        return None

    for i, nm in enumerate(market_list):
        if nm in by_name:
            result.append(deepcopy(by_name[nm]))
            continue

        # 누락: 이웃 템플릿 선택 (앞 우선, 없으면 뒤)
        missing.append(nm)

        template = None
        if result:  # 앞(바로 이전에 채워진 것)
            template = result[-1]
        else:       # 앞이 없으면 뒤(다음으로 존재하는 것)
            template = next_existing_template(i)

        if template is None:
            # 응답이 완전히 비어있거나, 템플릿을 찾을 수 없는 극단 케이스 대비
            new_item = {name_key: nm}
        else:
            new_item = deepcopy(template)
            new_item[name_key] = nm

        result.append(new_item)

    print("누락 업종:", missing)

    return result



def api_total_market_cap(url):
    headers = {'Content-Type': 'charset=utf-8'}
    response = requests.get(url, params=params, headers=headers)
    list3 =[]
    json = response.json()
    for i in range(len(json)):
        new_dict = {k: v for k, v in json[i].items() if k not in 'ITM_NM'}
        new_dict['total_market_cap'] = new_dict.pop('DT')
        new_dict['total_market_cap'] = int(float(new_dict['total_market_cap']))
        list3.append(new_dict)

    filled = fill_missing_markets(market, list3)

    return filled

def api_market_per(url):
    headers = {'Content-Type': 'charset=utf-8'}
    response = requests.get(url, params=params, headers=headers)
    list4 =[]
    json = response.json()
    for i in range(len(json)):
        keys_to_remove = ["C2_NM","ITM_NM"]
        new_dict = {k: v for k, v in json[i].items() if k not in keys_to_remove}
        new_dict['market_per'] = new_dict.pop('DT')
        new_dict['market_per'] = int(float(new_dict['market_per']))
        if new_dict['C1_NM']=='제조':
            new_dict['C1_NM'] = '기타제조'
        list4.append(new_dict)
    filled = fill_missing_markets(market, list4)
    return filled

def api_stock_count(url):
    headers = {'Content-Type': 'charset=utf-8'}
    response = requests.get(url, params=params, headers=headers)
    list2 =[]
    json = response.json()
    for i in range(len(json)):
        keys_to_remove = ["C2_NM","ITM_NM"]
        new_dict = {k: v for k, v in json[i].items() if k not in keys_to_remove}
        new_dict['stock_count'] = new_dict.pop('DT')
        new_dict['stock_count'] = int(float(new_dict['stock_count']))
        list2.append(new_dict)
    filled = fill_missing_markets(market, list2)
    return filled

def apiget(url,param,params):
    var =[]
    headers = {'Content-Type': 'charset=utf-8'}
    if param:
        response = requests.get(url,params=params, headers=headers) #개별 주식 정보
        json = response.json()
        list1 = json['response']['body']['items']['item']

        for i in range(len(list1)):
            keys_to_remove = ['isinCd', 'trPrc', 'lstgStCnt' ,'hipr' ,'lopr','mkp','mrktCtg','basDt']
            new_dict = {k: v for k, v in list1[i].items() if k not in keys_to_remove}

            # fltRt 보정: -.63 -> -0.63, .63 -> 0.63, +.63 -> +0.63
            flt = new_dict.get('fltRt')
            if flt is not None:
                s = str(flt).strip()
                if s.startswith('-.'):
                    s = '-0' + s[1:]  # '-.63' -> '-0.63'
                elif s.startswith('+.'):
                    s = '+0' + s[1:]  # '+.63' -> '+0.63'
                elif s.startswith('.'):
                    s = '0' + s  # '.63'  -> '0.63'
                new_dict['fltRt'] = s
            new_dict.update({'market':''})
            var.append(new_dict)

        #  업로드된 엑셀 파일 경로
        xlsx_path = "./주식별 업종 분류.xlsx"

        # 엑셀 로드 (종목코드는 문자열로)
        df = pd.read_excel(xlsx_path, dtype={"종목코드": str})

        # 종목코드 -> 업종명 매핑 딕셔너리 생성
        code_to_sector = df.set_index("종목코드")["업종명"].to_dict()

        # var market 빈값 채우기
        not_found = 0
        not_found_codes = []  # (원하면 어떤 코드가 못찾혔는지도 확인 가능)

        new_var = []
        for it in var:
            # market이 이미 있으면 그대로 유지
            if it.get("market"):
                new_var.append(it)
                continue

            code = str(it.get("srtnCd", "")).zfill(6)
            sector = code_to_sector.get(code, "")

            if sector:  # sector != ""
                it["market"] = sector
                new_var.append(it)
            else:
                # sector == "" 인 경우: 해당 dict는 var에서 제거(= new_var에 안 넣음)
                not_found += 1
                not_found_codes.append(code)

        var = new_var

        print("못찾은 종목코드:", not_found_codes)
        print(f"업종명을 못 찾아서 market이 빈 항목 개수: {not_found}")
        return var
    else:
        response = requests.get(url,headers=headers)
        list2 = response.json()
        temp =[]

        for i in range(len(list2)):
            keys_to_remove = ["ITM_NM"]
            new_dict = {k: v for k, v in list2[i].items() if k not in keys_to_remove}
            new_dict['DT'] = int(float(new_dict['DT']))
            if new_dict['C1_NM'] == '제조':
                new_dict['C1_NM'] = '기타제조'
            temp.append(new_dict)

        var = build_sector_dt_map_old_to_new(temp, months=12)
        return var


def _prev_months_old_to_new(latest_yyyymm: str, n: int) -> list[str]:
    """latest_yyyymm(YYYYMM) 기준 최근 n개월을 과거→최신 순으로 반환"""
    base = datetime.strptime(latest_yyyymm, "%Y%m")
    tmp = []
    y, m = base.year, base.month

    # 최신부터 n개월을 만들고
    for i in range(n):
        mm = m - i
        yy = y
        while mm <= 0:
            yy -= 1
            mm += 12
        tmp.append(f"{yy:04d}{mm:02d}")  # 최신 -> 과거

    # 과거 -> 최신으로 뒤집기
    return list(reversed(tmp))

def build_sector_dt_map_old_to_new(list2: list[dict], months: int = 12) -> dict[str, list[int | None]]:
    """
    list2 원소 예:
      {"DT":"15253.53", "PRD_DE":"202411", "C1_NM":"제약", ...}

    반환:
      {"제약":[...12개...], ...}  # 과거 -> 최신 순
    """
    sector_month_to_dt = defaultdict(dict)
    sector_latest_month = {}

    for row in list2:
        sector = row.get("C1_NM")
        month = row.get("PRD_DE")
        dt_str = row.get("DT")

        if not sector or not month:
            continue

        try:
            dt_val = int(dt_str)
        except (TypeError, ValueError):
            dt_val = None

        sector_month_to_dt[sector][month] = dt_val

        if sector not in sector_latest_month or month > sector_latest_month[sector]:
            sector_latest_month[sector] = month

    result = {}
    for sector, month_to_dt in sector_month_to_dt.items():
        latest = sector_latest_month[sector]
        months_list = _prev_months_old_to_new(latest, months)  # 과거 -> 최신
        result[sector] = [month_to_dt.get(m, None) for m in months_list]

    return result
def list_to_map_unique(lst, key_field="C1_NM"):
    """중복이 없다는 전제: [{C1_NM:..., ...}] -> {C1_NM: dict}"""
    return {d[key_field]: d for d in lst}

def merge_market_responses(chart_dict, caps_list, per_list, count_list, market_order=None):
    caps_by  = list_to_map_unique(caps_list,  "C1_NM")
    per_by   = list_to_map_unique(per_list,   "C1_NM")
    count_by = list_to_map_unique(count_list, "C1_NM")

    names = set(chart_dict) | set(caps_by) | set(per_by) | set(count_by)

    # 정렬: market_order가 있으면 그 순서 우선, 나머지는 뒤에 추가
    if market_order:
        ordered = [n for n in market_order if n in names]
        ordered += [n for n in names if n not in set(market_order)]  # 예: '제조' 같은 것
    else:
        ordered = list(names)

    merged = []
    for name in ordered:
        merged.append({
            "market_name": name,
            "total_market_cap": caps_by.get(name, {}).get("total_market_cap"),
            "market_per":       per_by.get(name, {}).get("market_per"),
            "stock_count":      count_by.get(name, {}).get("stock_count"),
            "chart":            deepcopy(chart_dict.get(name))
        })

    return merged


# #개별 주식 정보 기조
index = apiget('https://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo',True,params)
#
#산업군 정보 기조
chart_dict = apiget('https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=ZmVmMjhjMjMwYTBlZjcxODdlMWE4NGM0YjA5NjgxMWU=&itmId=13103130657T1+&objL1=13102130657A.01+13102130657A.02+13102130657A.03+13102130657A.04+13102130657A.05+13102130657A.06+13102130657A.07+13102130657A.08+13102130657A.09+13102130657A.10+13102130657A.11+13102130657A.12+13102130657A.13+13102130657A.14+13102130657A.15+13102130657A.16+13102130657A.17+13102130657A.20+13102130657A.21+13102130657A.22+13102130657A.23+13102130657A.24+13102130657A.25+&objL2=&objL3=&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=M&newEstPrdCnt=12&outputFields=NM+ITM_NM+PRD_DE+&orgId=343&tblId=DT_343_2010_S0190',False,params)

# 산업군별 시가총액 기조
total_market_cap =api_total_market_cap('https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=ZmVmMjhjMjMwYTBlZjcxODdlMWE4NGM0YjA5NjgxMWU=&itmId=13103792812T1+&objL1=13102792812A.03+13102792812A.04+13102792812A.05+13102792812A.06+13102792812A.07+13102792812A.08+13102792812A.09+13102792812A.10+13102792812A.11+13102792812A.12+13102792812A.13+13102792812A.14+13102792812A.15+13102792812A.16+13102792812A.17+13102792812A.18+13102792812A.19+13102792812A.2003+13102792812A.2004+13102792812A.21+13102792812A.22+13102792812A.23+13102792812A.24+&objL2=&objL3=&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=M&newEstPrdCnt=1&outputFields=NM+ITM_NM+&orgId=343&tblId=DT_343_2010_S0026')

# 산업군별 per 기조
market_per = api_market_per('https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=ZmVmMjhjMjMwYTBlZjcxODdlMWE4NGM0YjA5NjgxMWU=&itmId=13103792793T1+&objL1=13102792793A.19+13102792793A.01+13102792793A.02+13102792793A.03+13102792793A.04+13102792793A.05+13102792793A.06+13102792793A.07+13102792793A.08+13102792793A.09+13102792793A.10+13102792793A.11+13102792793A.12+13102792793A.13+13102792793A.14+13102792793A.15+13102792793A.16+13102792793A.1703+13102792793A.1704+13102792793A.18+13102792793A.20+13102792793A.21+13102792793A.22+&objL2=13102792793B.02+&objL3=&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=M&newEstPrdCnt=1&outputFields=NM+ITM_NM+&orgId=343&tblId=DT_343_2010_S0052')

# 산업군 별 상장종목수 기조
stock_count = api_stock_count('https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=ZmVmMjhjMjMwYTBlZjcxODdlMWE4NGM0YjA5NjgxMWU=&itmId=13103792790T1+&objL1=13102792790A.04+13102792790A.05+13102792790A.06+13102792790A.07+13102792790A.08+13102792790A.09+13102792790A.10+13102792790A.11+13102792790A.12+13102792790A.13+13102792790A.14+13102792790A.15+13102792790A.16+13102792790A.17+13102792790A.18+13102792790A.21+13102792790A.19+13102792790A.2003+13102792790A.2004+13102792790A.22+13102792790A.23+13102792790A.24+13102792790A.25+&objL2=13102792790B.02+&objL3=&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=M&newEstPrdCnt=1&outputFields=NM+ITM_NM+&orgId=343&tblId=DT_343_2010_S0016')



print(index)
print(chart_dict)
print(total_market_cap)
print(market_per)
print(stock_count)


# 개별 주식
for i in index:
    data_tuple = (
        i['itmsNm'],
        i['clpr'],
        i['vs'],
        i['fltRt'],
        i['trqu'],
        i['mrktTotAmt'],
        i['market'],
    )

    sql_query = "insert into company values (null, %s, %s, %s, %s, %s, %s, %s)"
    path.execute(sql_query, data_tuple)
    sql.commit()

#산업군
merged = merge_market_responses(chart_dict, total_market_cap, market_per, stock_count, market_order=market)

print(merged)

for i in merged:
    chart_data_str = ",".join(map(str, i['chart']))
    data_tuple = (
        i['market_name'],
        i['total_market_cap'],
        i['market_per'],
        i['stock_count'],
        chart_data_str
    )

    sql_query = "insert into market values (null, %s, %s, %s, %s, %s)"
    path.execute(sql_query, data_tuple)
    sql.commit()


