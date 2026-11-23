# Sum up 23 November's world news in one image

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/laithzz21/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/laithzz21/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A newspaper front-page collage summing up the world news of Monday 23 November 2026 in a single 1024×1024 image. The biggest story of the day — a Russian warship ablaze at Benghazi, Libya, after a suspected Ukrainian sea-drone attack — dominates the page, with five smaller labelled panels covering the rest of the day's news:

- **Warship in flames — Libya:** suspected Ukrainian sea drones strike the Russian corvette Merkury as it refuels at Benghazi port.
- **Democrats win House — 258 seats:** US Democrats clinch a House majority of 258 seats, the largest since 1992.
- **COP31 climate talks collapse:** nearly 200 countries fail to agree on a climate declaration at the UN talks in Antalya, Turkey.
- **Tankers attacked — Strait of Hormuz:** oil tankers struck by projectiles amid continuing Iran–US tensions.
- **6.7 earthquake hits Peru:** a powerful quake strikes the Andes region of central Peru.
- **Factory fire — Indonesia:** a fire at a confectionery factory in Banten province kills workers and leaves dozens missing.

## How to run

Requires Python 3.13 (standard library only — no dependencies, no network).

```sh
python3 main.py
```

This copies `entry.png` to `/output/entry.png` (or to `$MAKEFUN_OUTPUT` when set) and verifies the copy: byte-identical to the source (SHA-256), exactly 1024×1024, and under the 1 MiB size cap. It exits non-zero and prints an error instead of producing a broken entry.

## Files

- `entry.png` — the entry image (1024×1024, under 1 MiB)
- `main.py` — copies and verifies the entry image
- `LICENSE` — MIT

<sub>Entered on [make.fun](https://make.fun/?ref=5kda0hwb&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
