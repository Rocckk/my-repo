#  прочитати файл, в унікоді погратися, зберегти в коремому файлі зміст.

from email.parser import BytesParser
from email.policy import default, HTTP, SMTP
from email import message_from_file
import locale
import sys



#  using convenience functions
with open("mail1", "r", encoding="utf-8") as f:
    cont = message_from_file(f, policy=default)
    print('start:----')
    print(cont)
    print('stop:----')
    with open("targ.txt", 'w', encoding="utf-8")as fp:
        fp.write(cont.as_string(maxheaderlen=90))

"""
#  reading in binary mode
with open("mail1", "rb") as f:
    cont = BytesParser(policy=default).parse(f)

for i in cont.walk():
    if i.get_content_type() == "text/plain":
        with open("targ.txt", 'wb') as fp:  
            fp.write(i.get_payload(decode=True))
"""
'''
# reading message's body withou headers
body = cont.get_body(preferencelist=('plain'))
mes = body.get_content()
with open("targ.txt", 'w', encoding="utf-8") as fp:
   fp.write(mes)
'''
"""
# simple reading and writing
with open("t.txt", "r", encoding="utf-8") as f:
    a = f.read()
    with open("targ.txt", 'w', encoding="utf-8", newline='\r\n') as fp:
        fp.write(a)
print(locale.getpreferredencoding())
"""

"""
#  loop for char comparison
with open("mail2", "r", encoding="utf-8") as f:
    a = f.read()
    print(len(a))
    with open("targ.txt", 'r', encoding="utf-8") as fp:
        b = fp.read()
        for i in range(len(a)):
            print(a[i], b[i])
            if a[i] != b[i]:
                print('!!!!!!!!!!!!!')
                break
"""

