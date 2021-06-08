import json
import requests
from dingtalkchatbot.chatbot import DingtalkChatbot


def send_message(msg, cp_resp=1):
    webhook = "https://oapi.dingtalk.com/robot/send?access_token=653984671613796137a18ac7a8d65e5df8b461088e26d2ec75f77cf63a020aec"
    #构建请求头部
    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
            }
    if cp_resp == 1:
        #构建请求数据
        tex = msg
        message ={
            "msgtype": "text",
            "text": {"content": tex},
            "at": {"isAtAll": False}
                }
        #对请求的数据进行json封装
        message_json = json.dumps(message)
        #发送请求
        info = requests.post(url=webhook,data=message_json,headers=header)
        if info.status_code == 200 or info.json()['errcode'] == 'ok':
            return
        else:
            print('钉钉消息发送失败')
            return
    else:
        #构建请求数据
        tex = msg
        message ={
            "msgtype": "text",
            "text": {"content": tex},
            "at": {"isAtAll": False}
                }
        #对请求的数据进行json封装
        message_json = json.dumps(message)
        #发送请求
        info = requests.post(url=webhook,data=message_json,headers=header)
        if info.status_code == 200 or info.json()['errcode'] == 'ok':
            return
        else:
            print('钉钉消息发送失败')
            return
