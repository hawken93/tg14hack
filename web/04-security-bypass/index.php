<!doctype html>
<html>
<head></head>
<body>
<form action="" method="post">
	<table>
		<tr>
			<td>User (Who needs passwords anyway?!)</td><td><input type="text" name="user" /></td>
		</tr>
		<tr>
			<td colspan="2"><input type="submit" /></td>
		</tr>
	</table>
</form>
<?php
/* mysql> CREATE TABLE users (
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        user VARCHAR(50),
        password VARCHAR(50)
        );
	grant SELECT on users.* TO web02@localhost IDENTIFIED BY '123123'
	insert into users (user,password) VALUES ("AwesomeUser7331!", "god");
*/
	$token = "07820116211337";
	if(isset($_POST['user'])){
		$user = $_POST['user'];
		$q = "SELECT * FROM users WHERE user='$user'";
		$link = mysql_connect('127.0.0.1', 'web02', '123123') or die('Could not connect :(, ' . mysql_error());
		mysql_select_db("web02") or die("Could not select database :(\n");

		$result = mysql_query($q);
		if($result === false){
			echo mysql_error()."<br />";
		}
		if($result !== false && mysql_num_rows($result)>0){
			echo "Yes! logged in, here's the token: $token\n";
		} else {
			echo "Wrong user or password :(\n";
		}
	}
?>
</body>
</html>
