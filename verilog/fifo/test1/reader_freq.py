def solid(): 
	while True:
		yield 1

def on_off():
	a=0
	while True:
		yield a&1
		a+=1
