import math
import numpy as np

from kalman_filter.constants.dynamic_state_constants import DynamicStateMultipleTrueValues1D


def calculate_initial_process_covariance():
	cov = DynamicStateMultipleTrueValues1D.ESTIMATE_ERROR_POSITION * DynamicStateMultipleTrueValues1D.ESTIMATE_ERROR_VELOCITY

	# replace cov with 0
	return np.array([
		[math.pow(DynamicStateMultipleTrueValues1D.ESTIMATE_ERROR_POSITION, 2), 0.0], 
		[0.0, math.pow(DynamicStateMultipleTrueValues1D.ESTIMATE_ERROR_VELOCITY, 2)]
	])


def calculate_predicted_process_covariance(previous_process_covariance):
	predicted_process_cov = (
		DynamicStateMultipleTrueValues1D.STATE_MULTIPLIER_MATRIX.dot(previous_process_covariance)
	).dot(DynamicStateMultipleTrueValues1D.STATE_MULTIPLIER_MATRIX.transpose()) \
	+ DynamicStateMultipleTrueValues1D.PREDICTED_ESTIMATE_PROCESS_ERROR_MATRIX

	np.fill_diagonal(np.fliplr(predicted_process_cov),[0.0, 0.0])
	return predicted_process_cov

def calculate_kalman_gain(predicted_process_covariance):
	observation_errors_covariance = np.array([[math.pow(DynamicStateMultipleTrueValues1D.OBSERVATION_ERROR_POSITION, 2), 0.0], 
												[0.0, math.pow(DynamicStateMultipleTrueValues1D.OBSERVATION_ERROR_VELOCITY, 2)]])

	transformer_matrix_H = np.array([[1.0, 0.0], [0.0, 1.0]])

	kalman_gain = predicted_process_covariance.dot(transformer_matrix_H.transpose()) \
	/ ((transformer_matrix_H.dot(predicted_process_covariance)).dot(transformer_matrix_H.transpose()) \
		+ observation_errors_covariance)

	kalman_gain_nans = np.isnan(kalman_gain)
	kalman_gain[kalman_gain_nans] = 0.0
	return kalman_gain


def calculate_observation_with_non_obs_errors(observation):
	transformer_matrix_C = np.array([[1.0, 0.0], [0.0, 1.0]])
	return transformer_matrix_C.dot(observation) + DynamicStateMultipleTrueValues1D.NEW_OBSERVATION_PROCESS_ERROR_MATRIX


def calculate_current_state_estimate(predicted_state_estimate, kalman_gain, observation_with_non_obs_errors):
	transformer_matrix_H = np.array([[1.0, 0.0], [0.0, 1.0]])
	observation_and_predicted_state_estimate_diff = observation_with_non_obs_errors - transformer_matrix_H.dot(predicted_state_estimate)
	return predicted_state_estimate + kalman_gain.dot(observation_and_predicted_state_estimate_diff)


def calculate_predicted_state(previous_state):
	return DynamicStateMultipleTrueValues1D.STATE_MULTIPLIER_MATRIX.dot(previous_state) \
	+ DynamicStateMultipleTrueValues1D.CONTROL_VARIABLE_MULTIPLIER_MATRIX.dot(DynamicStateMultipleTrueValues1D.CONTROL_VARIABLE_MATRIX) \
	+ DynamicStateMultipleTrueValues1D.STATE_PREDICTION_PROCESS_ERROR_MATRIX


def calculate_current_process_covariance(predicted_process_covariance, kalman_gain):
	transformer_matrix_H = np.array([[1.0, 0.0], [0.0, 1.0]])
	I = np.array([[1.0, 0.0], [0.0, 1.0]])
	return (I - kalman_gain.dot(transformer_matrix_H)).dot(predicted_process_covariance)


def estimate_multiple_true_value_1d():
	measurements = readFromFile(DynamicStateMultipleTrueValues1D.MEASUREMENT_DATA_FILE)

	previous_process_covariance = calculate_initial_process_covariance()
	previous_state = np.array([[DynamicStateMultipleTrueValues1D.INITIAL_ESTIMATE_POSITION], 
								[DynamicStateMultipleTrueValues1D.INITIAL_ESTIMATE_VELOCITY]])

	for measurement in measurements:
		# predicted state estimate
		predicted_state_estimate = calculate_predicted_state(previous_state)

		# predicted process covariance
		predicted_process_covariance = calculate_predicted_process_covariance(previous_process_covariance)

		# kalman gain
		kalman_gain = calculate_kalman_gain(predicted_process_covariance)
		
		# new observation
		position, velocity = measurement.split(",")
		position, velocity = float(position), float(velocity)

		observation_with_non_obs_errors = calculate_observation_with_non_obs_errors(np.array([[position], [velocity]]))

		# current state estimate
		current_state_estimate = calculate_current_state_estimate(predicted_state_estimate, kalman_gain, observation_with_non_obs_errors)
		
		# updated process covariance
		current_process_covariance = calculate_current_process_covariance(predicted_process_covariance, kalman_gain)
		
		# current becomes previous for the next iteration
		previous_state = current_state_estimate
		previous_process_covariance = current_process_covariance

		print("Current state estimate")
		print(current_state_estimate)
		print("======================")
		

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