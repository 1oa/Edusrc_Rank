import requests
import re
import os
import smtplib
from email.header import Header
from email.mime.text import MIMEText

#####
#####
userId=8451  # edusrc的用户id，在个人主页的url里有
receivers = ['xxxxxxxx@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

#####
#####
# 第三方 SMTP 服务
mail_host = "smtp.126.com"      # SMTP服务器
mail_user = "xxxxxx@126.com"                  # 用户名
mail_pass = "XXXXXXXXXXXXXXXX"               # 授权密码，非登录密码
sender = 'xxxxxx@126.com'    # 发件人邮箱(最好写全, 不然会失败)

def sendEmail(getrank):
    message = MIMEText("Rank Update::"+str(getrank), 'plain', 'utf-8')  # 内容, 格式, 编码
    message['From'] = "{}".format(sender)
    message['To'] = ",".join(receivers)
    message['Subject'] = "Rank Update::"+str(getrank)
 
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
        smtpObj.login(mail_user, mail_pass)  # 登录验证
        smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
        print("Mail sent")
    except smtplib.SMTPException as e:
        print(e)

def getRank():
    url="https://src.sjtu.edu.cn/profile/"+str(userId)
    r = requests.get(url)
    rule = r'Rank： (.*?)\n'
    rank = re.findall(rule, r.text)[0]
    return rank


getrank=getRank()

if os.path.exists('edurank.txt'):
    with open("edurank.txt") as f:
        rank = f.read()
    if(getrank!=rank and rank!=''):
        sendEmail(getrank)
        print('Rank Update:'+str(getrank))
    else:
        print('Not updated')
else:
    with open("edurank.txt", mode='w+', encoding='utf-8') as ff:
        ff.write(getrank)
        print('newfile')
