# -*- coding: utf-8 -*-
"""VnStock 2.0 - ChatBot.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IsXf6Krrexa1nPUkYVEKbfuX2FA2yBLC
"""

!pip install Flask
!pip install pymessenger
!pip install schedule
#!pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_md-2.0.0/en_core_web_md-2.0.0.tar.gz

#!pip install flask-ngrok flask==0.12.2

!pip install gunicorn

!pip freeze>requirements.txt

#Python libraries that we need to import for our bot
import random
from flask import Flask, request
from pymessenger.bot import Bot
#from flask_ngrok import run_with_ngrok

app = Flask(__name__)
#run_with_ngrok(app)

ACCESS_TOKEN = 'EAAV5cyiWGJ4BAB2CM8rOkIZCpcZAGeteIa7LojlbkNuWBJ70pr0gdsY0xFaQYFafTAL2pmaIt7HsmQLexAZBcoSCx5ZB9gjGpL1MOZC5qPJ7bmdOTnWCmiJOx7pflqqbPRn2QlejgvyTwbGuB3pM6hR3ZBFXYn59jWX8AFR1PnBe7lrGZCw5OE3'
VERIFY_TOKEN = 'LearningEnglish'
bot = Bot(ACCESS_TOKEN)

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        print(token_sent)
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                print(recipient_id)
                if message['message'].get('text'):
                    response_sent_text = get_message()
                    send_message(recipient_id, response_sent_text)
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    response_sent_nontext = get_message()
                    send_message(recipient_id, response_sent_nontext)
    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
      print(token_sent)
      return request.args.get("hub.challenge")
    return 'Invalid verification token'


#chooses a random message to send to the user
def get_message():
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    # return selected item to the user
    return random.choice(sample_responses)

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    try:
      bot.send_text_message(recipient_id, response)
      return "success"
    except:
      return "fail"

if __name__ == "__main__":
    app.run()

# import schedule
# import time

# def job():
#     send_message("2388099994534010","Hello")

# schedule.every(3).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every(5).to(10).minutes.do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
# schedule.every().minute.at(":17").do(job)

# while True:
#     schedule.run_pending()
#     time.sleep(1)

"""TRIỂN KHAI TRÊN HEROKU

1) Có tài khoản
"""