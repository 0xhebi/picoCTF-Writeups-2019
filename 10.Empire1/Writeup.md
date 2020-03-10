<blockquote><i>Psst, Agent 513, now that you're an employee of Evil Empire Co., try to get their secrets off the company website. https://2019shell1.picoctf.com/problem/27357/ (link) Can you first find the secret code they assigned to you? or http://2019shell1.picoctf.com:27357</i></blockquote>  

In this challenge we have a site with login and register form.  

First things first I inspected the page to see if there is any hidden login logic in some form of script,which wasn't the case.After creating a user and logging in I've caught one thing.The session cookie looked quite odd: 

```javascript
session=.eJwlj0FqQzEMRO_idRayJEt2LvORZYmGQAv_J6vSu8fQWb95zPyWI8-4vsr9db7jVo7HKveCHTAqM7r6cFhdIeoO2-i0eA6UEUnihrMFk5upSGJl9UWQMmf20Rc1arAWmyaw6OC6Teg5g5XSWptrRjRMbyYA5hvZEiq34teZx-vnGd97jxNn776BUWVgtypNOhFNNVimwO48XXbvfcX5f4LK3wdBOT5K.XmPcqA.dDQLm8QVYSADCJMay9b9Rh3dpc0
```

So i had to determine in what framework the server was written. From previous picoCTF's i guessed with Flask. So I've tried decoding the cookie. And I was right since this JSON object was result of it.  

```javascript  
{
    "_fresh": true,
    "_id": "2802e1442c7c9c0d870e11114a983d4b9269ef36ca2b5e43caa766f2147cd30f6bbf898d35350dd4a7f04679418702cfbe473fa55bdbee52fc5a600ac7942143",
    "csrf_token": "c34f88c0ac916928a16568333b7a0da704cc4bc6",
    "user_id": "3"
}  
```  
So we do see that user_id value is 3.<br>
Have in mind <br><quote>Flask, by default, uses the URL-safe signed serializer "itsdangerous" to encode its client-side session cookies. A Flask app uses a secret key to sign the session cookie so that the client can't modify it.</quote><br>  
Which means if we could spoof the secret key we would be able to modify the cookie by swapping the value to 1 which would be admin value , and get the session cookie for admin.  

So I've registered account with some random name and then you can see the multiple pages as a user.You see Employees listing,Add todo ,Your todos.  
Empoyees listing was interesting because it looks like a typical SQL table , 3 columns with fields Employee id, Username, Name.<br> Then in Add Todo we have a input field where we can input some text and that is going into list on the page Your Todos.
<br><br>
First I've tried testing the input simply with providing <b>ASCII alphabet</b> you can either google or just make this one liner in python :<br>
<br>
```python
"".join(chr(x) for x in range(32,127))
```

That instantly crashed and gave me internal server 500 error.<br>After that I tried all upper and lowercase letters from A-Z. Which didn't show any strange behaviour. However when I tried single quotes ' and other math logical operators and some of them crashed again.  
<br>
I've tried simple classic SQL injection for authentication OR 1 '=' 1 which weirdly evaluated to 0. <br>
That was very weird and i had to realize what is being filtered out.  

I've tried doing '+ 12 +' which evaluated into 12.So i've tried simple expression '+ 1 + 2  +' which evaluated into 3. Which was pretty nice.<br> I was getting somewhere with that.   

After that i tried taking it step further and making query so i tried '+ SELECT +' and that crashed. So i realized that those words must be filtered and i wanted to try query inside of parantheses . <br>  
so i've tried '+ (SELECT 1) +' and that evaluated to 1. From that point i determined that i can do queries.
 

