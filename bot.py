import requests
import yaml
import os
import flask
import logging
import keywords
if os.path.exists("./config.yml"):
    configText = open("./config.yml", 'r', encoding='utf-8')
    config = yaml.safe_load(configText)
else:
    raise Exception("Config not found")
app = flask.Flask(__name__)
log = logging.getLogger("werkzeug")
log.disabled = True
def send_private_msg(id, message):
    requests.get("http://127.0.0.1:%d/send_private_msg?user_id=%d&message=%s" % (config["bot"]["http"]["port"], id, message))
def send_group_msg(group, message):
    requests.get("http://127.0.0.1:%d/send_group_msg?group_id=%d&message=%s" % (config["bot"]["http"]["port"], group, message))
@app.route("/", methods=["POST","GET"])
def get_data():
    if flask.request.get_json().get("post_type") == "message":
        if flask.request.get_json().get("message_type") == "private":
            user = flask.request.get_json().get("user_id")
            splitWord = flask.request.get_json().get("message").split(" ")
            for admin in config["admin"]:
                if user == admin:
                    flag = True
                else:
                    flag = False
            if splitWord[0] == "添加关键词":
                if flag == False:
                    send_private_msg(user, "只有管理员才能添加关键词喵")
                else:
                    if len(splitWord) != 3:
                        send_private_msg(user, "喂, 两个参数, 栓Q (")
                    else:
                        send_private_msg(user, "收到了喵")
                        keywords.addKeyWord(splitWord[1], splitWord[2])
            elif splitWord[0] == "删除关键词":
                if flag == False:
                    send_private_msg(user, "只有管理员才能删除关键词 (恼")
                else:
                    if len(splitWord) != 2:
                        send_private_msg(user, "一个参数, 栓Q")
                    else:
                        send_private_msg(user, "收到啦")
                        keywords.delKeyWord(splitWord[1])
            elif splitWord[0] == "更新关键词":
                if flag == False:
                    send_private_msg(user, "只有管理员才能更新关键词喵")
                else:
                    if len(splitWord) != 3:
                        send_private_msg(user, "喂, 两个参数, 栓Q (不屑")
                    else:
                        send_private_msg(user, "收到了 (欣慰")
                        keywords.updateKeyWord(splitWord[1],splitWord[2])
            elif splitWord[0] == "查看关键词":
                if flag == False:
                    send_private_msg(user, "叫管理稍微滥权一下, 就看得到关键词啦")
                else:
                    send_private_msg(user, keywords.seeData())
            else:
                matching = keywords.matchingKeyWord()
                for word in matching:
                    if word[0] in flask.request.get_json().get("message"):
                        send_private_msg(user, word[1])
        if flask.request.get_json().get("message_type") == "group":
            group = flask.request.get_json().get("group_id")
            matching = keywords.matchingKeyWord()
            for word in matching:
                if word[0] in flask.request.get_json().get("message"):
                    send_group_msg(group, word[1])
    return "OK"
if __name__ =="__main__":
    app.run(port=config["bot"]["post"]["port"],debug=False)