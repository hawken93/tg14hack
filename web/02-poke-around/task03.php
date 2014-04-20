<!doctype html>
<html>
<head></head>
<body>
<form action="" method="post">
	<table>
		<tr><td>Password</td><td><input type="text" name="pass" /></tr>
		<tr><td colspan="2"><input type="submit" /></td></tr>
	</table>
</form>
<?php
	if(isset($_POST['pass'])){
		$pass = $_POST['pass'];		
		if($pass == "Remember-to-drink-water"){
			$token = "Fb5Xb9CXLr";
			echo "That's right, here's your reward: $token\n";
		}
	}
?>
</body>
</html>
