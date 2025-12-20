import requests

params ={'serviceKey':'9k9a3/dWfMNnVqG9mRPMQQ28gKPieL/zP8QrxRrOr6gP71ukyqvL7voKvS6fYOooEJiA1/UjQ/SS0sg49nZEUA==',
             'resultType':'json',
             'likeItmsNm':'아모레퍼시픽'
             }

def apiget(url,param,params):
    result = []

    headers = {'Content-Type': 'charset=utf-8'}
    if param:
        response = requests.get(url,params=params, headers=headers)
        json = response.json()
        var = json['response']['body']['items']['item']
    else:
        response = requests.get(url,headers=headers)
        var = response.json()



    # var = list
    #
    # for i in range(len(var)):
    #     keys_to_remove = ['srtnCd', 'isinCd', 'trPrc', 'lstgStCnt', 'mrktTotAmt']
    #     new_dict = {k: v for k, v in var[i].items() if k not in keys_to_remove}
    #     result.append(new_dict)
    # print(result)

    return var

print(apiget('https://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo',True,params))
print("\n\n\n\n\n")
print(apiget('https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=ZmVmMjhjMjMwYTBlZjcxODdlMWE4NGM0YjA5NjgxMWU=&itmId=13103130657T1+&objL1=ALL&objL2=&objL3=&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=M&newEstPrdCnt=12&orgId=343&tblId=DT_343_2010_S0190',False,params))
