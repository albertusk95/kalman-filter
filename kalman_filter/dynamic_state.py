import numpy as np

from constants.dynamic_state import DynamicStateMultipleTrueValues1D

def calculate_predicted_state(previous_state):



def estimate_multiple_true_value_1d():
	measurements = readFromFile('../resources/example_dynamic_state_1d')

	for measurement in measurements:
		position, velocity = measurement.split(",")
		position, velocity = float(position), float(velocity)

		# create the numpy array
		previous_state = np.array([[position, velocity]])

		# calculate predicted state
		predicted_state = calculate_predicted_state(previous_state)


def readFromFile(path: str) -> [float]:
	with open(path, "r") as f:
		measurements = f.readlines()
	return [float(x.strip()) for x in measurements]

def run(true_value: str):
	if true_value == "multiple":
		# ex: measure position & velocity at once
		dimensions = int(input("dimension: "))

		if dimensions == 1:
			# only in one axis
			estimate_multiple_true_value_1d()