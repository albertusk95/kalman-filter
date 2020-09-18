import argparse

from kalman_filter import static_model


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--process', help='static or dynamic')
	parser.add_argument('--true_value', help='single or multiple')
	
	args = parser.parse_args()
	process = args.process

	if process == "static":
		true_value = args.true_value
		static_model.run(true_value)
