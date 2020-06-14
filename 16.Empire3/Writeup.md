<h3> Challenge #16 Empire-3</h3>
<blockquote><i>Agent 513! One of your dastardly colleagues is laughing very sinisterly! Can you access his todo list and discover his nefarious plans? https://2019shell1.picoctf.com/problem/45132/ (link) or http://2019shell1.picoctf.com:45132</i></blockquote>
<br>
In the Empire2 we saw that input was not sanitized for SSTI. So logging in as a random user and going back to our lovely todo list I've tried {{7*7}}.
And it did evaluate to 49...so SSTI is still a thing. Next was obviously {{conf.items()}} which evaluated to full config info , which showed us a Secret Key. Since we know that flask cookies are signed , we can resign cookie for admin or any other user and try to login. This reminds me of the "Flask card skeleton key" from 2018 picoCTF. <br>So I used the same script that I've made for the last year , you can find it <a href="https://github.com/DejanJS/picoCTF-Writeups/blob/master/14.Flaskcards%20Skeleton%20Key/CTF_cookie.py">here</a>. First decode flask cookie at <a href="https://www.kirsle.net/wizards/flask-session.cgi">Flask Session Cookie Decoder</a>.<br>After that you will get json object with properties. We have 2 users in our employees list , and one of those is admin. So either was userid 1 or 2 , tested both of them by generating both session cookies and checking todo list for a flag, and it seems userid 2 was an admin.<br>

![alt_text](https://github.com/DejanJS/picoCTF-Writeups-2019/blob/master/16.Empire3/flag.png)

<br>
<b>FLAG : picoCTF{cookies_are_a_sometimes_food_8038d44f}</b>