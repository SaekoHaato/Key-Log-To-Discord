from discord import Webhook,SyncWebhook
import requests

def send_to_discord(type,info):
    try:
        if type == 1:
            payload = {'content':info[2]}
            header = {'authorization':info[0]}
            r = requests.post(info[1],json=payload,headers=header)
        else:
            webhook = SyncWebhook.from_url(info[1])
            webhook.send(info[2], username= info[0])
    except Exception as e:
        print(e)