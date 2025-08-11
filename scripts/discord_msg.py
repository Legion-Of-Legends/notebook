import os
import requests

discord_webhook=os.environ.get("discord_webhook")

def send_discord_msg(message: str):
    data={
        "username":"Github Bot",
        "avatar_url":"https://github.githubassets.com/assets/GitHub-Mark-ea2971cee799.png",
        "content":message,
        "allowed_mentions": { "parse": ["everyone"] }
      }
    response=requests.post(discord_webhook, json=data)

