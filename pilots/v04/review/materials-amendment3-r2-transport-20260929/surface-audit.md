# Surface-only material audit

Selectors were chosen on development histories and frozen before the disjoint review evaluation.
The selected six reviews are an additional fixed subset, not a model-selection set.

Development / review / selected history counts: 24 / 24 / 6.
Investigation required: **False**. Material approval remains pending.

The source oracle defines the target. Its apparent perfect agreement is not independent validation.
Balanced accuracy is undefined for one-class groups; they do not receive fabricated negative records.

## all_non_registration

| Development-selected family | Evaluation | TP / FP / TN / FN | Precision | Recall | Specificity | Pooled BA | History-macro BA | Defined / undefined groups |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| date_equality | development | 72 / 471 / 1 / 0 | 0.133 | 1.000 | 0.002 | 0.501 | 0.521 | 24 / 0 |
| date_equality | review | 72 / 472 / 0 / 0 | 0.132 | 1.000 | 0.000 | 0.500 | 0.500 | 24 / 0 |
| date_equality | selected_review | 18 / 118 / 0 / 0 | 0.132 | 1.000 | 0.000 | 0.500 | 0.500 | 6 / 0 |
| date_threshold | development | 49 / 353 / 119 / 23 | 0.122 | 0.681 | 0.252 | 0.466 | 0.577 | 24 / 0 |
| date_threshold | review | 53 / 384 / 88 / 19 | 0.121 | 0.736 | 0.186 | 0.461 | 0.573 | 24 / 0 |
| date_threshold | selected_review | 14 / 99 / 19 / 4 | 0.124 | 0.778 | 0.161 | 0.469 | 0.539 | 6 / 0 |
| day_threshold | development | 19 / 171 / 301 / 53 | 0.100 | 0.264 | 0.638 | 0.451 | 0.567 | 24 / 0 |
| day_threshold | review | 31 / 256 / 216 / 41 | 0.108 | 0.431 | 0.458 | 0.444 | 0.508 | 24 / 0 |
| day_threshold | selected_review | 6 / 41 / 77 / 12 | 0.128 | 0.333 | 0.653 | 0.493 | 0.484 | 6 / 0 |
| hour_threshold | development | 65 / 382 / 90 / 7 | 0.145 | 0.903 | 0.191 | 0.547 | 0.566 | 24 / 0 |
| hour_threshold | review | 64 / 400 / 72 / 8 | 0.138 | 0.889 | 0.153 | 0.521 | 0.562 | 24 / 0 |
| hour_threshold | selected_review | 18 / 106 / 12 / 0 | 0.145 | 1.000 | 0.102 | 0.551 | 0.720 | 6 / 0 |
| minute_threshold | development | 67 / 412 / 60 / 5 | 0.140 | 0.931 | 0.127 | 0.529 | 0.599 | 24 / 0 |
| minute_threshold | review | 64 / 413 / 59 / 8 | 0.134 | 0.889 | 0.125 | 0.507 | 0.497 | 24 / 0 |
| minute_threshold | selected_review | 17 / 106 / 12 / 1 | 0.138 | 0.944 | 0.102 | 0.523 | 0.490 | 6 / 0 |
| clock_quarter_hour_threshold | development | 63 / 374 / 98 / 9 | 0.144 | 0.875 | 0.208 | 0.541 | 0.576 | 24 / 0 |
| clock_quarter_hour_threshold | review | 62 / 387 / 85 / 10 | 0.138 | 0.861 | 0.180 | 0.521 | 0.563 | 24 / 0 |
| clock_quarter_hour_threshold | selected_review | 18 / 102 / 16 / 0 | 0.150 | 1.000 | 0.136 | 0.568 | 0.726 | 6 / 0 |
| comment_equality | development | 72 / 272 / 200 / 0 | 0.209 | 1.000 | 0.424 | 0.712 | 0.816 | 24 / 0 |
| comment_equality | review | 72 / 272 / 200 / 0 | 0.209 | 1.000 | 0.424 | 0.712 | 0.816 | 24 / 0 |
| comment_equality | selected_review | 18 / 68 / 50 / 0 | 0.209 | 1.000 | 0.424 | 0.712 | 0.816 | 6 / 0 |
| position_quartile | development | 43 / 229 / 243 / 29 | 0.158 | 0.597 | 0.515 | 0.556 | 0.591 | 24 / 0 |
| position_quartile | review | 32 / 235 / 237 / 40 | 0.120 | 0.444 | 0.502 | 0.473 | 0.452 | 24 / 0 |
| position_quartile | selected_review | 6 / 59 / 59 / 12 | 0.092 | 0.333 | 0.500 | 0.417 | 0.376 | 6 / 0 |
| constant | development | 0 / 0 / 472 / 72 | undefined | 0.000 | 1.000 | 0.500 | 0.500 | 24 / 0 |
| constant | review | 0 / 0 / 472 / 72 | undefined | 0.000 | 1.000 | 0.500 | 0.500 | 24 / 0 |
| constant | selected_review | 0 / 0 / 118 / 18 | undefined | 0.000 | 1.000 | 0.500 | 0.500 | 6 / 0 |

