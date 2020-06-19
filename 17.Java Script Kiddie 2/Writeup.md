<h3>Challenge #17 Java Script Kiddie 2</h3>
<blockquote><i>The image link appears broken... twice as badly... https://2019shell1.picoctf.com/problem/12281 or http://2019shell1.picoctf.com:12281</i></blockquote>

This one looks like a previous challenge with some differences. Let's take a look at page source this time : <br>
```javascript
			var bytes = [];
			$.get("bytes", function(resp) {
				bytes = Array.from(resp.split(" "), x => Number(x));
			});

			function assemble_png(u_in){
				var LEN = 16;
				var key = "00000000000000000000000000000000";
				var shifter;
				if(u_in.length == key.length){
					key = u_in;
				}
				var result = [];
				for(var i = 0; i < LEN; i++){
					shifter = Number(key.slice((i*2),(i*2)+1));
					for(var j = 0; j < (bytes.length / LEN); j ++){
						result[(j * LEN) + i] = bytes[(((j + shifter) * LEN) % bytes.length) + i]
					}
				}
				while(result[result.length-1] == 0){
					result = result.slice(0,result.length-1);
				}
				document.getElementById("Area").src = "data:image/png;base64," + btoa(String.fromCharCode.apply(null, new Uint8Array(result)));
				return false;
			}
```
The algorithm is sort of same , but now we have key of 32 characters. And shifter that is taking every odd character and converts it into a number.<br>
I will use the same script but modified to our needs to solve this. Check the <a href="https://github.com/DejanJS/picoCTF-Writeups-2019/blob/master/13.Java%20Script%20Kiddie/Writeup.md">Java Script Kiddie part 1</a> writeup for more info. I've took my script from the part 1 and made some adjustments , you can check it <a href="https://github.com/DejanJS/picoCTF-Writeups-2019/blob/master/17.Java%20Script%20Kiddie%202/script.js">here.</a><br>
The script is more of the less the same , we are just adjusting the shifter to take every odd number and filling the rest of characters to match length of the key which is 32. The script at the end generates the possible combinations of the key, the one that worked was : <code>30703080109030600050301080506090</code><br>

After that we are getting again QR code image which we put it through qr decoder and we get the flag:<br>
![alt_text](https://github.com/DejanJS/picoCTF-Writeups-2019/blob/master/17.Java%20Script%20Kiddie%202/flag.png)
<br>
<b>FLAG : picoCTF{3aa9bd64cb6883210ee0224baec2cbb4}<b>