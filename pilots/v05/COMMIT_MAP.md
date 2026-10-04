# Commit map for the v0.5 identity rewrite

On 4 October 2026, before the first push of branch `pilot-v05`, the author and committer of ten local commits were changed from an institutional address to `Milad Morad <47043126+miladmo@users.noreply.github.com>`, decided by Milad Morad. Only name and address changed: every file tree is identical, so each new commit corresponds to its old one through the same tree hash. Commit messages and dates are unchanged. The first six v0.5 commits kept their hashes.

One committed record names an old hash: `pilots/v05/preflight/dcheck-20261003-attempt2/verification.json` refers to `c560fe2`, which is now `1b49052`. The unchanged branch is kept outside the repository as a git bundle (`pilot-v05-before-identity-rewrite-20261004.bundle`, SHA-256 `cc82288c4155cef4b6286e148ab4920891230e3c5051cb590b1d6e0ea1a7cc7d`).

| Old commit | New commit | Tree (identical) | Subject |
| --- | --- | --- | --- |
| `59bdd60d36b4` | `59bdd60d36b4` | `30932f69af2d` | Start pilot v0.5: protocol, rule classes, oracle and generator |
| `7325df50c42b` | `7325df50c42b` | `8461b745ef34` | Add v0.5 arms, runner and material review export |
| `cd9c9751e81a` | `cd9c9751e81a` | `c61c362f2b18` | v0.5 material revision r2 after the first material review |
| `757b87b01e84` | `757b87b01e84` | `cf5a3ebdff7d` | v0.5 material revision r3 after the second material review |
| `86c1e26563cc` | `86c1e26563cc` | `3a2c4a719953` | v0.5: record r3 approval, freeze prompts, prepare calibration request |
| `7129302f0b9d` | `7129302f0b9d` | `494ca2e5600e` | v0.5 calibration: two stopped attempts, timeout correction, attempt 3 |
| `2a26f9ecff3d` | `cc7d09451d09` | `8911da2b4b3e` | v0.5 calibration attempt 3 complete: headroom exists |
| `b28e09cc43c1` | `13c30760b9e5` | `28316d0a7ae9` | v0.5: prepare and approve the D technical check |
| `c560fe2fb029` | `1b4905271dcf` | `765c7ae7fd09` | v0.5 D technical check: two query contract defects found and fixed |
| `d8b5fc769742` | `c0920ab547de` | `5f3b64eaae93` | v0.5: prepare and approve the second D technical check |
| `9e5862e76b22` | `ab01ec37cdeb` | `5b9a71309b9d` | v0.5 second D technical check complete |
| `3e3a318b92b2` | `ecb467328935` | `157b4afbefa0` | v0.5: freeze D and all sources, prepare the main run |
| `c73103a1bb8e` | `cf19c0f0f003` | `6b5a6d9dce23` | v0.5: main run live approval ("Hauptlauf live freigegeben") |
| `e42f26965f0f` | `4899cd5892dd` | `2f872f014865` | v0.5 main run complete |
| `009e819aaf21` | `2e3f7539d302` | `e43f25008d83` | v0.5: main-run analysis and draft report for the attribution review |
| `cee9b99db85b` | `06a32e16e335` | `66f0d83245a8` | v0.5: attribution review part 1 incorporated, case files for part 2 |

The tag `pilot-v05-frozen-20261003` was moved from `3e3a318b92b2` to `ecb467328935`, the same tree.
