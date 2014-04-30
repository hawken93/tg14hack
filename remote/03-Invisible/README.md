Invisible
=========

Goal
----
* Attacker uses the heartbleed exploit to get a token out of the server
* The ticket contains a tab, so there will be a little bump in getting it into the web interface

Description
-----------
[Find the token!](https://10.75.2.2/)

How to make
-----------
* Linux box
* Our patch

How to exploit
---------------
* get hb-test.py (https://gist.github.com/takeshixx/10107280) (attached as well)
* point it at the server, and look for plaintext
