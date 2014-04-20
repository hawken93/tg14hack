<!doctype html>
<html>
<head></head>
<body>
<p>We have now realized that we indeed needed to shape up and use passwords. Good luck with this one!</p>
<form action="" method="post">
	<table>
		<tr>
			<td>User</td><td><input type="text" name="user" <?php if(isset($_POST['user'])) echo "value=\"".$_POST['user']."\""; ?> /></td>
		</tr>
		<tr>
			<td>Password</td><td><input type="text" name="pass" <?php if(isset($_POST['pass'])) echo "value=\"".$_POST['pass']."\""; ?> /></td>
		</tr>
		<tr>
			<td colspan="2"><input type="submit" /></td>
		</tr>
	</table>
</form>
<?php
/*
mysql> create table users (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	user VARCHAR(50),
	password VARCHAR(50)
	);
	grant SELECT on users.* TO web07@localhost IDENTIFIED BY '123123'
	insert into users (user,password) VALUES ("AwesomeUser7331!", "god");
*/
	$token = "if(\$str==\"\\\'\") ouch();";
	if(isset($_POST['user']) && isset($_POST['pass'])){


		$user = $_POST['user'];
		$user = str_replace("'",'\\\'', $user);
		$pass = $_POST['pass'];
		$pass = str_replace("'",'\\\'', $pass);
		$q = "SELECT * FROM users WHERE user='$user' and password='$pass'";

		// This did not exist during competition.
		file_put_contents("log.txt",$q."\n",FILE_APPEND);
		//echo $q." <br />\n";
		$link = mysql_connect('127.0.0.1', 'web07', '123123') or die('Could not connect :(, ' . mysql_error());
		mysql_select_db("web07") or die("Could not select database :(\n");

		// for next time: @mysql_query to suppress errors
		$result = mysql_query($q);
		if($result === false){
			echo "Error!<br />";
		}
		if($result !== false && mysql_num_rows($result)>0){
			echo "Yes! logged in, here's the token: <pre>$token</pre>\n";
		} else {
			echo "Wrong user or password :(\n";
		}
	}
?>
</body>
</html>
