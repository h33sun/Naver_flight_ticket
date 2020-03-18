import requests
from crawl import *

naver_flight = naver_flight_ticket(month = 5)
df,summary = naver_flight.get_flight_info()
airline, price, date, link = summary.airline[0], summary.price[0], summary.date[0], summary.links[0]

# Api 및 Token 정보
API_HOST = 'https://notify-api.line.me'
headers = {'Authorization': 'Bearer ECbsnz0szY9xYFMJRRETp5z1ACpgo2ZN9XdN2KeqtTx'}
data = {}


 
# get & post 호출 정의
def req(path, query, method, data={}):
    url = API_HOST + path
 
    print('HTTP Method: %s' % method)
    print('Request URL: %s' % url)
    print('Headers: %s' % headers)
    print('QueryString: %s' % query)
 
    if method == 'GET':
        return requests.get(url, headers=headers)
    else:
        return requests.post(url, headers=headers, data=data)
 
# 메신저로 보낼 메세지 내용
message = '\n'*2 +  '링크: ' + link + '\n'*2+'항공사: '+ airline + '\n' +'가격: '+ '₩'+ price + '\n'+'날짜: ' + date
# imageThumbnail= screenshot_crop.png
# imageFullsize= screenshot_crop.png
 
# parameter 값 및 호출 실행
# params = {"message": message, "imageThumbnail" :imageThumbnail, "imageFullsize" : imageFullsize}
params = {"message": message}
resp = req('/api/notify', '', 'POST', params)
 
# Response
print("response status:\n%d" % resp.status_code)
print("response headers:\n%s" % resp.headers)
print("response body:\n%s" % resp.text)
