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
	return [str_key, str_cipher]


mystr = ["Enter the secret password: ",
	"'%s'\n",
	"Yay, your token is: %s\n",
	"Wrong password!\n",
	"WHUJYEWf-i-can-haz-token",
	"That was easy!"]



arr = encode(mystr)

[str_cipher,str_key]=gen_xor(arr[0])

f = open("strings.c", 'w')
f.write("unsigned char str[] = "+c_arr(str_cipher)+";\n")
f.write("unsigned char str_key[] = "+c_arr(str_key)+";\n")
f.write("int str_len = "+str(arr[1])+";\n")
f.write("int str_count = "+str(arr[2])+";\n")
f.close()
#print "Encrypted strings in strings.c"
