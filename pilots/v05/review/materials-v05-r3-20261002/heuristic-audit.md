# v0.5 heuristic audit (material r3)

Histories constructed from the review and development seeds: 32 (generation stops on any failed condition). No model calls.

Each cell gives how often a shortcut reaches the warranted action at the hard task. Shortcuts that must never succeed by construction: nearest neighbour and every misreading under fallback (b).

## Reference lines

| Setting and hard type | nearest_neighbour | compatible_majority | simplest_compatible | always_keep |
| --- | ---: | ---: | ---: | ---: |
| K-L transfer_change | 0/4 | 4/4 | 4/4 | 0/4 |
| K-L unidentifiable | 0/4 | 4/4 | 4/4 | 4/4 |
| K-S transfer_change | 0/4 | 4/4 | 4/4 | 0/4 |
| K-S unidentifiable | 0/4 | 4/4 | 4/4 | 4/4 |
| U-L transfer_change | 0/4 | 4/4 | 4/4 | 0/4 |
| U-L unidentifiable | 0/4 | 4/4 | 4/4 | 4/4 |
| U-S transfer_change | 0/4 | 4/4 | 4/4 | 0/4 |
| U-S unidentifiable | 0/4 | 4/4 | 4/4 | 4/4 |

## Misreadings

Oracle reading: the misread evidence fed to the oracle; a contradiction is "undefined" and is not a success. Fallback (a): a contradiction means keep, so unidentifiable tasks are structurally always right under (a), like always-keep. Fallback (b): majority of the misread evidence in the exact context, otherwise the nearest neighbour over binding plus misread evidence.

### all_accepted_reviews

| Setting and hard type | oracle reading | fallback (a) | fallback (b) |
| --- | ---: | ---: | ---: |
| K-L transfer_change | 0/4 (undefined 4) | 0/4 | 0/4 |
| K-L unidentifiable | 0/4 (undefined 4) | 4/4 | 0/4 |
| K-S transfer_change | 0/4 (undefined 4) | 0/4 | 0/4 |
| K-S unidentifiable | 0/4 (undefined 4) | 4/4 | 0/4 |
| U-L transfer_change | 0/4 (undefined 4) | 0/4 | 0/4 |
| U-L unidentifiable | 0/4 (undefined 4) | 4/4 | 0/4 |
| U-S transfer_change | 0/4 (undefined 4) | 0/4 | 0/4 |
| U-S unidentifiable | 0/4 (undefined 4) | 4/4 | 0/4 |

### inverted_rejections

| Setting and hard type | oracle reading | fallback (a) | fallback (b) |
| --- | ---: | ---: | ---: |
| K-L transfer_change | 0/4 (undefined 4) | 0/4 | 0/4 |
| K-L unidentifiable | 0/4 (undefined 4) | 4/4 | 0/4 |
| K-S transfer_change | 0/4 (undefined 4) | 0/4 | 0/4 |
| K-S unidentifiable | 1/4 (undefined 3) | 4/4 | 0/4 |
| U-L transfer_change | 0/4 (undefined 4) | 0/4 | 0/4 |
| U-L unidentifiable | 0/4 (undefined 4) | 4/4 | 0/4 |
| U-S transfer_change | 1/4 (undefined 3) | 1/4 | 0/4 |
| U-S unidentifiable | 0/4 (undefined 2) | 2/4 | 0/4 |

### rejections_as_assent

| Setting and hard type | oracle reading | fallback (a) | fallback (b) |
| --- | ---: | ---: | ---: |
| K-L transfer_change | 0/4 (undefined 4) | 0/4 | 0/4 |
| K-L unidentifiable | 0/4 (undefined 4) | 4/4 | 0/4 |
| K-S transfer_change | 0/4 (undefined 4) | 0/4 | 0/4 |
| K-S unidentifiable | 1/4 (undefined 3) | 4/4 | 0/4 |
| U-L transfer_change | 0/4 (undefined 4) | 0/4 | 0/4 |
| U-L unidentifiable | 0/4 (undefined 4) | 4/4 | 0/4 |
| U-S transfer_change | 0/4 (undefined 4) | 0/4 | 0/4 |
| U-S unidentifiable | 0/4 (undefined 4) | 4/4 | 0/4 |

### followed_preferences

| Setting and hard type | oracle reading | fallback (a) | fallback (b) |
| --- | ---: | ---: | ---: |
| K-L transfer_change | 0/4 (undefined 4) | 0/4 | 0/4 |
| K-L unidentifiable | 0/4 (undefined 4) | 4/4 | 0/4 |
| K-S transfer_change | 0/4 (undefined 4) | 0/4 | 0/4 |
| K-S unidentifiable | 0/4 (undefined 1) | 1/4 | 0/4 |
| U-L transfer_change | 0/4 (undefined 4) | 0/4 | 0/4 |
| U-L unidentifiable | 0/4 (undefined 4) | 4/4 | 0/4 |
| U-S transfer_change | 0/4 (undefined 4) | 0/4 | 0/4 |
| U-S unidentifiable | 0/4 (undefined 2) | 2/4 | 0/4 |

## Distractor agreement with the world

| Type | Size | Location | World | Counter |
| --- | --- | --- | ---: | ---: |
| approval without target | large | exact | 3 | 13 |
| approval without target | large | relevant | 91 | 91 |
| approval without target | large | rest | 295 | 291 |
| approval without target | small | exact | 3 | 13 |
| approval without target | small | relevant | 2 | 1 |
| approval without target | small | rest | 5 | 8 |
| preference | large | exact | 3 | 13 |
| preference | large | relevant | 83 | 82 |
| preference | large | rest | 301 | 302 |
| preference | small | exact | 3 | 13 |
| preference | small | relevant | 1 | 2 |
| preference | small | rest | 6 | 7 |
| rejected version | large | relevant | 62 | 61 |
| rejected version | large | rest | 330 | 331 |
| rejected version | small | rest | 16 | 16 |
| review outside roster | large | exact | 3 | 13 |
| review outside roster | large | relevant | 97 | 95 |
| review outside roster | large | rest | 292 | 284 |
| review outside roster | small | exact | 3 | 13 |
| review outside roster | small | relevant | 4 | 3 |
| review outside roster | small | rest | 14 | 11 |

Nearest rejected version farther from the hard task than the nearest binding approval: 32 of 32 histories.
Each listed reviewer approves both configurations in 32 of 32 histories.
Name collisions between people and attribute values: 0.
