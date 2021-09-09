import os
import re
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import numpy as np
import pandas as pd

import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Run main app...
@app.route('/sms', methods=['GET', 'POST'])
def main():
    number = request.form['From']
    body = request.form['Body']
    quoc_number = '+8083899459'
    sean_number = '+18085515481'
    # resp = MessagingResponse()
    # resp.message(str(number))
    # return str
    # 3 types of texts
    if number == sean_number or number == quoc_number:
        # If correct order was recorded
        if body.upper() == 'YES':
            return record_order(body)
        # If incorrect order was recorded
        if body.upper() == 'NO':
            None
        
        # Initial order 
        else:
            return initial_order_handler(body)
    else:
        None


# Send order and sms reply
def record_order(body):
    send_order(body)
    resp = sms_confirmation(body)
    return resp


# Send order to google sheets 
def send_order(body):
    df_order = df_maker(body)

    # -----------------for Google Sheets-------------------
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('nails_json_key.json', scope)
    client = gspread.authorize(creds)
    # ----------------------------------------------------------


def df_maker(body):
    quantities = []
    items = []
    for order in body.split('/n'):
        quantity, item = quantity_item_parser(order)
        quantities.append(quantity)
        items.append(item)

    return pd.DataFrame(quantities, items)


def sms_confirmation(body):
    resp = MessagingResponse()
    customer, detailed_body = detailer(body)
    response = '// \n\nOrder confirmed! \n' + detailed_body
    resp.message(response)
    return str(resp)



# Create response text to confirm order
def initial_order_handler(body):
    resp = MessagingResponse()
    try:
        customer, detailed_body = detailer(body)
        if customer == 'Not Found':
            response = 'Customer %s not found'%detailed_body
        else:
            response = '// \n\nYour order for %s: \n'%customer + detailed_body
            response = response + '\nIs this order correct? Reply "YES" or "NO"' 
    except: 
        response = 'Incorrect Format. Revise SMS Message!'
    resp.message(response)
    return str(resp)


def detailer(body):
    nice_list = ''
    body_split = body.split('\n')
    customer = body_split[0].upper()

    # Check customer is valid
    if customer in ['A','B','C']:
        # NEED TO check if item is valid (take from sheet?)
        for order in body_split[1:]:
            quantity, item = quantity_item_parser(order)
            nice_list = nice_list + quantity + ' --> ' + 'Item #' + item + '\n'

        return customer, nice_list
    else:
        return 'Not Found', customer

# Just quantity;:/-item\n pattern 
def quantity_item_parser(order):
    order_split = re.split('\W+', order)
    
    quantity = order_split[0]
    item = order_split[1]
    return quantity, item




if __name__ == '__main__':
    app.run(debug=True) 

