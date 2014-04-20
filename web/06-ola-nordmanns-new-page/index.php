<?php

$allowed_path = realpath(dirname(__FILE__));

// PHP null byte poisoning cured in 5.3.3, but sapi (Suhosin) filters _GET and _POST instead. 5.3.4 fixed, and now we can emulate the error

// 1: Get page
if(!isset($_GET['page'])){
	header("Location: index.php?page=fruit");
	$_GET['page'] = "fruit.php";
}

// A bit html to go with that
?><!doctype html>
<html>
<head>
<title>SuperSikker Nettside A/S</title>
</head>
<body>
<h1>Ola Nordmann sin ultra-sikre nettside</h1>
<pre>
<?php

// 2: Filename
$file = $allowed_path."/pages/{$_GET['page']}.php";

// 3: Make us as vulnerable as before 5.3.3!
if(strpos($file, "\x00") !== false){
	$file = substr($file,0,strpos($file,"\x00"));
}

// 4: Verify enough to not give away our server
if(substr(realpath($file),0,strlen($allowed_path)) != $allowed_path && file_exists($file)){
	echo "Sorry, can't let you do that!\n";
} else {
	// 5: inject
	// This is pretty dangerous
	// BTW, *_once stopped us from recursing into ourselves
	ini_set("display_errors","Off");
	include_once $file;
}

?>
</pre>
</body>
</html>
