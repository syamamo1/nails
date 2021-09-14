from sheet import Sheet

import re
from twilio.twiml.messaging_response import MessagingResponse
import pandas as pd


class MessageHandler():

    def __init__(self):
        self.client_names = ['Sheet-1','Sheet-2','Sheet-3','Sheet-4','Sheet-5']

    # Send order and sms reply
    def record_order(self, body):
        self.send_order(body)
        resp = self.sms_confirmation(body)
        return resp

    # Send order to google sheets 
    def send_order(self, body):
        client, order = self.df_maker(body)

        cur_sheet = Sheet(self.client_names)
        cur_sheet.update_client_sheet(client, order)


    # Int, Int
    def df_maker(self, body):
        quantities = []
        items = []
        client = body.split('\n')[0]
        for order in body.split('\n')[1:]:
            quantity, item = self.quantity_item_parser(order)
            quantities.append(int(quantity))
            items.append(item)

        # String, Int
        dict_order = {'Item Number':items, 'Quantity':quantities}
        return client, pd.DataFrame(dict_order)


    def sms_confirmation(self, body):
        resp = MessagingResponse()
        customer, detailed_body = self.detailer(body)
        response = '// \n\nOrder confirmed! \n' + detailed_body
        resp.message(response)
        return str(resp)


    # Create response text to confirm order
    def initial_order_handler(self, body):
        resp = MessagingResponse()
        try:
            customer, detailed_body = self.detailer(body)
            if customer == 'Not Found':
                response = 'Customer %s not found'%detailed_body
            else:
                response = '// \n\nYour order for %s: \n'%customer + detailed_body
                response = response + '\nIs this order correct? Reply "YES" or "NO"' 
        except: 
            response = 'Incorrect Format. Revise SMS Message!'
        resp.message(response)
        return str(resp)


    def detailer(self, body):
        nice_list = ''
        body_split = body.split('\n')
        customer = body_split[0]

        # Check customer is valid
        if customer in self.client_names:
            # NEED TO check if item is valid (take from sheet?)
            for order in body_split[1:]:
                quantity, item = self.quantity_item_parser(order)
                nice_list = nice_list + quantity + ' --> ' + 'Item #' + item + '\n'

            return customer, nice_list
        else:
            return 'Not Found', customer

    # Input just quantity;:/-item\n pattern 
    def quantity_item_parser(self, order):
        order_split = re.split('\W+', order)
        
        quantity = order_split[0]
        item = order_split[1]
        return quantity, item