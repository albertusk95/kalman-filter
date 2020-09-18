def calculate_kalman_gain(previous_estimate_error: float, measurement_error: float):
	# KG = error_est / (error_est + error_meas)
	return previous_estimate_error / (previous_estimate_error + measurement_error)

def calculate_estimate(previous_estimate: float, kalman_gain: float, measurement: float):
	# est(t) = previous_estimate + KG[mea - previous_estimate]
	return previous_estimate + (kalman_gain * (measurement - previous_estimate))

def calculate_error_estimate(kalman_gain: float, previous_estimate_error: float):
	# error(est(t)) = [1 - KG] * previous_estimate_error
	return (1 - kalman_gain) * previous_estimate_error

def readFromFile(path):
	with open(path, "r") as f:
		measurements = f.readlines()
	
	return [float(x.strip()) for x in measurements]

def run(true_value: str):
	if true_value == "single":
		# assumption: error measurement is constant
		true_value = input("true value: ")
		initial_estimate = input("initial estimate: ")
		initial_estimate_error = input("initial estimate error: ")
		initial_measurement = input("initial measurement: ")
		measurement_error = input("measurement error: ")
		
		previous_estimate = initial_estimate
		previous_estimate_error = initial_estimate_error

		measurements = readFromFile("resources/example_measurements.txt")
		for measurement in measurements:
			kalman_gain = calculate_kalman_gain(previous_estimate_error, measurement_error)
			estimate = calculate_estimate(previous_estimate, kalman_gain, measurement)
			estimate_error = calculate_error_estimate(kalman_gain, previous_estimate_error)

			print("kalman gain %f".format(kalman_gain))
			print("estimate %f".format(estimate))
			print("estimate error %f".format(estimate_error))
			
			previous_estimate = estimate
			previous_estimate_error = estimate_error
