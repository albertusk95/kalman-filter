def calculate_kalman_gain(previous_estimate_error: float, measurement_error: float) -> float:
	# KG = error_est / (error_est + error_meas)
	return previous_estimate_error / (previous_estimate_error + measurement_error)

def calculate_estimate(previous_estimate: float, kalman_gain: float, measurement: float) -> float:
	# est(t) = previous_estimate + KG[mea - previous_estimate]
	return previous_estimate + (kalman_gain * (measurement - previous_estimate))

def calculate_error_estimate(kalman_gain: float, previous_estimate_error: float) -> float:
	# error(est(t)) = [1 - KG] * previous_estimate_error
	return (1 - kalman_gain) * previous_estimate_error

def readFromFile(path: str) -> [float]:
	with open(path, "r") as f:
		measurements = f.readlines()
	return [float(x.strip()) for x in measurements]

def estimate_single_true_value(
	previous_estimate: float, 
	previous_estimate_error: float, 
	measurement_error: float):
	measurements = readFromFile("resources/example_measurements.txt")
	for measurement in measurements:
		kalman_gain = calculate_kalman_gain(previous_estimate_error, measurement_error)
		estimate = calculate_estimate(previous_estimate, kalman_gain, measurement)
		estimate_error = calculate_error_estimate(kalman_gain, previous_estimate_error)

		print("kalman gain %f" % kalman_gain)
		print("estimate %f" % estimate)
		print("estimate error %f" % estimate_error)
		print("====================================")
		
		previous_estimate = estimate
		previous_estimate_error = estimate_error

def run(true_value: str):
	if true_value == "single":
		# assumption: error measurement is constant
		initial_estimate = float(input("initial estimate: "))
		initial_estimate_error = float(input("initial estimate error: "))
		measurement_error = float(input("measurement error: "))
		
		previous_estimate = initial_estimate
		previous_estimate_error = initial_estimate_error

		estimate_single_true_value(previous_estimate, previous_estimate_error, measurement_error)
