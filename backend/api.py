import poe
import toml
import os
import sys
import logging
from flask import Flask, request
from flask_sock import Sock
from poe import Client

poe.headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 "
                  "Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "Sec-Ch-Ua": "\"Chromium\";v=\"112\", \"Google Chrome\";v=\"112\", \"Not:A-Brand\";v=\"99\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Upgrade-Insecure-Requests": "1"
}

# poe.logger.setLevel(logging.INFO)

file_path = os.path.abspath(sys.argv[0])
file_dir = os.path.dirname(file_path)
config_path = os.path.join(file_dir, "..", "config.toml")
config = toml.load(config_path)
proxy = config["proxy"]
timeout = config["api-timeout"] or config["timeout"] or 7


def get_client(token) -> Client:
    print("Connecting to poe...")
    client_poe = poe.Client(token, proxy=None if proxy == "" else proxy)
    return client_poe


app = Flask(__name__)
sock = Sock(app)
sock.init_app(app)
client_dict = {}


def _add_token(token):
    if token not in client_dict.keys():
        try:
            c = get_client(token)
            client_dict[token] = c
            return "ok"
        except Exception as exception:
            print("Failed to connect to poe due to " + str(exception))
            return "failed: " + str(exception)
    else:
        return "exist"

@app.route('/add_token', methods=['GET', 'POST'])
def add_token():
    token = request.form['token']
    return _add_token(token)


@app.route('/ask', methods=['GET', 'POST'])
def ask():
    token = request.form['token']
    bot = request.form['bot']
    content = request.form['content']
    _add_token(token)
    client = client_dict[token]
    try:
        for chunk in client.send_message(bot, content, with_chat_break=True, timeout=timeout):
            pass
        return chunk["text"].strip()
    except Exception as e:
        del client_dict[token]
        client.disconnect_ws()
        errmsg = f"An exception of type {type(e).__name__} occurred. Arguments: {e.args}"
        print(errmsg)
        return errmsg


@sock.route('/stream')
def stream(ws):
    token = ws.receive()
    bot = ws.receive()
    content = ws.receive()
    _add_token(token)
    client = client_dict[token]
    try:
        for chunk in client.send_message(bot, content, with_chat_break=True, timeout=timeout):
            ws.send(chunk["text_new"])
    except Exception as e:
        del client_dict[token]
        client.disconnect_ws()
        errmsg = f"An exception of type {type(e).__name__} occurred. Arguments: {e.args}"
        print(errmsg)
        ws.send(errmsg)
    ws.close()



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=config.get('gateway-port', 5100))