Source-convention reference on review groups (definitional, not validation): 72 / 0 / 472 / 0 TP/FP/TN/FN; history-macro BA 1.000; 0 one-class or empty groups remain undefined.

Frozen selectors (parameters come only from development):

```json
{
  "date_equality": {
    "family": "date_equality",
    "feature": "date",
    "operation": "eq",
    "value": "2026-05-09",
    "polarity": false
  },
  "date_threshold": {
    "family": "date_threshold",
    "feature": "date",
    "operation": "le",
    "value": "2026-05-29",
    "polarity": false
  },
  "day_threshold": {
    "family": "day_threshold",
    "feature": "day",
    "operation": "le",
    "value": 8,
    "polarity": true
  },
  "hour_threshold": {
    "family": "hour_threshold",
    "feature": "hour",
    "operation": "le",
    "value": 9,
    "polarity": false
  },
  "minute_threshold": {
    "family": "minute_threshold",
    "feature": "minute",
    "operation": "le",
    "value": 6,
    "polarity": false
  },
  "clock_quarter_hour_threshold": {
    "family": "clock_quarter_hour_threshold",
    "feature": "minute_of_day",
    "operation": "le",
    "value": 614,
    "polarity": false
  },
  "comment_equality": {
    "family": "comment_equality",
    "feature": "comment",
    "operation": "eq",
    "value": null,
    "polarity": false
  },
  "position_quartile": {
    "family": "position_quartile",
    "feature": "position_quartile",
    "operation": "le",
    "value": 1,
    "polarity": false
  },
  "constant": {
    "family": "constant",
    "operation": "constant",
    "value": false
  }
}
```

Overall development winner: `{"family": "comment_equality", "feature": "comment", "operation": "eq", "value": null, "polarity": false}`.

| Review surface | Distinct values | Cross-class shared values | Exact observed separation |
| --- | ---: | ---: | --- |
| date | 27 | 21 | False |
| day | 25 | 21 | False |
| hour | 10 | 10 | False |
| minute | 60 | 45 | False |
| minute_of_day | 350 | 45 | False |
| comment | 7 | 6 | False |
| position_quartile | 4 | 4 | False |
| exact_timestamp | 543 | 0 | True |
| joint_signature | 544 | 0 | True |

## current_accepted_reviews

| Development-selected family | Evaluation | TP / FP / TN / FN | Precision | Recall | Specificity | Pooled BA | History-macro BA | Defined / undefined groups |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| date_equality | development | 71 / 167 / 9 / 1 | 0.298 | 0.986 | 0.051 | 0.519 | 0.507 | 8 / 16 |
| date_equality | review | 67 / 153 / 23 / 5 | 0.305 | 0.931 | 0.131 | 0.531 | 0.505 | 8 / 16 |
| date_equality | selected_review | 17 / 44 / 0 / 1 | 0.279 | 0.944 | 0.000 | 0.472 | 0.500 | 2 / 4 |
| date_threshold | development | 34 / 75 / 101 / 38 | 0.312 | 0.472 | 0.574 | 0.523 | 0.511 | 8 / 16 |
| date_threshold | review | 26 / 77 / 99 / 46 | 0.252 | 0.361 | 0.562 | 0.462 | 0.505 | 8 / 16 |
| date_threshold | selected_review | 7 / 20 / 24 / 11 | 0.259 | 0.389 | 0.545 | 0.467 | 0.517 | 2 / 4 |
| day_threshold | development | 58 / 122 / 54 / 14 | 0.322 | 0.806 | 0.307 | 0.556 | 0.514 | 8 / 16 |
| day_threshold | review | 51 / 125 / 51 / 21 | 0.290 | 0.708 | 0.290 | 0.499 | 0.505 | 8 / 16 |
| day_threshold | selected_review | 14 / 36 / 8 / 4 | 0.280 | 0.778 | 0.182 | 0.480 | 0.517 | 2 / 4 |
| hour_threshold | development | 41 / 98 / 78 / 31 | 0.295 | 0.569 | 0.443 | 0.506 | 0.558 | 8 / 16 |
| hour_threshold | review | 31 / 86 / 90 / 41 | 0.265 | 0.431 | 0.511 | 0.471 | 0.505 | 8 / 16 |
| hour_threshold | selected_review | 11 / 18 / 26 / 7 | 0.379 | 0.611 | 0.591 | 0.601 | 0.550 | 2 / 4 |
| minute_threshold | development | 22 / 45 / 131 / 50 | 0.328 | 0.306 | 0.744 | 0.525 | 0.577 | 8 / 16 |
| minute_threshold | review | 18 / 42 / 134 / 54 | 0.300 | 0.250 | 0.761 | 0.506 | 0.463 | 8 / 16 |
| minute_threshold | selected_review | 4 / 11 / 33 / 14 | 0.267 | 0.222 | 0.750 | 0.486 | 0.460 | 2 / 4 |
| clock_quarter_hour_threshold | development | 44 / 103 / 73 / 28 | 0.299 | 0.611 | 0.415 | 0.513 | 0.564 | 8 / 16 |
| clock_quarter_hour_threshold | review | 39 / 93 / 83 / 33 | 0.295 | 0.542 | 0.472 | 0.507 | 0.486 | 8 / 16 |
| clock_quarter_hour_threshold | selected_review | 12 / 18 / 26 / 6 | 0.400 | 0.667 | 0.591 | 0.629 | 0.550 | 2 / 4 |
| comment_equality | development | 24 / 49 / 127 / 48 | 0.329 | 0.333 | 0.722 | 0.527 | 0.529 | 8 / 16 |
| comment_equality | review | 24 / 43 / 133 / 48 | 0.358 | 0.333 | 0.756 | 0.545 | 0.544 | 8 / 16 |
| comment_equality | selected_review | 6 / 12 / 32 / 12 | 0.333 | 0.333 | 0.727 | 0.530 | 0.533 | 2 / 4 |
| position_quartile | development | 43 / 82 / 94 / 29 | 0.344 | 0.597 | 0.534 | 0.566 | 0.559 | 8 / 16 |
| position_quartile | review | 32 / 97 / 79 / 40 | 0.248 | 0.444 | 0.449 | 0.447 | 0.494 | 8 / 16 |
| position_quartile | selected_review | 6 / 27 / 17 / 12 | 0.182 | 0.333 | 0.386 | 0.360 | 0.442 | 2 / 4 |
| constant | development | 0 / 0 / 176 / 72 | undefined | 0.000 | 1.000 | 0.500 | 0.500 | 8 / 16 |
| constant | review | 0 / 0 / 176 / 72 | undefined | 0.000 | 1.000 | 0.500 | 0.500 | 8 / 16 |
| constant | selected_review | 0 / 0 / 44 / 18 | undefined | 0.000 | 1.000 | 0.500 | 0.500 | 2 / 4 |

