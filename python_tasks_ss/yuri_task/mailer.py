from email.message import EmailMessage
from email.parser import BytesParser, Parser, HeaderParser
from email.policy import default, SMTP
from email.generator import Generator
import smtplib

# writing content from a file to EmailMessage
with open('t.txt', encoding='utf-8') as f:
    m = EmailMessage()
    m.set_content(f.read())
    print(m)

print(30*'++')
#  sending mail with attachment
m['Subject'] = 'test attachment'
m['From'] = 'me'
m['To'] = 'Igor Tymoshenko <igorrrock.it@gmail.com>'


with open('a.txt', 'rb') as f:
    text = f.read()

m.add_attachment(text, maintype='text', subtype='plain', filename='b.txt')

print(m)

with smtplib.SMTP('alt4.gmail-smtp-in.l.google.com') as s:
    s.send_message(m, from_addr='me@localhost', to_addrs='igorrrock.it@gmail.com')

