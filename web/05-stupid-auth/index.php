<?php

$path = "/";

if (!isset($_COOKIE['a']))
{
	setcookie("user", "thegathering", 0, $path);
	setcookie("a", "0", 0, $path);
}

?>
<!DOCTYPE html>
<html>
<title>TG14</title>
</head>
<body>
<h1>Token-storage</h1>
<p><a href="gettoken.php">Fetch token (only for admin user) &raquo;</a></p>
</body>
</html>
