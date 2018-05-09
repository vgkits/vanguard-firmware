from deployall import run

count = 0

while True:
	print("Flashing board " + str(count))
	run()
	count += 1
