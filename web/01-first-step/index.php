<!doctype html>
<html>
<head></head>
<body>
<?php
	if(isset($_POST['pass']) && $_POST['pass'] == "123abc"){
		?>
<p>Here is your token, manager: 321apes</p>
<?php
	} else {
		// false or unset
?>
<form action="" method="POST">
	<table>
		<!-- Our manager can't remember his password, so he asked us to put it here: 123abc -->
		<tr>	<td>Password</td>	<td><input type="password" name="pass"/></td>	</tr>
		<tr>	<td colspan="2"><input type="submit" /></td></tr>
	</table>
</form>
<?php
}
?></body>
</html>
