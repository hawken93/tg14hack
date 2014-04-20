from random import randrange


def decode(instr,length,elements):
	mystr=[]
	for i in range(0,elements):
		mystr.append("")

	for i in range(0,length/elements):
		for j in range(0,elements):
			mystr[j] = mystr[j]+instr[(i*elements)+j]
	return mystr

def encode(mystr):
	outstr=""
	elements=len(mystr)
	length=len(max(mystr,key=len))

	for i in range(0,length):
		for j in range(0,elements):
			k = mystr[j]
			if len(k) <= i:
				outstr = outstr+'\0'
			else:
				outstr = outstr+k[i]
	length = length*elements
	return [outstr, length, elements]

def c_arr(mystr):
	array=[]
	for i in range(0, len(mystr)):
		c=mystr[i]
		h="{:02x}".format(ord(c))
		h="0x"+h
		array.append(h)
	return "{"+", ".join(array)+"}"

def gen_xor(str_clear):
	str_cipher=""
	str_key=""
	for i in range(0, len(str_clear)):
		str_key = str_key+chr(randrange(0,256))
		str_cipher = str_cipher+chr(ord(str_clear[i])^ord(str_key[i]))
	str_key = str_key+chr(0)
	str_cipher = str_cipher+chr(0)
	return [str_key, str_cipher]


mystr_token = "y5JQmV7saA"
mystr_pass = "AAARNEEEEEEEEEEEEEEE"

[token,token_key]=gen_xor(mystr_token)
[pass_,pass_key]=gen_xor(mystr_pass)

f = open("strings.c", 'w')
f.write("unsigned char token[] = "+c_arr(token)+";\n")
f.write("unsigned char token_key[] = "+c_arr(token_key)+";\n")
f.write("int token_len = "+str(len(mystr_token))+";\n")
f.write("unsigned char pass[] = "+c_arr(pass_)+";\n")
f.write("unsigned char pass_key[] = "+c_arr(pass_key)+";\n")
f.write("int pass_len = "+str(len(mystr_pass))+";\n")
f.close()
#print "Encrypted strings in strings.c"
