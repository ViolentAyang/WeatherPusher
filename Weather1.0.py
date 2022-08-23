import requests
import datetime
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import time


def get_alluser():
    user_list = {}
    with open('user.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.rstrip('\n')
            flag = line.find(':')
            length = len(line)
            user_list[line[0:flag]] = line[flag + 1:length]
        return user_list


def get_user(number):
    user_list = {}
    with open('user.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.rstrip('\n')
            flag = line.find(':')
            length = len(line)
            user_list[line[0:flag]] = line[flag + 1:length]
        return user_list[number]


def get_content(data, name):
    weekday = get_week_day(datetime.datetime.now())
    tempMax = data['daily'][0]['tempMax']  # 最高温
    tempMin = data['daily'][0]['tempMin']  # 最低温
    textDay = data['daily'][0]['textDay']  # 天气情况 晴、多云..
    windDirDay = data['daily'][0]['windDirDay']  # 风向
    windScaleDay = data['daily'][0]['windScaleDay']  # 风力
    content = '早上好！' + name + '！\n' + weekday + ' 的天气是 ' + textDay + '\n最高温度为' + tempMax + '° ' + '最低温度为' + tempMin + '° ' + '\n风向为 ' + windDirDay + ' 风力为' + windScaleDay + '级'
    return content


def get_week_day(date):
    week_day_dict = {
        0: '星期一',
        1: '星期二',
        2: '星期三',
        3: '星期四',
        4: '星期五',
        5: '星期六',
        6: '星期天',
    }
    day = date.weekday()
    return week_day_dict[day]


def get_weather(name):
    url = 'https://devapi.qweather.com/v7/weather/3d?location=118.89,31.90&key='
    res = requests.get(url)
    if res.json()['code'] == '200':
        data = res.json()
        return get_content(data, name)  # 返回拼接好的数据
    else:
        return False


def send_qq(number):
    if get_weather(get_user(number)):
        data = get_weather(get_user(number))
        url = 'https://qmsg.zendee.cn/send/?qq=' + number + '&msg=' + data
        res = requests.get(url)
        if not res.json()['success']:
            send_mail(number + '@qq.com', '机器人出现故障，请联系管理员1972076517及时修复', 'Qmsg推送报错')
    else:
        send_mail('1972076517@qq.com', '获取天气数据失败，请联系管理员1972076517及时修复', '天气数据推送报错')


def send_mail(mail, content, title):
    number = '...@qq.com'
    password = ''
    to_addr = mail
    smtp_server = 'smtp.qq.com'
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = Header('暴力扬消息推送')
    msg['To'] = Header(to_addr)
    msg['Subject'] = Header(title)
    server = smtplib.SMTP_SSL(host=smtp_server)
    server.login(number, password)
    server.sendmail(number, to_addr, msg.as_string())


def main():
    dic = get_alluser()
    for i in dic:
       send_mail(i+'@qq.com',get_weather(get_user(i)),'每日天气推送')


if __name__ == '__main__':
    main()
