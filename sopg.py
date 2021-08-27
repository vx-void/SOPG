import sys
# import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException as e
import csv
from datetime import datetime
from time import sleep


proxyDict = {}

countries = ('us','id','br','de','bd','ru','gb','sg','in','fr','nl','co','tr','ec','ar','za','ir','mx','jp','cn','ua', \
    'do', 'kh', 'pe', 'kz', 'th', 'nz')

headers = ['IP:PORT', 'TYPE', 'ANONYMITY', 'COUNTRY/REGION', 'HOSTNAME', 'DELAY', 'UPTIME', 'CHECK DATE']

class ProxyList(object):

    def __init__(self, counter, driver) -> None:
       
        self.counter = int(counter)
        self.driver = driver
    
    def grabbing(self):
        
        self.address = self.driver.find_element_by_xpath(f'/html/body/table[2]/tbody/tr[3]/td/table/tbody/tr[{self.counter}]/td[1]')
        self.type = self.driver.find_element_by_xpath(f'/html/body/table[2]/tbody/tr[3]/td/table/tbody/tr[{self.counter}]/td[2]')
        self.anon = self.driver.find_element_by_xpath(f'/html/body/table[2]/tbody/tr[3]/td/table/tbody/tr[{self.counter}]/td[3]')
        self.region = self.driver.find_element_by_xpath(f'/html/body/table[2]/tbody/tr[3]/td/table/tbody/tr[{self.counter}]/td[4]')
        self.hostname = self.driver.find_element_by_xpath(f'/html/body/table[2]/tbody/tr[3]/td/table/tbody/tr[{self.counter}]/td[5]')
        self.delay = self.driver.find_element_by_xpath(f'/html/body/table[2]/tbody/tr[3]/td/table/tbody/tr[{self.counter}]/td[6]')
        self.uptime = self.driver.find_element_by_xpath(f'/html/body/table[2]/tbody/tr[3]/td/table/tbody/tr[{self.counter}]/td[8]')
        self.data = self.driver.find_element_by_xpath(f'/html/body/table[2]/tbody/tr[3]/td/table/tbody/tr[{self.counter}]/td[9]')
                                                        
    def toDict(self):
        proxyDict[int(self.counter-4)] = {
                                   'ip': self.address.text, 
                                   'type': self.type.text,
                                   'anon' : self.anon.text,
                                   'region': self.region.text,
                                   'hostname': self.hostname.text,
                                   'delay' : self.delay.text,
                                   'uptime' : self.uptime.text,
                                   'data' : self.data.text
                                   }   

if __name__ == '__main__':
    print('*********************************')
    print('*   SPYS.ONE PROXY GRABBER      *')
    print('*********************************')
    print('\n\n')
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    

    print(f'[{datetime.now()}]: Launching Chromedriver...\n')
    driver = webdriver.Chrome('chromedriver', options=options)
    
    c_version = driver.capabilities['browserVersion']
    cd_version = driver.capabilities['chrome']['chromedriverVersion']

    print(f'[{datetime.now()}]: Chromedriver version: {cd_version}\n')
    print(f'[{datetime.now()}]: Chrome version: {c_version}\n')
    

    try:    
        country = input("[Input]Enter the country to search for: ")
        print(f'[\n{datetime.now()}]: Connecting ...\n')
        if country.lower() == 'all' or country == None or country == '':
            driver.get('https://spys.one/proxies/')
            sleep(4)
        elif country.lower() in countries:
            driver.get(f'https://spys.one/proxies/{country.lower()}')
            sleep(4)
        elif country.lower() not in countries:
            print(f"[{datetime.now()}]:[ERROR]: The country / region was not found or entered incorrectly\n")    
            driver.close()
            sys.exit()
        print(f'[{datetime.now()}]: Extracting...\n')
        for i in range(4, 29):
            proxy_ = ProxyList(counter=i, driver=driver)
            proxy_.grabbing()
            proxy_.toDict()
        output = f'{country}-{datetime.now()}.csv'
        print(f'[{datetime.now()}]: Saving to \'{output}\'\n')
        
        with open (output, 'w') as file:
            f_csv = csv.writer(file)
            f_csv.writerow(headers)
            f_csv.writerow(['---------','---------','---------','---------',\
                '---------','---------','---------','---------'])
            
            for key in proxyDict.keys():
                f_csv.writerow([proxyDict[key]['ip'], proxyDict[key]['type'], proxyDict[key]['anon'],\
                    proxyDict[key]['region'], proxyDict[key]['hostname'],\
                    proxyDict[key]['delay'], proxyDict[key]['uptime'],proxyDict[key]['data']]) 
            print(f'[{datetime.now()}]: The \'{output}\' was written\n')
        print(f'[{datetime.now()}]: Chromedriver closed\n')    
        
        driver.close()
        print('****** Thank you for using SOPG ********\n')
        sys.exit()
    except e:
        print(f'[{datetime.now()}]:[ERROR]: {e}')
        driver.close()
        sys.exit()

                
         



