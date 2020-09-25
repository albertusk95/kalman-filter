import argparse

from kalman_filter import static_state, dynamic_state


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--state', help='static or dynamic')
	parser.add_argument('--true_value', help='single or multiple')
	
	args = parser.parse_args()
	state = args.state
	true_value = args.true_value

	if state == "static":
		static_state.run(true_value)
	elif state == "dynamic":
		dynamic_state.run(true_value)
