
import warnings
warnings.filterwarnings('ignore')

import requests
import time
import pandas as pd
import re
import calendar
import datetime

from bs4 import BeautifulSoup as bs
from PIL import Image as pil
from selenium import webdriver


class naver_flight_ticket():
    
    next_month = datetime.datetime.now().month+1

    def __init__(self, year = 2020, month = next_month, departure = 'SIN'):
        '''
        year(default = 2020)
        month(default = next_month(if today is 2020.03.04 next_month = 4)), 
        departure (IATA Airport Code with Uppercase, default = 'SIN')
        check your IATA code in https://www.asianacargo.com/contents/listOfAirportCode.do
        '''
        self.year = year
        self.month = month
        self.departure = departure
#         dates = []
        
                
        
        
    def get_flight_urls(self):
        '''
        return urls in https://www.flight.naver.com
        from ICN to Destination in specific month
        
        
        '''
        year = self.year
        month = self.month
        departure = self.departure
        
        result = []
        dates = []
#         print(month)
        last_date = calendar.monthrange(year, month)[1]
        urls = []
        
        for date in range(1,last_date+1):
            if len(str(date))==1:
                date='0'+str(date)
            if len(str(month))==1:
                month = '0'+str(month)
            url = 'https://flight.naver.com/flights/v2/results?trip=OW&scity1=ICN&ecity1={}&adult=1&child=0&infant=0&sdate1=\
2020.{}.{}.&fareType=Y'.format(departure,month,date)
            urls.append(url)
        return urls
    
    
    
    
    
    
    def get_flight_info(self):
        data = []
        links = []
        urls = self.get_flight_urls()
        for url in urls:
            print(url[-22:-12])
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            options.add_argument('window-size=1920x1080')
            driver = webdriver.Chrome(options = options)
            driver.get(url)
            time.sleep(20)

    
            for i in range(5):
                print(i)
                flights = driver.find_elements_by_css_selector('#content > div:nth-child(3) > div.trip_itinerary.ng-scope > div:nth-child(7) > ul > li')
    
                info = flights[i].text.strip().split()
                print(info)

                if len(info) == 17:
                    data.append({
                                'date' : url[-22:-12],
                                'airline' : info[0],
                                'departure': info[2],
                                'departure_time' : info[3],
                                'arrival' : info[5],
                                'arrival_time':info[6],
                                'overall_hour':info[9],
                                'price':info[14].replace('원~','')
                        })
                else:
                    data.append({
                                'date' : url[-22:-12],
                                'airline' : info[0],
                                'departure': info[2],
                                'departure_time' : info[3],
                                'arrival' : info[5],
                                'arrival_time':info[6],
                                'overall_hour':info[10],
                                'price':info[15].replace('원~','')
                        })
                num_terms = driver.find_element_by_css_selector('#content > div:nth-child(3) > div.trip_itinerary.ng-scope > div:nth-child(7) > ul > li:nth-child({}) > div:nth-child(5) > a > strong'.format(i+1)).text
                if num_terms != '1':
                    driver.find_element_by_css_selector('#content > div:nth-child(3) > div.trip_itinerary.ng-scope > div:nth-child(7) > ul > li:nth-child({}) > div:nth-child(5) > a'.format(i+1)).click()
                    driver.find_element_by_css_selector('#content > div:nth-child(3) > div.trip_itinerary.ng-scope > div:nth-child(7) > ul > li:nth-child({}) > div:nth-child(5) > div > a.sp_flight.btn_check'.format(i+1)).click()
                    links.append(driver.current_url)
                    driver.find_element_by_css_selector('#content > div:nth-child(2) > div > div > div.trip_title > span').click()
                else:
                    driver.find_element_by_css_selector('#content > div:nth-child(3) > div.trip_itinerary.ng-scope > div:nth-child(7) > ul > li:nth-child({}) > div:nth-child(5) > a'.format(i+1)).click()
                    links.append(driver.current_url)
                    driver.find_element_by_css_selector('#content > div:nth-child(2) > div > div > div.trip_title > span').click()

            driver.quit()
            df = pd.DataFrame(data)
            df['links'] = links
        summary = df[df.price== min(df.price)].sort_values(['date'],ascending = False).reset_index()
        return df, summary
            