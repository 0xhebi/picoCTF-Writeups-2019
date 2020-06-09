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
This signature indicates that the remainder of the file contains a single PNG image, consisting of a series of chunks beginning with an IHDR chunk and ending with an IEND chunk.</blockquote><br>
This image will give us better insight :<br>
![alt_text](https://github.com/DejanJS/picoCTF-Writeups-2019/blob/master/13.Java%20Script%20Kiddie/file-structure.png)
<br>
The script above is basically algorithm that takes key of 16 chars input that will generate array of image bytes and then decode it to base64 which will represent image.<br>
So from all of that research I came to conclusion that our result array has to start with png signature and to end with IEND.So we will have to get the right key that will search for index in a bytes array (where our bytes for png are). I've made a <a href="https://github.com/DejanJS/picoCTF-Writeups-2019/blob/master/13.Java%20Script%20Kiddie/script.js">script</a> that will give me the possible keys that would work.<br>Before I get into explaining how I did it , the one thing that I was trying and failing at was trying to order bytes array footer from second part of my key(8-16chars) which wasn't possible. The thing that actually worked was bruteforcing combinations of key with second part of the key being correct bytes for IHDR. The way i realized that is by comparing 5-10 random images of png format through hexeditor. And from the above PNG File Structure docs we could see that after PNG Signature are being followed by bytes of IHDR. So I just searched for those in bytes array , but having that said we would have to analyze a little bit how assemble_png function is working.<br>So let's explain what is going on, our assemble.png function is taking one parameter and if that parameter has length of 16 it is being used as our "key" as I mentioned on start. Then we are looping through our key and generating 'shifter' as charcode of every key char - 48. In the next loop we are ordering our result array which is going to be used for representing the image . Next loop is ordering our result array, for first character in our key it would be something like this : <code>result[0 * 16 + 0] = bytes[(((0+shifter)*16)% 720) + 0]</code> . So since we know that our first 8 characters of a key should match first 8 bytes of PNG Signature and other 8 characters have to match first 8 bytes of IHDR , in my script i made a function that will do that for me(gen_idx). After we find all indexes for PNG Signature and IHDR in our bytes array. We should calculate possible values for each of those and generate every possible combinations of a key.<br>Just to note (I was first trying to fit footer bytes at the end of our result array and try to see if I could make possible calculations as I mentioned before , so this could script is probably a little bit of overcomplicating things but it worked for me, I am quite sure I could have come with something more simple and there is way better solution , but oh well...).<br> After all possible values for our key we just have to convert em to valid characters using reverse shifter logic with already known index , concatanate and loop over for combinations.<br>The key that worked was 4549618526012495. The QRcode image generated from that input and all we had to do is put it into some QR decoder which you can find those online and decode it. And we got our flag : <br>
![alt_text](https://github.com/DejanJS/picoCTF-Writeups-2019/blob/master/13.Java%20Script%20Kiddie/flag.png)
<br>
<b>FLAG: picoCTF{cfbdafe5a65de4f32cce2e81e8c14a39 </b>