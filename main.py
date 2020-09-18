def readFromFile(path):
	with open(path, "r") as f:
		measurements = f.readlines()
	
	return [float(x.strip()) for x in measurements] 

if __name__ == "main":
	measurements = readFromFile("resources/example.txt")
	
