import json
import os
from datetime import date, datetime
import getpass
import pandas as pd
import requests

class WineSpectator:
    def __init__(self, url, place, file_save_path):
        self.url = url
        self.place = place
        self.file_save_path = file_save_path

    def sample_run(self, page):
        sample_hit = self.url + str(page)

        response_get = requests.get(sample_hit)
        data_fetch = json.loads(response_get.text)

        data_ret = {'data': data_fetch}

        print('Total Pages --', int(data_ret['data']['summary']['total_pages']))
        print('Count --', int(data_ret['data']['summary']['count']))

    @staticmethod
    def default_data_generation(url, page):
        sample_hit = url + str(page)

        response_get = requests.get(sample_hit)

        data_fetch = json.loads(response_get.text)
        return int(data_fetch['summary']['total_pages']), data_fetch

    def data_file_create(self):
        total_pages_for_iter, data_ = self.default_data_generation(self.url, page=1)

        final_data = {}
        data_store = {}

        for page_idx in range(1, total_pages_for_iter + 1):
            _, data_store['page' + str(page_idx)] = self.default_data_generation(self.url, page_idx)

        final_data['data'] = data_store

        data_ls = []

        for idx, val in final_data['data'].items():
            for idx_new in final_data['data'][str(idx)]['results']:
                data_ls.append({'Outlet Name': idx_new['name'], 'Outlet Address': idx_new['address1'],
                                'Outlet City': idx_new['city']['short_name'],
                                'Outlet State': idx_new['state']['short_name'], 'Outlet Zip Code': idx_new['zipcode'],
                                'place': self.place})

        return data_ls

    def excel_data_create(self):
        df_obj = pd.DataFrame(
            columns=['Outlet Name', 'Outlet Address', 'Outlet City', 'Outlet State', 'Outlet Zip Code'])
        output = df_obj.append(self.data_file_create(), ignore_index=True)
        output.to_excel(
            os.path.join(self.file_save_path, 'Wine_Spectator_' + self.place + '_' + str(date.today())[-5:] + '.xlsx'),
            index=False)

        return 'Data For ' + self.place + ' Saved In ' + self.file_save_path.split('\\')[
            len(self.file_save_path.split('\\')) - 2]


def create_directory():
    user = getpass.getuser()
    today = datetime.now()
    directory = today.strftime("%d") + '-' + today.strftime("%B")[:3] + '-' + 'WineSpectator'
    path = r'C:\\Users\\' + user + '\\Desktop\\' + directory
    os.mkdir(path)
    return path


if __name__ == '__main__':
    URL = 'https://locations.mshanken.io/restaurants.json?latitude=0&longitude=0&radius=999999&search=country%3A%22United%20States%22%20AND%20state%3A%22AZ%22&sort=current_award%20desc%2C%20restaurant_name%20asc&page='
    CITY = 'Florida'

    FILE_SAVE_PATH = create_directory()
    obj_cls = WineSpectator(URL, CITY, FILE_SAVE_PATH)
    incoming_data = obj_cls.excel_data_create()