import math
import numpy as np

from kalman_filter.constants.dynamic_state import DynamicStateMultipleTrueValues1D

def calculate_initial_process_covariance():
	cov = DynamicStateMultipleTrueValues1D.ESTIMATE_ERROR_POSITION * DynamicStateMultipleTrueValues1D.ESTIMATE_ERROR_VELOCITY

	# replace cov with 0
	return np.array([
		[math.pow(DynamicStateMultipleTrueValues1D.ESTIMATE_ERROR_POSITION, 2), 0.0], 
		[0.0, math.pow(DynamicStateMultipleTrueValues1D.ESTIMATE_ERROR_VELOCITY, 2)]
	])


def calculate_predicted_process_covariance(previous_process_covariance):
	return (
		DynamicStateMultipleTrueValues1D.STATE_MULTIPLIER_MATRIX.dot(previous_process_covariance)
	).dot(DynamicStateMultipleTrueValues1D.STATE_MULTIPLIER_MATRIX.transpose()) \
	+ DynamicStateMultipleTrueValues1D.PREDICTED_ESTIMATE_ERROR_MATRIX


def calculate_kalman_gain(predicted_process_covariance):
	observation_errors_covariance = np.array([[DynamicStateMultipleTrueValues1D.OBSERVATION_ERROR_POSITION, 0], 
												[0, DynamicStateMultipleTrueValues1D.OBSERVATION_ERROR_VELOCITY]])

	transformer_matrix_H = np.array([[1.0, 0.0], [0.0, 1.0]])

	where_are_NaNs = isnan(a)
	a[where_are_NaNs] = 0

	kalman_gain = predicted_process_covariance.dot(transformer_matrix_H.transpose()) \
	/ ((transformer_matrix_H.dot(predicted_process_covariance)).dot(transformer_matrix_H.transpose()) \
		+ observation_errors_covariance)

	kalman_gain[np.isnan(kalman_gain)] = 0.0
	return kalman_gain

def calculate_predicted_state(previous_state):
	return DynamicStateMultipleTrueValues1D.STATE_MULTIPLIER_MATRIX.dot(previous_state) \
	+ DynamicStateMultipleTrueValues1D.CONTROL_VARIABLE_MULTIPLIER_MATRIX.dot(DynamicStateMultipleTrueValues1D.CONTROL_VARIABLE_MATRIX) \
	+ DynamicStateMultipleTrueValues1D.STATE_PREDICTION_ERROR_MATRIX


def estimate_multiple_true_value_1d():
	measurements = readFromFile(DynamicStateMultipleTrueValues1D.MEASUREMENT_DATA_FILE)

	previous_process_covariance = calculate_initial_process_covariance()

	for measurement in measurements:
		position, velocity = measurement.split(",")
		position, velocity = float(position), float(velocity)

		# create the numpy array
		previous_state = np.array([[position], [velocity]])

		# calculate predicted state
		predicted_state = calculate_predicted_state(previous_state)

		# predicted process covariance
		predicted_process_covariance = calculate_predicted_process_covariance(previous_process_covariance)

		# kalman gain
		kalman_gain = calculate_kalman_gain(predicted_process_covariance)


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