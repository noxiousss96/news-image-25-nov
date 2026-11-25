[![make.fun](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/noxiousss96/news-image-25-nov/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/noxiousss96/news-image-25-nov/reward.svg)](https://make.fun/bounty/news-image-20261125)

# THE WORLD — Wednesday 25 November 2026's world news in one image

Entry for the [make.fun](https://make.fun) bounty
[news-image-20261125](https://make.fun/bounty/news-image-20261125):
"Sum up 25 November's world news in one image".

`main.ts` (Node 22, standard library only) copies the pre-rendered
`assets/entry.png` to `/output/entry.png`. The image is a newspaper front
page drawn from scratch with PIL (`gen_image.py`): deterministic, no network,
no randomness — every run writes identical bytes. The front page is
1024x1024 px and under 1 MiB, as the competition requires.

## Stories on the front page

- **Houthi strike hits Riyadh Tower** — rebels struck the PIF Tower in
  Riyadh's financial district, wounding at least 11 people.
- **Oil tankers hit by mines in Hormuz** — Iran claims three tankers hit
  naval mines and caught fire; the claim is unverified.
- **NATO vows space defence** — after reports Russia may launch a
  nuclear-armed satellite.
- **Putin: retaliation "inevitable"** — after Ukraine hit Russian oil plants.
- **Huang's $34 billion day** — Nvidia's Jensen Huang recouped nearly $34bn
  in a day after being reinstated as CEO.
- **UN court condemns Myanmar** — the UN's top court condemned Myanmar over
  genocidal actions against the Rohingya.

## Regenerate the image

```sh
python3 gen_image.py   # writes assets/entry.png (1024x1024, deterministic)
```

## License

MIT — see [LICENSE](LICENSE).
