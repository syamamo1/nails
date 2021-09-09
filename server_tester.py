import os
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import numpy as np

app = Flask(__name__)

# Run main app...
@app.route('/sms', methods=['GET', 'POST'])
def main():
    number = request.form['From']
    body = request.form['Body']
    quoc_number = 8083899459
    sean_number = 8085515481

    resp = MessagingResponse()
    resp.message("test")
    return str(resp)




if __name__ == '__main__':
    app.run(debug=True) 

