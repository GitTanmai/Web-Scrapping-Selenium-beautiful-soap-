import requests
import pandas as pd
import json
import os
from datetime import datetime
#driver = webdriver.Chrome(executable_path=r'C:\\driver\\chromedriver.exe')
URL = 'https://locations.mshanken.io/restaurants.json?latitude=0&longitude=0&radius=999999&search=country%3A%22United%20States%22%20AND%20state%3A%22AZ%22&sort=current_award%20desc%2C%20restaurant_name%20asc&page=2'
dr=requests.get(URL)
data= json.loads(dr.text)

def data_file_create():
#        final_data = {}
#        data_store = {}
	data_ls = []
	try:
		for i,k in enumerate(data['results']):
		#print('sadadadadad      ',k['name'])
	
			data_ls.append({'Outlet Name': k['name'], 'Outlet Address': k['address1'],
                                	'Outlet City': k['city']['short_name'],
                                	'Outlet State': k['state']['short_name'], 'Outlet Zip Code': k['zipcode'],
                                	'place': 'Florida'})
		df_obj = pd.DataFrame(
            	columns=['Outlet Name', 'Outlet Address', 'Outlet City', 'Outlet State', 'Outlet Zip Code'])
		output = df_obj.append(data_ls, ignore_index=True)   
	except:
		print('Error while scraping data')
	return output
o=data_file_create()
print(o)
o.to_excel(
            os.path.join( 'Wine_Spectator_' + 'Florida' + '_' + str(datetime.date(datetime.now()))[-5:] + '.xlsx'),
            index=False)	
