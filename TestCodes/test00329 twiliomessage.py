
# coding = utf-8
from twilio.rest import Client
import time

# Your Account SID from twilio.com/console
account_sid = "AC412d0f21432ea42fe2f9068b7a26fd35"
# Your Auth Token from twilio.com/console
auth_token  = "7c996ef074f8ddbdf5fe200333a41c9c"

client = Client(account_sid, auth_token)

for each in range(1,2):
    message = client.messages.create(body="买入 600487" + str(each), from_='+16606754209', to='+8617312656875') 
    time.sleep(1)
    print(message.sid)