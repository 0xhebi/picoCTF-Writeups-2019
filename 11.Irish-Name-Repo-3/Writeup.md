<h3>Challenge #11 Irish-Name-Repo-3</h3>
<blockquote><i>There is a secure website running at https://2019shell1.picoctf.com/problem/12271/ (link) or http://2019shell1.picoctf.com:12271. Try to see if you can login as admin!</i></blockquote>

Here we have website with login page that we have to try to login as an admin obviously.  

I've tried inspecting the page to see if there is any additional script that will give me some more info.

```html
<form action="login.php" method="POST">
 <fieldset>
  <div class="form-group">
    <label for="password">Password:</label>
      <div class="controls">
        <input type="password" id="password" name="password" class="form-control">
      </div>
   </div>
   <input type="hidden" name="debug" value="0">
  <div class="form-actions">
   <input type="submit" value="Login" class="btn btn-primary">
  </div>
 </fieldset>
</form>  
```

Nothing seemed pretty unusual , except this hidden input with debug an value 0 was kinda weird.<br>I've tried inserting some random input as start that will return me login failed.I was inspecting the request to see if there is anything interesting. Nothing seemed really weird so i tried testing other input.