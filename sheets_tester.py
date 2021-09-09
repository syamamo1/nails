import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials


class Sheet():

    def __init__(self) -> None:
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('nails_json_key.json', scope)
        client = gspread.authorize(creds)

        self.sheet = client.open('Order List')
        # Find by sheet name instad of index?
        self.client_names = {'A':1, 'B':2}


    def update_client_sheet(self, client, order):
        ind = self.client_names[client]
        worksheet_instance = self.sheet.get_worksheet(ind)
        worksheet_prev_records = self.get_all_records(worksheet_instance)

        worksheet_updated_records = worksheet_prev_records.add(order, fill_value = 0)
        # worksheet_instance.



    # def update_master_sheet(self, client, )

    
    def get_all_records(self, sheet_instance):
        all_records = sheet_instance.get_all_records()
        return(pd.DataFrame(all_records))





if __name__ == '__main__':
    S = Sheet()
    print(S.all_records)