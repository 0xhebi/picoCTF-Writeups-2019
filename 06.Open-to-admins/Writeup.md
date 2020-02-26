<blockquote><i>This secure website allows users to access the flag only if they are admin and if the time is exactly 1400. https://2019shell1.picoctf.com/problem/21882/ (link) or http://2019shell1.picoctf.com:21882</i></blockquote>  

This challenge was the weirdest one so far.We had a page with flag button.Once you click the flag you get this message :  

![Alt_text](https://github.com/DejanJS/picoCTF-Writeups-2019/blob/master/06.Open-to-admins/ss.png)

Or you download default html page for <b>nginx</b> 

After inspecting network tab in dev tools to see what is going with requests I haven't found anything interesting.We have session cookie <br> <code>session=.eJwdi1EKwkAMBa_yyM_-iAfwBp5BiixttKG7CSQRKaV3d_FrYJg56PlqNVYOuj0OQg7Qt7qKvulC99IR5r5DEotxaEk0sw1NNsZuH1Rn5MqoSxeF-ShL_I3oPFaeEymdrzSd0_kDY1ImxQ.XlY__g.VmZq_8ZJdDDnY0RSf1j3gBeMHAI</code><br> and it seems that server is written in Flask. I've tried multiple things which most of them were dumb but i had no ideas.</br>
Tried decoding session cookie didn't get me far. Apparently flag can only be achieved by being admin and if the time is exactly <b>1400</b>.<br> I've tried creating cookie : 
</br>

```javascript
document.cookie='admin=true;Expires:22 Feb 14:00:00GMT'
```

And similar things with Max-Age converting hours into milisecond didn't get me far.  

So what we had to do was only this   

```javascript
document.cookie ='admin=true'
document.cookie='time=1400'
```

And we get the flag.<br></br><br>
<b>Flag : picoCTF{0p3n_t0_adm1n5_b6ea8359} </b>
<br></br><br>
That totally makes any sense right???
