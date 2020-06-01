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

<br> So...we have serialized array, from there I've tried changing username to admin and password to admin and encoding it back to base64 but unfortunately that didn't work.
