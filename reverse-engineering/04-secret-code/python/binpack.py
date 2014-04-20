from random import randrange

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

f = open("stage1.bin",'rb')
data = f.read()

#print "Blob length: "+str(len(data))
[data_cipher,data_key]=gen_xor(data)

f = open("blob.c", 'w')
f.write("unsigned char blob[] = "+c_arr(data_cipher)+";\n")
f.write("unsigned char blob_key[] = "+c_arr(data_key)+";\n")
f.write("unsigned int blob_len = "+str(len(data))+";\n")
f.close()
#print "Encrypted blob in blob.c"
