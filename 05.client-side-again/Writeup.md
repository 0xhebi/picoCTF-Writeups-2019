<h3>Challenge #5 client side again </h3>

<blockquote><i>Can you break into this super secure portal? https://2019shell1.picoctf.com/problem/45137/ (link) or http://2019shell1.picoctf.com:45137</i></blockquote>  

This challenge is similar to second challenge.If we view page source or inspect this page we will see.  

```javascript
<script type="text/javascript">
  var _0x5a46=['55670}','_again_0','this','Password\x20Verified','Incorrect\x20password','getElementById','value','substring','picoCTF{','not_this'];(function(_0x4bd822,_0x2bd6f7){var _0xb4bdb3=function(_0x1d68f6){while(--_0x1d68f6){_0x4bd822['push'](_0x4bd822['shift']());}};_0xb4bdb3(++_0x2bd6f7);}(_0x5a46,0x1b3));var _0x4b5b=function(_0x2d8f05,_0x4b81bb){_0x2d8f05=_0x2d8f05-0x0;var _0x4d74cb=_0x5a46[_0x2d8f05];return _0x4d74cb;};function verify(){checkpass=document[_0x4b5b('0x0')]('pass')[_0x4b5b('0x1')];split=0x4;if(checkpass[_0x4b5b('0x2')](0x0,split*0x2)==_0x4b5b('0x3')){if(checkpass[_0x4b5b('0x2')](0x7,0x9)=='{n'){if(checkpass[_0x4b5b('0x2')](split*0x2,split*0x2*0x2)==_0x4b5b('0x4')){if(checkpass[_0x4b5b('0x2')](0x3,0x6)=='oCT'){if(checkpass[_0x4b5b('0x2')](split*0x3*0x2,split*0x4*0x2)==_0x4b5b('0x5')){if(checkpass['substring'](0x6,0xb)=='F{not'){if(checkpass[_0x4b5b('0x2')](split*0x2*0x2,split*0x3*0x2)==_0x4b5b('0x6')){if(checkpass[_0x4b5b('0x2')](0xc,0x10)==_0x4b5b('0x7')){alert(_0x4b5b('0x8'));}}}}}}}}else{alert(_0x4b5b('0x9'));}}
</script>
```
This chunk of code is <a href="https://en.wikipedia.org/wiki/Obfuscation_(software)"  >obfuscated</a>. To make this more readable you can use some of the deobfuscators that are out there on the web. I will use <a href="http://www.jsnice.org/">JS nice</a> for our example.  

After doing that we get more readable code :  

```javascript  
'use strict';
/** @type {!Array} */
var _0x5a46 = ["55670}", "_again_0", "this", "Password Verified", "Incorrect password", "getElementById", "value", "substring", "picoCTF{", "not_this"];
(function(data, i) {
  var write = function(isLE) {
    for (; --isLE;) {
      data["push"](data["shift"]());
    }
  };
  write(++i);
})(_0x5a46, 435);
var _0x4b5b = function(level, ai_test) {
  level = level - 0;
  var rowsOfColumns = _0x5a46[level];
  return rowsOfColumns;
};
function verify() {
  checkpass = document[_0x4b5b("0x0")]("pass")[_0x4b5b("0x1")];
  split = 4;
  if (checkpass[_0x4b5b("0x2")](0, split * 2) == _0x4b5b("0x3")) {
    if (checkpass[_0x4b5b("0x2")](7, 9) == "{n") {
      if (checkpass[_0x4b5b("0x2")](split * 2, split * 2 * 2) == _0x4b5b("0x4")) {
        if (checkpass[_0x4b5b("0x2")](3, 6) == "oCT") {
          if (checkpass[_0x4b5b("0x2")](split * 3 * 2, split * 4 * 2) == _0x4b5b("0x5")) {
            if (checkpass["substring"](6, 11) == "F{not") {
              if (checkpass[_0x4b5b("0x2")](split * 2 * 2, split * 3 * 2) == _0x4b5b("0x6")) {
                if (checkpass[_0x4b5b("0x2")](12, 16) == _0x4b5b("0x7")) {
                  alert(_0x4b5b("0x8"));
                }
              }
            }
          }
        }
      }
    }
  } else {
    alert(_0x4b5b("0x9"));
  }
}
;  
```
So if we investigate this chunk of code we can see that is doing the comparison to the array. Let's break it down.  
If we want this code to look more understandable we can replace those hexadecimal values into some string so we get some proper name for our variables.
This is how i did it :  

