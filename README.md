# Kalman Filter

## What is it?

An iterative mathematical process applied on consecutive data inputs to quickly estimate the true value (position, velocity, weight, temperature, etc) of the object being measured, when the measured values contain random error or uncertainty.

## Currently available modules:

- Static state => the true value of the object being measured is constant
   - Estimates a single true value
- Dynamic state => the true value of the object being measured is governed by a certain equation
   - Estimates multiple true values

## How it works

### Static model

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
