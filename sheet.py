import gspread
from gspread_formatting import *
from gspread_formatting.batch_update_requests import format_cell_range
import numpy as np
from oauth2client.service_account import ServiceAccountCredentials


class Sheet():

    def __init__(self, client_names):
        # Target
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        # Credentials
        creds = ServiceAccountCredentials.from_json_keyfile_name('nails_json_key.json', scope)
        # Client for API
        client = gspread.authorize(creds)

        # Open 'Order Sheet' Google Sheet
        self.sheet = client.open('Order Sheet')
        # NEEDS TO BE UPDATED AS SOME POINT
        self.client_names = client_names

        # self.update_client_sheet('Sheet-1', pd.DataFrame({'Item Number':['01','001','101'], 'Quantity':[9997,9998,9999]}))


    # Updates appointed client's sheet
    # Order in format: df('Item Number': [n1,n2,n3], 'Quantity':[q1, q2, q3])
    def update_client_sheet(self, client, order):
        worksheet_instance = self.sheet.worksheet(client)

        current_data = self.get_current_data(worksheet_instance)
        order_data = self.get_order_data(order)
        updated_data = current_data + order_data

        # Sheets Column Headers
        locations = ['H','K','N','Q','T','W','Z','AC','AF','AI','AL']
        ind = 0
        fmt = CellFormat(backgroundColor=Color((1,1,1)))
        for col in updated_data:
            lst_col = self.lots_list(col)
            # Sheet Indices (1 Index, row 4 to row 103)
            location = locations[ind]+'4:'+locations[ind]+'103'
            # Update location with new column
            worksheet_instance.update(location, lst_col)
            format_cell_range(worksheet_instance, location, fmt)

            ind += 1


    # 1 Index, Return numpy array of orders/0s
    def get_current_data(self, worksheet_instance):
        current_data = np.zeros((11, 100))
        column = 1
        ind = 0
        for cell in worksheet_instance.row_values(3):
            if cell == 'Numbers':
                # Column + 1 bc get Quantity 
                current_data[ind] += np.array(worksheet_instance.col_values(column+1)[3:103]).astype(int)
                ind += 1
            column += 1

        return current_data


    def get_order_data(self, order):
        order_data = np.zeros((11, 100))
        item_ind = 0
        for item in order['Item Number']:
            if len(item) == 2:
                item_num = int(item)
                order_data[0, item_num] += order['Quantity'][item_ind]
            else:
                item_col = int(item[0]) + 1
                item_num = int(item)
                order_data[item_col, item_num%100] += order['Quantity'][item_ind]
            item_ind += 1

        return order_data    
        
    # Formatting for gspread update method
    def lots_list(self, col):
        list_list = []
        for i in range(100):
            list_list.append([col[i]])

        return list_list



if __name__ == '__main__':
    S = Sheet()