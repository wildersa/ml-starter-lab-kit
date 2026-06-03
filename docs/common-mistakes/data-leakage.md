# Data Leakage

Data leakage happens when the model uses information that would not be available at prediction time.

## Example

Using `campaign_duration` to predict whether a user converted during the campaign, when duration is only known after the contact.

## Why it is dangerous

It creates scores that look great during training but fail in real use.

## Quick check

Ask:

```text
Would I know this value before making the prediction?
```

If not, remove or quarantine the feature.