Source-convention reference on review groups (definitional, not validation): 72 / 0 / 176 / 0 TP/FP/TN/FN; history-macro BA 1.000; 16 one-class or empty groups remain undefined.

Frozen selectors (parameters come only from development):

```json
{
  "date_equality": {
    "family": "date_equality",
    "feature": "date",
    "operation": "eq",
    "value": "2026-06-05",
    "polarity": false
  },
  "date_threshold": {
    "family": "date_threshold",
    "feature": "date",
    "operation": "le",
    "value": "2026-06-06",
    "polarity": false
  },
  "day_threshold": {
    "family": "day_threshold",
    "feature": "day",
    "operation": "le",
    "value": 6,
    "polarity": false
  },
  "hour_threshold": {
    "family": "hour_threshold",
    "feature": "hour",
    "operation": "le",
    "value": 12,
    "polarity": false
  },
  "minute_threshold": {
    "family": "minute_threshold",
    "feature": "minute",
    "operation": "le",
    "value": 45,
    "polarity": false
  },
  "clock_quarter_hour_threshold": {
    "family": "clock_quarter_hour_threshold",
    "feature": "minute_of_day",
    "operation": "le",
    "value": 734,
    "polarity": false
  },
  "comment_equality": {
    "family": "comment_equality",
    "feature": "comment",
    "operation": "eq",
    "value": "Approved.",
    "polarity": true
  },
  "position_quartile": {
    "family": "position_quartile",
    "feature": "position_quartile",
    "operation": "le",
    "value": 1,
    "polarity": false
  },
  "constant": {
    "family": "constant",
    "operation": "constant",
    "value": false
  }
}
```

Overall development winner: `{"family": "minute_threshold", "feature": "minute", "operation": "le", "value": 45, "polarity": false}`.

| Review surface | Distinct values | Cross-class shared values | Exact observed separation |
| --- | ---: | ---: | --- |
| date | 25 | 13 | False |
| day | 25 | 13 | False |
| hour | 10 | 10 | False |
| minute | 60 | 43 | False |
| minute_of_day | 198 | 23 | False |
| comment | 6 | 6 | False |
| position_quartile | 4 | 4 | False |
| exact_timestamp | 247 | 0 | True |
| joint_signature | 248 | 0 | True |

## Construction checks and review flags

Hard checks concern common comments, day/hour support, earlier/later hard negatives and record kind
within current accepted reviews. Old-version dates in the broad population are not defects.

```json
{
  "requires_investigation": false,
  "construction_failures": [],
  "perfect_heldout_selectors": [],
  "hardnegative_evidence_available": true,
  "human_material_approval": "pending"
}
```

The [complete audit](surface-audit.json) contains every selected predictor, constant baseline,
source-oracle reference, per-history denominator and overlap/construction result.

- No final-test cases or model outputs are used.
- Broad-population dates can legitimately distinguish expired approvals.
- Exact joint signatures can memorise small samples; separation is diagnostic, not a hard failure.
- Nonperfect elevated accuracy is reported; it is not equated with chance.
- Mixed list order is descriptive; chance patterns in one short list do not trigger a redraw.
- Only the prespecified surface selectors are tested; other shortcuts may exist.
- This material audit is separate from the inference headroom criterion.
