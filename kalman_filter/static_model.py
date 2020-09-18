def calculate_kalman_gain(error_estimate: float, error_measurement: float):
	return error_estimate / (error_estimate + error_measurement)

def calculate_estimate(estimate: float, kalman_gain: float, measurement: float):

def calculate_error_estimate(kalman_gain: float, error_estimate: float):

def readFromFile(path):
	with open(path, "r") as f:
		measurements = f.readlines()
	
	return [float(x.strip()) for x in measurements]

def run(true_value: str):
	if true_value == "single":
		true_value = input("true value: ")
		estimate = input("initial estimate: ")
		error_estimate = input("initial error estimate: ")
		measurement = input("initial measurement: ")
		error_measurement = input("error measurement: ")
		
		measurements = readFromFile("resources/example_measurements.txt")
		for measurement in measurements:
			kalman_gain = calculate_kalman_gain(error_estimate, error_measurement)
			estimate = calculate_estimate(estimate, kalman_gain, measurement)
			error_estimate = calculate_error_estimate(kalman_gain, error_estimate)




# KG = error_est / (error_est + error_meas)
# est(t) = est(t-1) + KG[mea - est(t-1)]
# error(est(t)) = [1-KG] (error(est(t-1)))