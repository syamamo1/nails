from message_handler import MessageHandler

from flask import Flask, request, redirect

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
            return MessageHandler().record_order(body)
        # If incorrect order was recorded
        if body.upper() == 'NO':
            None
        
        # Initial order 
        else:
            return MessageHandler().initial_order_handler(body)
    else:
        None



if __name__ == '__main__':
    app.run(debug=True) 

