import os
import sys
import json
import time
import requests
import websocket
from keep_alive import keep_alive

status = "dnd"  # online/dnd/idle

custom_status = "𝘩𝘦𝘢𝘳𝘵 𝘴𝘰 𝘤𝘰𝘭𝘥."
#𝘩𝘦𝘢𝘳𝘵 𝘴𝘰 𝘤𝘰𝘭𝘥.
#𝘤𝘢𝘳𝘱𝘦 𝘥𝘪𝘦𝘮.
usertoken = os.getenv("TOKEN")
if not usertoken:
    print("[ERROR] Please add a token inside Secrets.")
    sys.exit()

headers = {"Authorization": usertoken, "Content-Type": "application/json"}

validate = requests.get("https://canary.discordapp.com/api/v9/users/@me", headers=headers)
if validate.status_code != 200:
    print("[ERROR] Your token might be invalid. Please check it again.")
    sys.exit()

userinfo = requests.get("https://canary.discordapp.com/api/v9/users/@me", headers=headers).json()
username = userinfo["username"]
discriminator = userinfo["discriminator"]
userid = userinfo["id"]
b = """`🔒` `root@ubuntu:~/DredDine#    ` `- ❐ ⤬`
˗
> `📂`〢<id:home>
> ╰─➤https://ln.ki/s/DD
˗
> *"electric dreams"*
˗
> `🟣🐍Py` `🟡<JS>` `✢`
˗
> `📌` <t:1604227492:R>
> updated <t:{}:R>
˗""".format(
    int(time.time())
)
requests.patch("https://discord.com/api/v9/users/@me", headers=headers, json={"bio": b})


def onliner(token, status):
    ws = websocket.WebSocket()
    ws.connect("wss://gateway.discord.gg/?v=9&encoding=json")
    start = json.loads(ws.recv())
    heartbeat = start["d"]["heartbeat_interval"]
    auth = {
        "op": 2,
        "d": {
            "token": token,
            "properties": {
                "$os": "Windows 10",
                "$browser": "Google Chrome",
                "$device": "Windows",
            },
            "presence": {"status": status, "afk": False},
        },
        "s": None,
        "t": None,
    }
    ws.send(json.dumps(auth))
    cstatus = {
        "op": 3,
        "d": {
            "since": 0,
            "activities": [
                {
                    "type": 4,
                    "state": custom_status,
                    "name": "Custom Status",
                    "id": "custom",
                    # Uncomment the below lines if you want an emoji in the status
                    # "emoji": {
                    # "name": "disappointed",
                    # "id": "emoji id",
                    # "animated": False,
                    # },
                }
            ],
            "status": status,
            "afk": False,
        },
    }
    ws.send(json.dumps(cstatus))
    online = {"op": 1, "d": "None"}
    time.sleep(heartbeat / 1000)
    ws.send(json.dumps(online))


def run_onliner():
    os.system("clear")
    print(f"Logged in as {username}#{discriminator} ({userid}).")
    while True:
        onliner(usertoken, status)
        time.sleep(30)


keep_alive()
run_onliner()
