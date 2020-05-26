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
<br>We can see that there is some logic for displaying an png image here.<br>We have get request for "bytes" which is in this case array with length of 720. Our assemble_png function has default key with 16 characters. We are supposed to provide key through an input with length of 16 and try to generate correct array of bytes which will represent an image of png format. By doing some research i came across <a href="http://www.libpng.org/pub/png/spec/1.2/PNG-Structure.html">PNG file structure</a> in docs which has some interesting stuff there. The thing that is important is : <br>
<blockquote>The first eight bytes of a PNG file always contain the following (decimal) values:

   137 80 78 71 13 10 26 10
This signature indicates that the remainder of the file contains a single PNG image, consisting of a series of chunks beginning with an IHDR chunk and ending with an IEND chunk.</blockquote>
Which means those numbers are header or to put it this way , the script above is basically algorithm that takes key of 16 chars input that will generate array of image bytes and then decode it to base64 which will represent image.  