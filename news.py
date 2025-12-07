import requests

params ={'serviceKey':'9k9a3/dWfMNnVqG9mRPMQQ28gKPieL/zP8QrxRrOr6gP71ukyqvL7voKvS6fYOooEJiA1/UjQ/SS0sg49nZEUA==',
             'resultType':'json',
             'likeItmsNm':'아모레퍼시픽'
             }

list = [{'basDt': '20251204', 'srtnCd': '002790', 'isinCd': 'KR7002790004', 'itmsNm': '아모레퍼시픽홀딩스', 'mrktCtg': 'KOSPI', 'clpr': '28000', 'vs': '-600', 'fltRt': '-2.1', 'mkp': '28500', 'hipr': '28800', 'lopr': '27750', 'trqu': '114487', 'trPrc': '3217674550', 'lstgStCnt': '79458180', 'mrktTotAmt': '2224829040000'}
,{'basDt': '20251204', 'srtnCd': '002795', 'isinCd': 'KR7002791002', 'itmsNm': '아모레퍼시픽홀딩스우', 'mrktCtg': 'KOSPI', 'clpr': '12380', 'vs': '-110', 'fltRt': '-.88', 'mkp': '12500', 'hipr': '12500', 'lopr': '12320', 'trqu': '5386', 'trPrc': '66787650', 'lstgStCnt': '6443770', 'mrktTotAmt': '79773872600'}
,{'basDt': '20251204', 'srtnCd': '00279K', 'isinCd': 'KR700279K010', 'itmsNm': '아모레퍼시픽홀딩스3우C', 'mrktCtg': 'KOSPI', 'clpr': '22050', 'vs': '-200', 'fltRt': '-.9', 'mkp': '22100', 'hipr': '22250', 'lopr': '21950', 'trqu': '2611', 'trPrc': '57750150', 'lstgStCnt': '7092200', 'mrktTotAmt': '156383010000'}
,{'basDt': '20251204', 'srtnCd': '090430', 'isinCd': 'KR7090430000', 'itmsNm': '아모레퍼시픽', 'mrktCtg': 'KOSPI', 'clpr': '124000', 'vs': '-1200', 'fltRt': '-.96', 'mkp': '125200', 'hipr': '125500', 'lopr': '123400', 'trqu': '153735', 'trPrc': '19049824050', 'lstgStCnt': '58492759', 'mrktTotAmt': '7253102116000'}
,{'basDt': '20251204', 'srtnCd': '090435', 'isinCd': 'KR7090431008', 'itmsNm': '아모레퍼시픽우', 'mrktCtg': 'KOSPI', 'clpr': '46100', 'vs': '-1300', 'fltRt': '-2.74', 'mkp': '47700', 'hipr': '47700', 'lopr': '46000', 'trqu': '14359', 'trPrc': '666614900', 'lstgStCnt': '10557830', 'mrktTotAmt': '486715963000'}
,{'basDt': '20251203', 'srtnCd': '002790', 'isinCd': 'KR7002790004', 'itmsNm': '아모레퍼시픽홀딩스', 'mrktCtg': 'KOSPI', 'clpr': '28600', 'vs': '500', 'fltRt': '1.78', 'mkp': '28200', 'hipr': '28750', 'lopr': '28000', 'trqu': '129640', 'trPrc': '3690713025', 'lstgStCnt': '79458180', 'mrktTotAmt': '2272503948000'}
,{'basDt': '20251203', 'srtnCd': '002795', 'isinCd': 'KR7002791002', 'itmsNm': '아모레퍼시픽홀딩스우', 'mrktCtg': 'KOSPI', 'clpr': '12490', 'vs': '50', 'fltRt': '.4', 'mkp': '12440', 'hipr': '12540', 'lopr': '12310', 'trqu': '8562', 'trPrc': '106652910', 'lstgStCnt': '6443770', 'mrktTotAmt': '80482687300'}
,{'basDt': '20251203', 'srtnCd': '00279K', 'isinCd': 'KR700279K010', 'itmsNm': '아모레퍼시픽홀딩스3우C', 'mrktCtg': 'KOSPI', 'clpr': '22250', 'vs': '250', 'fltRt': '1.14', 'mkp': '22050', 'hipr': '22300', 'lopr': '21950', 'trqu': '2677', 'trPrc': '59198450', 'lstgStCnt': '7092200', 'mrktTotAmt': '157801450000'}
,{'basDt': '20251203', 'srtnCd': '090430', 'isinCd': 'KR7090430000', 'itmsNm': '아모레퍼시픽', 'mrktCtg': 'KOSPI', 'clpr': '125200', 'vs': '400', 'fltRt': '.32', 'mkp': '124900', 'hipr': '125700', 'lopr': '124200', 'trqu': '92430', 'trPrc': '11573301800', 'lstgStCnt': '58492759', 'mrktTotAmt': '7323293426800'}
,{'basDt': '20251203', 'srtnCd': '090435', 'isinCd': 'KR7090431008', 'itmsNm': '아모레퍼시픽우', 'mrktCtg': 'KOSPI', 'clpr': '47400', 'vs': '-350', 'fltRt': '-.73', 'mkp': '47750', 'hipr': '48250', 'lopr': '47100', 'trqu': '11904', 'trPrc': '565086425', 'lstgStCnt': '10557830', 'mrktTotAmt': '500441142000'}
]

def apiget(params):
    url = 'https://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo'
    result = []

    # headers = {'Content-Type': 'charset=utf-8'}
    # response = requests.get(url,params=params, headers=headers)
    #
    # json =  response.json()
    # var = json['response']['body']['items']['item']
    var = list

    for i in range(len(var)):
        keys_to_remove = ['srtnCd', 'isinCd', 'trPrc', 'lstgStCnt', 'mrktTotAmt']
        new_dict = {k: v for k, v in var[i].items() if k not in keys_to_remove}
        result.append(new_dict)
    print(result)

apiget(params)