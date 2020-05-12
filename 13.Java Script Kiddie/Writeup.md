<h3>Challenge #13 Java Script Kiddie</h3>

<blockquote><i>The image link appears broken... https://2019shell1.picoctf.com/problem/59857 or http://2019shell1.picoctf.com:59857</i></blockquote>

So in this challenge we have just a page with input and submit button.If we view page source we will see some js script : <br>
```javascript
			var bytes = [];
			$.get("bytes", function(resp) {
				bytes = Array.from(resp.split(" "), x => Number(x));
			});

			function assemble_png(u_in){
				var LEN = 16;
				var key = "0000000000000000";
				var shifter;
				if(u_in.length == LEN){
					key = u_in;
				}
				var result = [];
				for(var i = 0; i < LEN; i++){
					shifter = key.charCodeAt(i) - 48;
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
<br>We can see that there is some logic for displaying an png image here.So let's investigate what is going on.