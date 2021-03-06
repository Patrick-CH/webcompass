import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import os


def Send_Email(filename, receivers):
    # 第三方 SMTP 服务
    mail_host = "smtp.qq.com"  # 设置服务器
    mail_user = os.getenv('MAIL_ID')  # 用户名
    mail_pass = os.getenv('MAIL_PASS') # 口令
    # print(mail_pass)
    # print(mail_user)

    sender = mail_user

    # 创建一个带附件的实例
    message = MIMEMultipart()
    message['From'] = Header("webcompass", 'utf-8')
    message['To'] = Header("user", 'utf-8')
    subject = '自动邮件不必回复'
    message['Subject'] = Header(subject, 'utf-8')

    # 邮件正文内容
    message.attach(MIMEText('自动邮件不必回复', 'plain', 'utf-8'))

    # 构造附件1，传送当前目录下的 test.txt 文件
    try:
        with open(filename, 'rb') as f:
            att1 = MIMEText(f.read(), 'base64', 'utf-8')
            att1["Content-Type"] = 'application/octet-stream'
            att1["Content-Disposition"] = 'attachment; filename="{}"'.format(filename.split('\\')[-1])
            message.attach(att1)
    except Exception:
        print("can't open the file!")
        exit(-1)

    # try:
    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())
    print("邮件发送成功")
    print(receivers)
    # except smtplib.SMTPException:
    #     print("Error: 无法发送邮件")
    #     exit(-2)


if __name__ == '__main__':
    Send_Email('D:\\Download\\20201204_232035.mp4', receivers = ['1648109733@qq.com'])