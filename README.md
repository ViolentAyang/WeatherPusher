
# ✨项目前言
>**立春后天气忽热忽略冷,当然需要有个每日提醒自己多少度，该穿什么衣服的女朋友啦，那没有怎么办啊？今天我就带大家自己写一个进行每日提醒的机器人😜**

# 🎨所需工具
- ```pycharm ```
- ```python 3.9```
- time
- Qmsg
- smtplib
- email 
# 🌔实现思路
通过和风天气提供的接口，获得今日天气数据，对数据进行拼接修改，然后调用qmsg提供的接口，发送到指定qq号，利用腾讯云函数的cron触发器，设置每日的定时调用，即可实现！

# 🏂准备工作
**安装pycharm**

[https://www.runoob.com/w3cnote/pycharm-windows-install.html](https://www.runoob.com/w3cnote/pycharm-windows-install.html)

**安装python**

[https://www.emojidaquan.com/common-sports-emojis](https://www.emojidaquan.com/common-sports-emojis)

**安装其他所需模块**

[https://docs.python.org/zh-cn/3/installing/index.html](https://docs.python.org/zh-cn/3/installing/index.html)

**注册腾讯云函数**

[https://cloud.tencent.com/register?&s_url=https%3A%2F%2Fconsole.cloud.tencent.com%2Fscf%2Flist%3Frid%3D1%26ns%3Ddefault](https://cloud.tencent.com/register?&s_url=https://console.cloud.tencent.com/scf/list?rid=1&ns=default)

**注册qmsg**

[https://qmsg.zendee.cn/](https://qmsg.zendee.cn/)

**注册和风天气**

[https://id.qweather.com/#/login?redirect=https%3A%2F%2Fconsole.qweather.com%2F%23%2Fconsole](https://id.qweather.com/#/login?redirect=https://console.qweather.com/#/console)

# 🌟项目实现
## 创建应用
在和风天气控制台创建一个新应用，获取你的**个人KEY**
![在这里插入图片描述](https://img-blog.csdnimg.cn/42a677c906c244f189e601190cec2273.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAVmlvbGVudC1BeWFuZw==,size_20,color_FFFFFF,t_70,g_se,x_16)
## 检索全部用户
获取所有使用用户（我的应用不仅是一个人使用，有很多用户，用户账号信息全部存储在user.txt中）

```python
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
```
## 检索指定用户
定义一个查找指定用户账号的函数

```python
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
```
## 获取时间
编写一个获取当前是周几的函数，以便之后我们对数据进行拼接

```python
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
```
## 解析数据
获取和风天气数据，对数据进行分析

```json
{
    "code": "200", 
    "updateTime": "2022-03-08T15:35+08:00", 
    "fxLink": "http://hfx.link/30l1", 
    "daily": [
        {
            "fxDate": "2022-03-08", 
            "sunrise": "06:25", 
            "sunset": "18:07", 
            "moonrise": "09:32", 
            "moonset": "23:36", 
            "moonPhase": "峨眉月", 
            "moonPhaseIcon": "801", 
            "tempMax": "22", 
            "tempMin": "8", 
            "iconDay": "100", 
            "textDay": "晴", 
            "iconNight": "150", 
            "textNight": "晴", 
            "wind360Day": "225", 
            "windDirDay": "西南风", 
            "windScaleDay": "1-2", 
            "windSpeedDay": "3", 
            "wind360Night": "135", 
            "windDirNight": "东南风", 
            "windScaleNight": "3-4", 
            "windSpeedNight": "16", 
            "humidity": "69", 
            "precip": "0.0", 
            "pressure": "1016", 
            "vis": "25", 
            "cloud": "25", 
            "uvIndex": "6"
        }, 
        {
            "fxDate": "2022-03-09", 
            "sunrise": "06:23", 
            "sunset": "18:08", 
            "moonrise": "10:07", 
            "moonset": "14:11", 
            "moonPhase": "峨眉月", 
            "moonPhaseIcon": "801", 
            "tempMax": "24", 
            "tempMin": "9", 
            "iconDay": "100", 
            "textDay": "晴", 
            "iconNight": "151", 
            "textNight": "多云", 
            "wind360Day": "135", 
            "windDirDay": "东南风", 
            "windScaleDay": "3-4", 
            "windSpeedDay": "16", 
            "wind360Night": "135", 
            "windDirNight": "东南风", 
            "windScaleNight": "3-4", 
            "windSpeedNight": "16", 
            "humidity": "83", 
            "precip": "0.0", 
            "pressure": "1013", 
            "vis": "25", 
            "cloud": "25", 
            "uvIndex": "6"
        }, 
        {
            "fxDate": "2022-03-10", 
            "sunrise": "06:22", 
            "sunset": "18:09", 
            "moonrise": "10:46", 
            "moonset": "01:30", 
            "moonPhase": "上弦月", 
            "moonPhaseIcon": "802", 
            "tempMax": "25", 
            "tempMin": "12", 
            "iconDay": "101", 
            "textDay": "多云", 
            "iconNight": "151", 
            "textNight": "多云", 
            "wind360Day": "225", 
            "windDirDay": "西南风", 
            "windScaleDay": "3-4", 
            "windSpeedDay": "16", 
            "wind360Night": "135", 
            "windDirNight": "东南风", 
            "windScaleNight": "1-2", 
            "windSpeedNight": "3", 
            "humidity": "69", 
            "precip": "0.0", 
            "pressure": "1011", 
            "vis": "25", 
            "cloud": "25", 
            "uvIndex": "6"
        }
    ], 
    "refer": {
        "sources": [
            "QWeather", 
            "NMC", 
            "ECMWF"
        ], 
        "license": [
            "no commercial use"
        ]
    }
}
```
我们需要最高温 最低温 天气情况 以及 风向和风力

可以在格式化后json中很清楚的看到，我们需要的最高温最低温，天气情况，风向风力都在daily中

```python
def get_weather(name):
    url = 'https://devapi.qweather.com/v7/weather/3d?location=118.89,31.90&key=key'
    res = requests.get(url)
    if res.json()['code'] == 200:
        data = res.json()
        return get_content(data,name)  # 返回拼接好的数据
    else:
        return False
print(get_weather('阿扬'))
def get_content(data, name):
    weekday = get_week_day(datetime.datetime.now())
    tempMax = data['daily'][0]['tempMax']  # 最高温
    tempMin = data['daily'][0]['tempMin']  # 最低温
    textDay = data['daily'][0]['textDay']  # 天气情况 晴、多云..
    windDirDay = data['daily'][0]['windDirDay']  # 风向
    windScaleDay = data['daily'][0]['windScaleDay']  # 风力
    content = '早上好！' + name + '！\n' + weekday + ' 的天气是 ' + textDay + '\n最高温度为' + tempMax + '° ' + '最低温度为' + tempMin + '° ' + '\n风向为 ' + windDirDay + ' 风力为' + windScaleDay + '级'
    return content
```
## 发送qq
获取完数据之后，我们就需要进行数据的推送

```python
def send_qq(number):
    if get_weather(get_user(number)):
        data = get_weather(get_user(number))
        url = 'https://qmsg.zendee.cn/send/key?qq=' + number + '&msg=' + data
        res = requests.get(url)
        if not res.json()['success']:
            send_mail(number + '@qq.com', '机器人出现故障，请联系管理员1972076517及时修复', 'Qmsg推送报错')
    else:
        send_mail('1972076517@qq.com', '获取天气数据失败，请联系管理员1972076517及时修复', '天气数据推送报错')

```
## 出现故障需要邮箱通知
由于qmsg可能会出现故障，所以我们需要邮箱向管理员推送信息，以便及时修复

```python
def send_mail(mail, content, title):
    number = 'qq@qq.com'
    password = 'key'
    to_addr = mail
    smtp_server = 'smtp.qq.com'
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = Header('暴力扬消息推送')
    msg['To'] = Header(to_addr)
    msg['Subject'] = Header(title)
    server = smtplib.SMTP_SSL(host=smtp_server)
    server.login(number, password)
    server.sendmail(number, to_addr, msg.as_string())

```
## 定时推送
创建云函数，点击触发管理
![在这里插入图片描述](https://img-blog.csdnimg.cn/5d1af8215bb34b58930dfe44d3c6dfc2.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAVmlvbGVudC1BeWFuZw==,size_20,color_FFFFFF,t_70,g_se,x_16)

设置触发时间
![在这里插入图片描述](https://img-blog.csdnimg.cn/fd8c2c67d8364b4fb440cdb33cf1050f.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAVmlvbGVudC1BeWFuZw==,size_20,color_FFFFFF,t_70,g_se,x_16)


```python
0 0 8 * * * *
```

意思是每天早上八点进行调用

## 关于cron详细说明
### Cron 表达式
创建定时触发器时，用户能够使用标准的 Cron 表达式的形式自定义何时触发。定时触发器现已推出秒级触发功能，为了兼容老的定时触发器，因此 Cron 表达式有两种写法。


#### Cron 表达式语法一（推荐）
Cron 表达式有七个必需字段，按空格分隔。
						
| 第一位 | 第二位 | 第三位 | 第四位 | 第五位 | 第六位 | 第七位 |
|----------|----------|----------|---------|----------|----------|----------|
| 秒 | 分钟 | 小时 | 日 | 月 | 星期 | 年 |

其中，每个字段都有相应的取值范围：

| 字段 | 值 | 通配符 |
|-------|-------|--------|
| 秒 | 0 - 59的整数 | , - * / |
| 分钟 | 0 - 59的整数 | , - * / |
| 小时 | 0 - 23的整数 | , - * / |
| 日 | 1 - 31的整数（需要考虑月的天数） | , - * / |
| 月 | 1 - 12的整数或 JAN,FEB,MAR,APR,MAY,JUN,JUL,AUG,SEP,OCT,NOV,DEC | , - * / |
| 星期 |0 - 6的整数或 SUN,MON,TUE,WED,THU,FRI,SAT。其中0指星期日，1指星期一，以此类推 | , - * / |
| 年 | 1970 - 2099的整数 | , - * / |

#### Cron 表达式语法二（不推荐）
Cron 表达式有五个必需字段，按空格分隔。

| 第一位 | 第二位 | 第三位 | 第四位 | 第五位 |
|----------|----------|----------|---------|----------|
| 分钟 | 小时 | 日 | 月 | 星期 |

其中，每个字段都有相应的取值范围：

| 字段 | 值 | 通配符 |
|---------|---------|---------|
| 分钟 | 0 - 59的整数 | , - * / |
| 小时 | 0 - 23的整数 | , - * / |
| 日 | 1 - 31的整数（需要考虑月的天数） | , - * / |
| 月 | 1 - 12的整数或 JAN,FEB,MAR,APR,MAY,JUN,JUL,AUG,SEP,OCT,NOV,DEC | , - * / |
| 星期 | 0 - 6的整数或 SUN,MON,TUE,WED,THU,FRI,SAT。其中0指星期日，1指星期一，以此类推 | , - * / |

#### 通配符
<table>
	<tr>
		<th>通配符</th>
		<th>含义</th>
	</tr>
	<tr>
		<td width="15%">,（逗号）</td>
		<td> 代表取用逗号隔开的字符的并集。例如：在“小时”字段中 1,2,3 表示1点、2点和3点</td>
	</tr>
	<tr>
		<td>-（破折号）</td>
		<td> 包含指定范围的所有值。例如：在“日”字段中，1 - 15包含指定月份的1号到15号</td>
	</tr>
	<tr>
		<td>* （星号） </td>
		<td>表示所有值。在“小时”字段中，* 表示每个小时</td>
	</tr>
	<tr>
		<td>/ （正斜杠）</td>
		<td>指定增量。在“分钟”字段中，输入1/10以指定从第一分钟开始的每隔十分钟重复。例如，第11分钟、第21分钟和第31分钟，以此类推</td>
	</tr>
</table>

### 注意事项
在 Cron 表达式中的“日”和“星期”字段同时指定值时，两者为“或”关系，即两者的条件分别均生效。

### 示例
下面展示了一些 Cron 表达式和相关含义的示例：

| 表达式 |相关含义 | 
|---------|---------|
| `*/5 * * * * * *` | 表示每5秒触发一次 | 
|`0 15 10 1 * * *`|表示在每月的1日的上午10:15触发|
|`0 15 10 * * MON-FRI *`|表示在周一到周五每天上午10:15触发|
|`0 0 10,14,16 * * * *`|表示在每天上午10点，下午2点，4点触发|
|`0 */30 9-17 * * * *`|表示在每天上午9点到下午5点每半小时触发|
|`0 0 12 * * WED *`|表示在每个星期三中午12点触发|
