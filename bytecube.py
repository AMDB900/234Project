size = 3
byte_cube = bytearray(range(size * size * size))
print(byte_cube)
#print(len(byte_cube))
#for n in range(len(byte_cube)):
#	print(byte_cube[n])

x = 0
y = 0
print([(byte_cube[x + y * size + z * size * size]) for z in range(size)])

y = 0
z = 0
print([(byte_cube[x + y * size + z * size * size]) for x in range(size)])


y=2
z=2
temparray = [(byte_cube[x + y * size + z * size * size]) for x in range(size)]
shift = -1
print([(byte_cube[x + y * size + z * size * size]) for x in range(size)])

for n in range(size):
	byte_cube[(n+shift)%size + y * size + z * size * size] = temparray[n]

print(byte_cube)
print([(byte_cube[x + y * size + z * size * size]) for x in range(size)])


	
