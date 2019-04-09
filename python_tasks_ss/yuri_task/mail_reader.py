#  прочитати файл, в унікоді погратися, зберегти в коремому файлі зміст.

from email.parser import BytesParser
from email.policy import default
import locale
import sys


"""
with open("mail2", "rb") as f:
    cont = BytesParser(policy=default).parse(f)

for i in cont.walk():
    #print(i.get_content_type())
    with open("targ.txt", 'ab') as fp:
        if i.get_content_type() == "text/plain":
            print (i)
            fp.write(i.get_payload(decode=True))

body = cont.get_body(preferencelist=('plain'))
mes = body.get_content()
with open("targ.txt", 'w', encoding="utf-8") as fp:
   fp.write(mes)

 """

with open("mail2", "r", encoding="cp1251") as f:
    a = f.read()
    with open("targ.txt", 'w', encoding="cp1251") as fp:
        fp.write(a)
print(locale.getpreferredencoding())


'''
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
'''

