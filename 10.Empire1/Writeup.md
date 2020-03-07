<blockquote><i>Psst, Agent 513, now that you're an employee of Evil Empire Co., try to get their secrets off the company website. https://2019shell1.picoctf.com/problem/27357/ (link) Can you first find the secret code they assigned to you? or http://2019shell1.picoctf.com:27357</i></blockquote>  

In this challenge we have a site with login and register form.  

First things first I inspected the page to see if there is any hidden login logic in some form of script,which wasn't the case.After creating a user and logging in I've caught one thing.The session cookie looked quite odd: 

```javascript
session=.eJwlj0FqQzEMRO_idRayJEt2LvORZYmGQAv_J6vSu8fQWb95zPyWI8-4vsr9db7jVo7HKveCHTAqM7r6cFhdIeoO2-i0eA6UEUnihrMFk5upSGJl9UWQMmf20Rc1arAWmyaw6OC6Teg5g5XSWptrRjRMbyYA5hvZEiq34teZx-vnGd97jxNn776BUWVgtypNOhFNNVimwO48XXbvfcX5f4LK3wdBOT5K.XmPcqA.dDQLm8QVYSADCJMay9b9Rh3dpc0
```

So i had to determine in what framework the server was written. From previous picoCTF's i guessed with Flask. So I've tried decoding the cookie.