```javascript  
'use strict';
var our_array = ["55670}", "_again_0", "this", "Password Verified", "Incorrect password", "getElementById", "value", "substring", "picoCTF{", "not_this"];
//array after write function  ["getElementById", "value", "substring", "picoCTF{", "not_this", "55670}", "_again_0", "this", "Password Verified", "Incorrect password"]
(function(data, i) {
  var write = function(isLE) {
    for (; --isLE;) {
      data["push"](data["shift"]());
    }
  };
  write(++i);
})(our_array, 435);
var our_func = function(level, ai_test) {
  level = level - 0;
  var rowsOfColumns = our_array[level];
  return rowsOfColumns;
};
function verify() {
  checkpass = document[our_func("0x0")]("pass")[our_func("0x1")]; // document.getElementyById('pass').value
  split = 4;
  if (checkpass[our_func("0x2")](0, split * 2) == our_func("0x3")) {
    if (checkpass[our_func("0x2")](7, 9) == "{n") {
      if (checkpass[our_func("0x2")](split * 2, split * 2 * 2) == our_func("0x4")) {
        if (checkpass[our_func("0x2")](3, 6) == "oCT") {
          if (checkpass[our_func("0x2")](split * 3 * 2, split * 4 * 2) == our_func("0x5")) {
            if (checkpass["substring"](6, 11) == "F{not") {
              if (checkpass[our_func("0x2")](split * 2 * 2, split * 3 * 2) == our_func("0x6")) {
                if (checkpass[our_func("0x2")](12, 16) == our_func("0x7")) {
                  alert(our_func("0x8"));
                }
              }
            }
          }
        }
      }
    }
  } else {
    alert(our_func("0x9"));
  }
}
;
```  

So let's explain what's going on here. We have our IIFE function that has another function inside of it called write(),function is iterating over the array and reordering it. We also have 'our_func' that is basically just returning us value  from the array.  

If we look at verify() function we can see that check pass is just targeting document node value of password input.And then we have our IF nesting(nasty,pun intend) that is doing substring on the input value and comparing it to the desired value which is in our case flag.

Now we just have to break this down a little bit and we get the flag :   

```javascript
  if (checkpass[our_func("0x2")](0, split * 2) == our_func("0x3")) { // picoCTF{ 
      if (checkpass[our_func("0x2")](7, 9) == "{n") { // picoCTF{n
        if (checkpass[our_func("0x2")](split * 2, split * 2 * 2) == our_func("0x4")) { // picoCTF{not_this == not_this
          if (checkpass[our_func("0x2")](3, 6) == "oCT") { // picoCTF{not_this substring(3,6) == oCT
          if (checkpass[our_func("0x2")](split * 2 * 2, split * 3 * 2) == our_func("0x6")) {//picoCTF{not_this_again_0
              if (checkpass["substring"](6, 11) == "F{not") { 
            if (checkpass[our_func("0x2")](split * 3 * 2, split * 4 * 2) == our_func("0x5")) {// picoCTF{not_this_again_055670}
                  if (checkpass[our_func("0x2")](12, 16) == our_func("0x7")) {
                    alert(our_func("0x8"));
                  }
                }
              }
            }
          }:
        }
      }
    } else {
      alert(our_func("0x9"));
    }
```

<b>FLAG : picoCTF{not_this_again_055670} </b>


