from selenium import webdriver
import time
import re
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options 
from pandas import DataFrame
import numpy as np
from bs4 import BeautifulSoup


options = Options()
di={}
column_names=['Product_Id','Product_Name','Product url','MRP','Price','Discount','Onshelfavalaiblity','Returnable','Sold_by','Rating','Total Rating count','Delivered_by','Best_Before','Number of images']
df = pd.DataFrame(columns = column_names)
#print('cols',df.columns)

links=['https://www.amazon.in/dp/B00HJ2E3Z0','https://www.amazon.in/dp/B07FLWFLL5','https://www.amazon.in/dp/B07RT6BPNX','https://www.amazon.in/dp/B0744L529L','https://www.amazon.in/dp/B00B0QCNXU',
'https://www.amazon.in/dp/B07NQQPNDG','https://www.amazon.in/dp/B00X9UOCEI','https://www.amazon.in/dp/B006LX9VPU']
#print(links)
def details(links,df):
        try:
                for li in links:
                        print('li',li)
                        #options.add_argument("window-size=1200x600")
                        driver = webdriver.Chrome(executable_path=r'C:\\driver\\chromedriver.exe')              
                        driver.get(li)
                        time.sleep(5)
                        soup = BeautifulSoup(driver.page_source, 'html.parser')
                        di['Product_Id']=re.search(r'\/(?!.*\/).*',li).group(0)[1:]             
                        #Adding product name in dict
                        pro = driver.find_element_by_xpath("//*[@id='productTitle']")
                        di['Product_Name']=pro.text             
                        #add url
                        di['Product url']=li
                        #Adding price to dict           
                                        #Discount in price
                        try:
                                dis=driver.find_element_by_xpath("//*[@id='regularprice_savings']/td[2]")
                                di['Discount']=re.search(r'\((.*?)\)',dis.text).group(1)
                        except:
                                di['Discount']='No Discount'
                        try:
                                if di['Discount']=='No Discount':
                                        o=driver.find_element_by_class_name("a-size-medium a-color-price priceBlockBuyingPriceString")
                                        di['MRP']=o.text[2:]
                                        di['Price']=o.text[2:]
                                else:
                                        orprice=driver.find_element_by_class_name("priceBlockStrikePriceString")
                                        di['MRP']=orprice.text[2:]
                                        price_el=driver.find_element_by_xpath("//*[@id='priceblock_ourprice']")
                                        di['Price']=price_el.text[2:]
                        except:
                                #price_el=driver.find_element_by_xpath("//*[@id='priceblock_ourprice']")
                                di['MRP']='NA'
                                di['Price']='NA'                        
                        #Adding availability in dict
                        stock=driver.find_element_by_xpath("//*[@id='availability']/span")
                        if stock.text=='In stock.':
                        di['Onshelfavalaiblity']=1
                        else:
                        di['Onshelfavalaiblity']=0              
                        #Returnable
                        try:
                                returna=driver.find_element_by_xpath("//*[@id='icon-farm-container']/div/div")
                                di['Returnable']=returna.text
                        except:
                                #quit()
                                #returna=driver.find_element_by_xpath("//*[@id='icon-farm-container']/div/div[2]/span/div[2]/span")
                                di['Returnable']='returna.text' 
                                #//*[@id="icon-farm-container"]/div/div/span/div[2]/span
                        #Sold by 
                        try:
                                sold=driver.find_element_by_xpath("//*[@id='sellerProfileTriggerId']")
                                di['Sold_by']=sold.text
                        except:
                                di['Sold_by']='NA'              
                        #Rating //*[@id="merchant-info"]/text()[2]                              
                        #time.sleep(15)
                        try:
                                rating=driver.find_element_by_xpath("//*[@id='merchant-info']")
                                rat=re.search(r'\((.*?)\)',rating.text).group(1)
                                di['Rating']=float(rat[:3])
                                di['Total Rating count']=re.search(r'\|(\s)(.[\d,]+)',rating.text).group(2).strip()
                        except:
                                rat=None
                                di['Rating']='NA'
                                di['Total Rating count']='NA'
                        #re.search(r'\|(\s)(.*[^\S])',rating.text).group(2).strip()
                        #Delivery by
                        try:
                                deliver=driver.find_element_by_xpath("//*[@id='ddmDeliveryMessage']")
                                di['Delivered_by']=deliver.text
                        except:
                                di['Delivered_by']='NA'
                        #//*[@id="ddmDeliveryMessage"]/b                        
                        #Best before 
                        try:
                                bb=driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[4]/div[5]/div[4]/div[19]/span[2]")
                                bb=bb.text
                        except:
                                bb=None
                        di['Best_Before']=bb
                        # Number of images                              
                        images = soup.find_all("li", class_=re.compile("a-spacing-small item .*"))
                        cc=0
                        for image in images: 
                                cc +=1
                        di['Number of images']=cc
                        print('dict',di)
                        df=df.append(di,ignore_index=True)                              
                        #Closing the listening tool
                        driver.close()
                        driver.quit()
        except:
                print('Error occurred while loading page')
        return df
df=details(links,df)
df.index = np.arange(1, len(df) + 1)
df.to_excel("noutput.xlsx")
print(df)



