<blockquote><i>Can you break into this super secure portal? https://2019shell1.picoctf.com/problem/45147/ (link) or http://2019shell1.picoctf.com:45147</i></blockquote>


In this challenge we have login form that is doing password validation on client side.  

If we view source or just inspect body of the html file, we can see this script.  

```javascript
 function verify() {
    checkpass = document.getElementById("pass").value;
    split = 4;
    if (checkpass.substring(0, split) == 'pico') {
      if (checkpass.substring(split*6, split*7) == 'a60f') {
        if (checkpass.substring(split, split*2) == 'CTF{') {
         if (checkpass.substring(split*4, split*5) == 'ts_p') {
          if (checkpass.substring(split*3, split*4) == 'lien') {
            if (checkpass.substring(split*5, split*6) == 'lz_4') {
              if (checkpass.substring(split*2, split*3) == 'no_c') {
                if (checkpass.substring(split*7, split*8) == '3}') {
                  alert("Password Verified")
                  }
                }
              }
            }
          }
        }
      }
    }
    else {
      alert("Incorrect password");
    }
  }
```

So let's sort of reverse engineer this one.So we can see that string is being cut using variable split as an argument.We are going to order this from lowest to highest split number that is getting multiplied.<br>

```javascript
(checkpass.substring(0, split) == 'pico')
(checkpass.substring(split, split*2) == 'CTF{')
(checkpass.substring(split*2, split*3) == 'no_c')
(checkpass.substring(split*3, split*4) == 'lien')
(checkpass.substring(split*4, split*5) == 'ts_p')
(checkpass.substring(split*5, split*6) == 'lz_4')
(checkpass.substring(split*7, split*8) == '3}')
```


<b>FLAG : picoCTF{no_clients_plz_43}</b>
