SSH-Trouble
============

Goal
-----
User makes his way into the box by the DSA-1571-1.

Description
------------
John Ifi has used the same key ever since 2007. Here's his IP and username: ifi@10.75.13.37

How to make
------------
* The user has a bad key or two in authorized\_keys, and the attacker tries the list of bad keys
* PS: The box has to have the blacklist of keys deleted, so that the keys won't be rejected
* A textfile is placed within users home directory with a token

How to exploit
---------------
* The attacker can for example use this script: http://www.exploit-db.com/exploits/5720/

