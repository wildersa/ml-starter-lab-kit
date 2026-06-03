# Bad Split

A bad split makes evaluation unreliable.

## Common cases

- random split for time series;
- same user appears in train and test when user separation matters;
- preprocessing learns from all data before splitting;
- duplicates appear in train and test.

## Practical rule

Split in a way that simulates the real prediction scenario.
