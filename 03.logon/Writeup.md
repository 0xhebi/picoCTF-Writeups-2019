<h3>Challenge #3 Logon </h3>

<blockquote><i>The factory is hiding things from all of its users. Can you login as logon and find what they've been looking at? https://2019shell1.picoctf.com/problem/49907/ (link) or http://2019shell1.picoctf.com:49907</i></blockquote>  

In this one we have login form , when we type in any kind of input we are successfully logged in but we are not getting the flag. If you inspect the page there is nothing interesting there. Checking network tab for observing request we can see that cookie has a value of admin=False. This is just one of those challenges that we had back then in 2018.Set cookie value admin to <b>True</b> and refresh and we get the flag.  

<b>Flag : picoCTF{th3_c0nsp1r4cy_l1v3s_9e21365b}</b>

