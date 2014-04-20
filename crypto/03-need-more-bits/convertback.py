
num = 281441281418489127035953670741060713

mystr = ""
for i in range(0,15):
	n = num%256
	num = num/256
	mystr = chr(n)+mystr
print "'"+mystr+"'"
