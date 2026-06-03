# Time Series and LSTM

Use time series methods when the order of events matters.

Examples:

- forecast sales;
- predict demand;
- estimate future traffic;
- detect temporal patterns.

## Important rule

Do not use random split by default.

For time series, train on the past and test on the future.

```text
past data -> train
future data -> test
```

## Common features

- lag values;
- rolling mean;
- rolling standard deviation;
- day of week;
- month;
- holidays/events;
- trend indicators.

## LSTM in one sentence

LSTM is a neural network architecture designed to learn patterns from sequences.

## When LSTM may make sense

- You have enough temporal data.
- Sequence patterns are important.
- Simpler baselines are not enough.

## Start simpler first

Before LSTM, try:

- last value baseline;
- moving average;
- linear regression with lags;
- tree model with lag features.

## Common mistakes

- Random split.
- Leakage through rolling features.
- Not comparing against a simple baseline.
- Using LSTM with too little data.
