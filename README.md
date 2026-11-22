# The World — 22 November 2026

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/xiaokai2013/makefun-news-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/xiaokai2013/makefun-news-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

A one-image newspaper front page summing up Sunday 22 November 2026
— built for the [make.fun bounty](https://make.fun/bounty/news-image-20261122)
"Sum up 22 November's world news in one image".

## What's on the page

Seven verified stories from the day:

1. **Russia sends 186 drones at Ukraine overnight; Kyiv block destroyed** — air
   defences down 161; a five-storey apartment block near Kyiv is flattened,
   14 people feared trapped under the rubble.
2. **Houthis fire new missile at western Saudi Arabia** — coalition intercepts
   it early Sunday; civil defence warns the Mecca region.
3. **Trump vows to cap credit card interest at 10%** — the president says he
   will work with Democrats on the cap.
4. **Boat capsizes on way to funeral; 24 dead** — the vessel was carrying
   mourners in southern Nigeria.
5. **Toxic alcohol kills 11 in Manipur, 180 in hospital** — more than 180
   people hospitalised, officials say.
6. **Drones attack Russian cargo ship in Gulf of Finland** — the vessel catches
   fire after the strike in the Baltic.
7. **Factory fire near Jakarta kills 3; 36 missing** — search goes on at the
   confectionery plant.

## How it works

- `news.json` — the seven stories, with a masthead, datelines and a
  source footer. Every headline was checked against reporting published
  on 22 November 2026.
- `render.py` — build tool (Pillow + Liberation fonts). Draws the
  1024x1024 front page and writes `entry.png`.
- `main.py` — the graded entrypoint. Standard library only: it copies the
  committed `entry.png` to `/output/entry.png`, because the grader runs
  in a bare `python:3.13-slim` container with no Pillow and no fonts.

## Rebuild

```bash
pip install Pillow
python3 render.py        # regenerates entry.png (deterministic)
python3 main.py          # copies entry.png to /output/entry.png
```

## License

MIT — see [LICENSE](LICENSE).
