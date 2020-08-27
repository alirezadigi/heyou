# 786
from flask import Flask, request
from requests import post
import config


class TelegramApi():
    def __init__(self, token):
        self.token = token

    def sendmessage(self, chat_id, message):
        token = self.token
        url = "https://api.telegram.org/bot{}/SendMessage?chat_id={}&text={}".format(
            token, chat_id, message)
        return post(url)


bot_agent = TelegramApi(config.bot_token)


app = Flask(__name__)
#app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Welcome To Heyou!</h1>"


@app.route('/api/sendalert', methods=['GET'])
def sendalert():
    if 'receiver' in request.args and 'sender' in request.args and 'message' in request.args:
        sender = request.args['sender']
        message = request.args['message']
        receiver = request.args['receiver']
        alert_text = '{} has a work with you!\nmessage: {}'.format(
            sender, message)
        telegram_response = bot_agent.sendmessage(receiver, alert_text)
        if telegram_response.status_code == 200:
            return '<h1>Message sucsessfully sent!</h1>'
        else:
            return '<h1>Error!</h1><h2>Status Error:' + str(telegram_response.status_code) + '</h2><h3>Error Text:' + str(telegram_response.text) + '</h3>'


app.run()
