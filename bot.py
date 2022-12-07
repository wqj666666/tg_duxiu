import telebot
from typing import NoReturn
from time import sleep
from asyncio import sleep
import requests
import re
import pymysql,telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests
#tg机器人id
bot_api = ""
import pymysql  #连接数据库
connect = pymysql.connect(host='',   # 本地数据库
                          user='',
                          password='',
                          db='',
                          charset='utf8') #服务器名,账户,密码，数据库名称
db = connect.cursor()



def start(update: Update, context: CallbackContext):
    update.message.reply_text('请输入：读秀SS号,输入格式为：/ss 14061086')
def ss(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    names = text.split(' ')
    name = names[1]
    content = '^[0-9]{8}$'
    result = re.findall(content, str(name))
    if len(result) != 0:
        sql = "SELECT * FROM FileObject WHERE name LIKE '%" + name + "%';"
        db.execute(sql)
        result = db.fetchall()
        if len(result) !=0:
            fs_id = result[0][1]
            ss = duxiu(fs_id)
            update.message.reply_text(ss)
        else:
            update.message.reply_text("数据库没有该书集")

    else:
        update.message.reply_text("输入的读秀SS格式错误")


    print(name)
    print(ss)

#百度网盘连接生成功能
def duxiu(ss):
    session = requests.session()
    # BDUSS和STOKEN的值从cookies种获取
    session.cookies["BDUSS"] = ''
    session.cookies["STOKEN"] = ''

    headerss = {
                            'Host': 'pan.baidu.com',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
                    }
    response = session.get('https://pan.baidu.com/', headers=headerss)
    if(not False):
        pwd = 1123
    form_data = {
        'schannel': 4,
        'channel_list': '[]',
        'period': 7,
        'pwd': pwd,
        'fid_list': str([int(ss)]),
    }
    print(str([ss]))
    # 补充cookie的值
    headers = {
    "Accept":"*/*" ,
    "Accept-Encoding":"gzip, deflate, br" ,
    "Accept-Language":"zh-CN,zh;q=0.9" ,
    "Cache-Control":"no-cache" ,
    "Connection":"keep-alive" ,
    "Content-Length":"16930" ,
    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8" ,
    "Cookie":"" ,
    "Host":"pan.baidu.com" ,
    "Origin":"https://pan.baidu.com" ,
    "Pragma":"no-cache" ,
    "Referer":"https://pan.baidu.com/disk/home?" ,
    "Sec-Fetch-Dest":"empty" ,
    "Sec-Fetch-Mode":"cors" ,
    "Sec-Fetch-Site":"same-origin" ,
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36" ,
    "X-Requested-With":"XMLHttpRequest"
    }
    responsess = session.post(url, headers=headers, data=form_data)
    print(responsess.headers)
    if(responsess.json()['errno'] == 0):
        print({'errno': 0, 'err_msg': '创建分享链接成功！', 'info': {'link': responsess.json()['link'], 'pwd': pwd}})
        return {'link': responsess.json()['link'], 'pwd': pwd}
    else:
        print( {'errno': 1, 'err_msg': '创建分享链接失败！', 'info': responsess.json()})
        return "创建分享链接失败！"



def main() -> None:
    updater = Updater(bot_api)

    dispatcher = updater.dispatcher

    # 机器人命令
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("ss", ss))
    # 启动机器人，勿删
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
