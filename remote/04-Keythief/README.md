Keythief
=========

Goal
----
* Attacker uses the heartbleed exploit to get a token out of the server
* More specifically, the server fills the buffer with noise, adds a fragment of the key, and returns it
* You have to do a lot of complex stuff to get the key (More on this later)

Description
-----------
[Find the token!](https://10.75.1.12/)

How to make
-----------
* Linux box
* Our patch (TODO: Make it!)
* An encrypted message (TODO: Exact commands to do this)

How to exploit
---------------
* PROTIP: don't run stage1 unless you have a server set up to test against :) hb-progress.bin has been provided to give you the needed information to start from pt. 2

* get hb-test.py (https://gist.github.com/takeshixx/10107280) as a starting point, then modify it to hell...
* Here's a script and a walkthrough: hb-search.py
 * 1: Run stage1() and stage1\_results(). Be patient.
 * 2: Comment stage1(). Grab some bytes from stage1\_results and put them in as a needle.  Run it and see what you get
 * 3: Comment stage1\_results(). Where most heartbeats seem to agree, you can extend your string, change needle to search a bit more to the left and so on. Do this until you are all the way to the left, then go all the way to the right.
 * 4: Remove two 0 bytes at start and end, and put it into the messages-string. Then let the script write it to privkey.bin.
* 5:
 * echo "-----BEGIN PRIVATE KEY-----" > privkey.key
 * base64 privkey.bin >> privkey.key
 * echo "-----END PRIVATE KEY-----" >> privkey.key
* 6: base64 -d challenge.txt > challenge.bin
* 7: openssl rsautl -decrypt -inkey privkey.key  < ./challenge.bin; echo
