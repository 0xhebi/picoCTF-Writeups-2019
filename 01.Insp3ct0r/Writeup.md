<blockquote>
<i>
Kishor Balan tipped us off that the following code may need inspection: https://2019shell1.picoctf.com/problem/61676/ (link) or http://2019shell1.picoctf.com:61676</i></blockquote>


Inspect warmup, lets use CURL to fetch our pages  

<code>curl -G https://2019shell1.picoctf.com/problem/61676/ https://2019shell1.picoctf.com/problem/61676/mycss.css https://2019shell1.picoctf.com/problem/61676/myjs.js | egrep -Eo 'flag:.{0,17}' -A1 | cut -c 6- | xargs</code>  

<b>FLAG : picoCTF{tru3_d3 t3ct1ve_0r_ju5t _lucky?1638dbe7} </b>