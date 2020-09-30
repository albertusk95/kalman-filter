# Kalman Filter

## What is it?

An iterative mathematical process applied on consecutive data inputs to quickly estimate the true value (position, velocity, weight, temperature, etc) of the object being measured, when the measured values contain random error or uncertainty.

## Currently available modules:

- Static state => the true value of the object being measured is constant
   - Estimates a single true value
- Dynamic state => the true value of the object being measured is governed by a certain equation
   - Estimates multiple true values

## How it works

### STATIC STATE

#### A) Single true value

<i>Assumption</i>: measurement error is constant

Inputs:
- Initial estimate
- Initial estimate error
- Measurement error (assumed to be constant over time)

There are three main calculations:
- Kalman gain: `previous_estimate_error / (previous_estimate_error + measurement_error)`
- Current estimate: `previous_estimate + (kalman_gain * (measurement - previous_estimate))`
- Current estimate error: `(1 - kalman_gain) * previous_estimate_error`

<i>Examples</i>

Suppose that we'd like to measure a temperature. Here are some basic information:
- The true temperature: `72`
- Initial estimate: `68`
- Initial estimate error: `2`
- Initial measurement: `75`
- Measurement error: `4`

The measured temperature values are `75`, `71`, `70`, and `74`.

We'd like to estimate the true temperature value based on the above data.

Performing Kalman filter calculation will yield the following results.

<table>
  <tr>
    <th>Time</th>
    <th>Measurement</th>
    <th>Measurement Error</th>
    <th>Estimate</th>
    <th>Estimate Error</th>
    <th>Kalman Gain</th>
  </tr>
  <tr>
    <td>t-1</td>
    <td>-</td>
    <td>-</td>
    <td>68</td>
    <td>2</td>
    <td>-</td>
  </tr>
  <tr>
    <td>t</td>
    <td>75</td>
    <td>4</td>
    <td>70.33</td>
    <td>1.33</td>
    <td>0.33</td>
  </tr>
  <tr>
    <td>t+1</td>
    <td>71</td>
    <td>4</td>
    <td>70.5</td>
    <td>1</td>
    <td>0.25</td>
  </tr>
  <tr>
    <td>t+2</td>
    <td>70</td>
    <td>4</td>
    <td>70.4</td>
    <td>0.8</td>
    <td>0.2</td>
  </tr>
  <tr>
    <td>t+3</td>
    <td>74</td>
    <td>4</td>
    <td>71</td>
    <td>0.66</td>
    <td>0.17</td>
  </tr>
</table>

According to the given data, the true value estimate is `71`.

### DYNAMIC STATE

#### A) Multiple true values

Suppose we're going to estimate the true value of position & velocity of a moving object in a single direction (x-axis).

Here are the general steps in applying Kalman filter. Note that variables with all capital letters denote matrix (ex: `VAR_NAME` refers to a matrix called `VAR_NAME`)

- Fill in all the required input values in <a href="https://github.com/albertusk95/kalman-filter/blob/master/kalman_filter/constants/dynamic_state_constants.py">DynamicStateMultipleTrueValues1D</a>

- Taking the initial estimate of position & velocity as the `PREVIOUS_STATE` and the initial estimate covariance matrix as the `PREVIOUS_STATE_COVARIANCE_MATRIX`, calculate the predicted state by the following.

```
PREDICTED_STATE_ESTIMATE = STATE_MULTIPLIER * PREVIOUS_STATE 
                              + CONTROL_VARIABLE_MULTIPLIER * CONTROL_VARIABLE \
                              + STATE_PREDICTION_PROCESS_ERROR
                              
PREDICTED_STATE_COVARIANCE_MATRIX = STATE_MULTIPLIER * PREVIOUS_STATE_COVARIANCE_MATRIX * STATE_MULTIPLIER_transposed \
                                    + PREDICTED_STATE_COVARIANCE_MATRIX_PROCESS_ERROR
```

- Calculate the Kalman gain

```
OBSERVATION_ERRORS_COVARIANCE = [[(OBSERVATION_ERROR_POSITION)^2, 0.0] 
                                 [0.0, (OBSERVATION_ERROR_VELOCITY)^2)]]

TRANSFORMER_H = np.array([[1.0, 0.0], [0.0, 1.0]])

KALMAN_GAIN = (PREDICTED_STATE_COVARIANCE_MATRIX * TRANSFORMER_H_TRANSPOSED) \
               / ((TRANSFORMER_H * PREDICTED_STATE_COVARIANCE_MATRIX)) * TRANSFORMER_H_TRANSPOSED) \
               + OBSERVATION_ERRORS_COVARIANCE)
```

- Calculate observations where non-observation errors are included

```
TRANSFORMER_C = [[1.0, 0.0]
                 [0.0, 1.0]]

OBSERVATION_WITH_NON_OBS_ERRORS = (TRANSFORMER_C * OBSERVATION) + NEW_OBSERVATION_PROCESS_ERROR
```

- Calculate current state estimate

```
TRANSFORMER_H = [[1.0, 0.0]
                 [0.0, 1.0]]
                 
OBSERVATION_AND_PREDICTED_STATE_ESTIMATE_DIFF = OBSERVATION_WITH_NON_OBS_ERRORS - (TRANSFORMER_H * PREDICTED_STATE_ESTIMATE)

CURRENT_STATE_ESTIMATE = PREDICTED_STATE_ESTIMATE + (KALMAN_GAIN * OBSERVATION_AND_PREDICTED_STATE_ESTIMATE_DIFF)
```

- Calculate current state estimate error

```
TRANSFORMER_H = [[1.0, 0.0]
                 [0.0, 1.0]]

I = [[1.0, 0.0]
     [0.0, 1.0]]

CURRENT_STATE_ESTIMATE_COVARIANCE_MATRIX = (I - (KALMAN_GAIN * TRANSFORMER_H)) * PREDICTED_STATE_COVARIANCE_MATRIX
```

- Current state estimate & current state estimate covariance matrix becomes the previous state for the next iteration. The next iteration follows the same steps as above.
