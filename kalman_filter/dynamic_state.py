import math
import numpy as np

from kalman_filter.constants.dynamic_state import DynamicStateMultipleTrueValues1D

def calculate_initial_process_covariance():
	cov = DynamicStateMultipleTrueValues1D.PROCESS_ERROR_POSITION * DynamicStateMultipleTrueValues1D.PROCESS_ERROR_VELOCITY

	return np.array([
		[math.pow(DynamicStateMultipleTrueValues1D.PROCESS_ERROR_POSITION, 2), cov], 
		[cov, math.pow(DynamicStateMultipleTrueValues1D.PROCESS_ERROR_VELOCITY, 2)]
	])


def calculate_predicted_state(previous_state):
	return DynamicStateMultipleTrueValues1D.STATE_MATRIX_MULTIPLIER.dot(previous_state) \
	+ DynamicStateMultipleTrueValues1D.CONTROL_VARIABLE_MATRIX_MULTIPLIER.dot(DynamicStateMultipleTrueValues1D.CONTROL_VARIABLE_MATRIX) \
	+ DynamicStateMultipleTrueValues1D.STATE_PREDICTION_ERROR_MATRIX


def estimate_multiple_true_value_1d():
	measurements = readFromFile(DynamicStateMultipleTrueValues1D.MEASUREMENT_DATA_FILE)

	initial_process_covariance = calculate_initial_process_covariance()

 	for measurement in measurements:
		position, velocity = measurement.split(",")
		position, velocity = float(position), float(velocity)

		# create the numpy array
		previous_state = np.array([[position], [velocity]])

		# calculate predicted state
		predicted_state = calculate_predicted_state(previous_state)



def readFromFile(path: str) -> [float]:
	with open(path, "r") as f:
		measurements = f.readlines()
	return [x.strip() for x in measurements]

def run(true_value: str):
	if true_value == "multiple":
		# ex: measure position & velocity at once
		dimensions = int(input("dimension: "))

		if dimensions == 1:
			# only in one axis
			estimate_multiple_true_value_1d()