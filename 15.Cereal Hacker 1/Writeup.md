<h3>Challenge #15 Cereal hacker 1</h3>
<blockquote><i>Login as admin. https://2019shell1.picoctf.com/problem/12279/ or http://2019shell1.picoctf.com:12279</i></blockquote>

This was a weird one...anyway...<br>
We have a page with a login form, from url we can think that is most likely php if something really odd is not happening on the server side. I've tried doing some path traversal for some possible LFI like <code> ../../../../etc/passwd/ </code> or adding %0 for poisoning null byte. But didn't have any luck with any of those , was just getting file not found or something. Also I've tried various <code> php://filter </code> wrapper for some sort of injection but that didn't work as well. I've looked for request/response behaviour but nothing seemed odd. I've tried to see if there is /admin page. And there was one.<br>It's basic page saying that I am not an admin with button to go back to login screen. I view source the page and saw something interesting that could be potentially initial vector.<br>
<blockquote> onclick="document.cookie='user_info=; expires=Thu, 01 Jan 1970 00:00:18 GMT; domain=; path=/;'"</blockquote><br>
So we have some cookie user_info that is clearing the value. (At this point when I was doing the challenge description of challenge was missing, as well as any hints, I found out that you can try logging as guest).<br>By logging as guest you are getting to regular_user page. And where you are getting the cookie.

```javascript 
document.cookie
"user_info=TzoxMToicGVybWlzc2lvbnMiOjI6e3M6ODoidXNlcm5hbWUiO3M6NToiZ3Vlc3QiO3M6ODoicGFzc3dvcmQiO3M6NToiZ3Vlc3QiO30%253D" 
```
<br> Ok I can see the value is base64 so let's decode this.<br>

```python
import base64
cookie = 'TzoxMToicGVybWlzc2lvbnMiOjI6e3M6ODoidXNlcm5hbWUiO3M6NToiZ3Vlc3QiO3M6ODoicGFzc3dvcmQiO3M6NToiZ3Vlc3QiO30='
print(base64.b64decode(cookie)) # b'O:11:"permissions":2:{s:8:"username";s:5:"guest";s:8:"password";s:5:"guest";}'
 ```

<br> So...we have serialized array, from there I've tried changing username to admin and password to admin and encoding it back to base64 but unfortunately that didn't work. So the thing that I can try is , bruteforcing username and password with some SQL injection payload. So I made a script that will do this to me. I will explain shortly how it works,check the script <a href="https://github.com/DejanJS/picoCTF-Writeups-2019/blob/master/15.Cereal%20Hacker%201/script.py">here</a> btw.<br>
So first thing is that we are going to take cookie and decode it and convert it into a string, then we will open file with our SQL injection payload I've used auth.txt from <a href="https://github.com/swisskyrepo/PayloadsAllTheThings">Payload All things</a> we will basically loop over each payload replace it in our cookie value string , and encode it back to b64 as encoded utf-8 and the decode utf-8 to get proper value for a cookie , make request for each generated cookie with sql injection payload.<br>
And after I started the script we've got the flag. Payload that worked was <blockquote>O:11:"permissions":2:{s:8:"username";s:8:"admin' #";s:8:"password";s:0:"";}<br>admin' #"</blockquote><br>
<b>FLAG : picoCTF{3fba6964d680deb73b38b7f2916df7d5}</b>
