#! -*- coding: utf-8 -*-


import email
import smtplib
import mimetypes


from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
from email.MIMEMultipart import MIMEMultipart


class Email(object):
    @staticmethod
    def send(eauth, esubject, eto, ecc=[], etext='', ehtml='', efrom='limanman@xiongmaitech.com'):
        srv_addr = eauth.get('smtp_host', None)
        srv_port = eauth.get('smtp_port', None)
        srv_user = eauth.get('smtp_user', None)
        srv_pass = eauth.get('smtp_pass', None)
        debug_no = eauth.get('debug_num', None)

        if__next = any(map(lambda s: s is None, ('srv_addr', 'srv_user', 'srv_pass', 'debug_no')))
        if if__next:
            return

        msgmeta = MIMEMultipart('related')
        msgmeta['Subject'] = esubject
        msgmeta['From'] = efrom
        msgmeta['To'] = ','.join(eto)
        if ecc:
            msgmeta['Cc'] = ','.join(ecc)
        msgmeta.preamble = 'This is a multi-part message in MIME format.'
        msgalternative = MIMEMultipart('alternative')
        msgmeta.attach(msgalternative)
        # 纯文本信息
        if etext.strip():
            msgtext = MIMEText(etext, 'plain', 'utf-8')
            msgalternative.attach(msgtext)

        # HTML的信息
        if ehtml.strip():
            msghtml = MIMEText(ehtml, 'html', 'utf-8')
            msgalternative.attach(msghtml)

        # 发送邮件区
        smtp = smtplib.SMTP(host=srv_addr, port=srv_port)
        smtp.set_debuglevel(debug_no)
        smtp.connect(srv_addr)
        smtp.login(srv_user, srv_pass)
        smtp.sendmail(efrom, eto, msgmeta.as_string())
        smtp.quit()
