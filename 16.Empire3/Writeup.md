<h3> Challenge #16 Empire-3</h3>
<blockquote><i>Agent 513! One of your dastardly colleagues is laughing very sinisterly! Can you access his todo list and discover his nefarious plans? https://2019shell1.picoctf.com/problem/45132/ (link) or http://2019shell1.picoctf.com:45132</i></blockquote>
<br>
In the Empire2 we saw that input was not sanitized for SSTI. So logging in as a random user and going back to our lovely todo list I've tried {{7*7}}.
And it did evaluate to 49...so SSTI is still a thing. Next was obviously {{conf.items()}} which evaluated to full config info , which showed us a Secret Key.