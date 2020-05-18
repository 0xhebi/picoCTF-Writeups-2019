<h3>Challange #14 Empire2</h3>
<blockquote><i>Well done, Agent 513! Our sources say Evil Empire Co is passing secrets around when you log in: https://2019shell1.picoctf.com/problem/6362/ (link), can you help us find it? or http://2019shell1.picoctf.com:6362</i></blockquote><br>

Here we have Empire2, with same website.
Create a user and login, as in Empire 1.<br>So I've tried testing if they protected their input this time on the Add todo page, with some of previous SQLite injections , and all of them didn't work and were represented as a normal string.So since SSTI is usual attack for picoCTF i gave it a try with <code>{{7*7}}</code> and it evaluated to 49.<br>Ok great now I just want to check conf items <code>{{conf.items()}}</code><br>
And we got this :

![Alt_text](https://github.com/DejanJS/picoCTF-Writeups-2019/blob/master/14.Empire2/ss2.png)

I was trying to expose the secret key and hoping the flag is there but that flag wasn't the real one. So I've looked around a little bit and saw that session cookie seemed quite odd. From SSTI i knew this application was running on Flask so i tried using Flask cookie decoder.

![Alt_text](https://github.com/DejanJS/picoCTF-Writeups-2019/blob/master/14.Empire2/ss.png)

<br>
And we got our flag :<br> <b>FLAG : picoCTF{its_a_me_your_flag0994faa6} </b>