<h3>Challenge #12 JaWT Scratchpad</h3>
<blockquote><i>Check the admin scratchpad! https://2019shell1.picoctf.com/problem/32267/ or http://2019shell1.picoctf.com:32267</i></blockquote>

Another site with another login register sort of form.

![alt text](https://github.com/DejanJS/picoCTF-Writeups-2019/blob/master/12.JaWT%20Scratchpad/Screenshot.png)

If you write any kind of input we are getting just getting to the welcome page with textarea as a scratchpad where you can type any input.Tho you are given one sort of a tip:<br> <quote><i>"You can use your name as a log in, because that's quick and easy to remember! If you don't like your name, use a short and cool one like John!"</i></quote> <br>By John they are referring to tool called John the Ripper well known cracking password,hashes and etc tool.When i registered I checked my cookies and i received JWT token. JWT has 3 sort of 'building' blocks.<br>They are :
<ol>
<li>Header</li>
<li>Payload</li>
<li>Signature</li>
</ol>
In the Header we have type of token which is JWT and Signature or encryption algorithm.<br>In the Payload we usually have user information like name , subject (whom token refers to) ,iat (time). <br> And for the last Signature has it's formula of signing the token itself for e.g <code>hmac256(base64UrlEncode(header) + '.' + base64UrlEncode(payload),your secret)</code><br>  
More info on JWT <a href="https://jwt.io/introduction/">here</a>.<br>
Ok so the challenge here is to crack the secret hash using John The Ripper or any other tool , since i found Hashcat to do it's job just fine, I avoided John.<br>
We are going to need some wordlist or dictionary for this. Since Hashcat has alot of attack modes which is out of this topic,you can read more about Hashcat <a href="https://hashcat.net/hashcat/">here.</a><br>I will use the most common rockyou.txt wordlist for this one.<br>

![alt text](https://github.com/DejanJS/picoCTF-Writeups-2019/blob/master/12.JaWT%20Scratchpad/hashcat.png)

<br></br>As you can see after cracking the hash we got 'ilovepico' which is the secret. Now all we have to do is use that secret and change payload to admin and recreate the token.<br></br>And we got our flag  :<br> </br>

![alt text](https://github.com/DejanJS/picoCTF-Writeups-2019/blob/master/12.JaWT%20Scratchpad/flag.png)

<br></br>
<b>FLAG :  picoCTF{jawt_was_just_what_you_thought_6ba7694bcc36bdd4fdaf010b2ec1c2c3}</b>