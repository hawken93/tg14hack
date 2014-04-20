<?php

if (!isset($_COOKIE['a']) || $_COOKIE['a'] != '1' || !isset($_COOKIE['user']) || $_COOKIE['user'] != 'admin')
{
	die("Restricted, only for admin with admin rights");
}

echo 'mysecretisyours';
