def estimate_multiple_true_value_1d(initial_acceleration, time_diff, process_errors, observation_errors):
	

def readFromFile(path: str) -> [float]:
	with open(path, "r") as f:
		measurements = f.readlines()
	return [float(x.strip()) for x in measurements]

def run(true_value: str):
	if true_value == "multiple":
		# ex: measure position & velocity at once

		# the first row in the external file denotes the initial estimates
		dimensions = int(input("dimension: "))

		if dimensions == 1:
			# only in the x axis
			initial_acceleration = float(input("initial acceleration: "))
			time_diff = float(input("time difference: "))

			# process errors in process covariance matrix
			process_error_position = float(input("process error for position: "))
			process_error_velocity = float(input("process error for velocity: "))
			process_errors = [process_error_position, process_error_velocity]

			# observation errors
			observation_error_position = float(input("observation error for position: "))
			observation_error_velocity = float(input("observation error for velocity: "))
			observation_errors = [observation_error_position, observation_error_velocity]

			estimate_multiple_true_value_1d(initial_acceleration, time_diff, process_errors, observation_errors)