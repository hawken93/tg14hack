<!doctype html>
<html>
<head></head>
<body>
<?php
if(!isset($_SERVER['HTTP_USER_AGENT'])) $ua = "";
else $ua = $_SERVER['HTTP_USER_AGENT'];

if(strstr($ua, "Googlebot")!==false){
	echo "Hi Google, your token is RChUSbEpTJ\n";
} else {
	echo "Only bots allowed! :p\n";
}
?>
</body>
</html>
