# ryutarotanno.com

Personal website of Ryutaro Tanno, built with [Hugo](https://gohugo.io/) (extended, 0.169) and deployed to
GitHub Pages at <https://ryutarotanno.com> by `.github/workflows/deploy.yml` on every push to `master`.

## Working on it

```sh
hugo server            # http://localhost:1313
```

Most content is data, not templates:

| What | Where |
| --- | --- |
| Intro, past paragraphs, contact links | `data/site.yaml` |
| Japanese home page (`/ja/`) | `data/ja.yaml`, plus `*_ja` fields in `data/selected_work.yaml` |
| Selected Work | `data/selected_work.yaml` (illustrations in `assets/art/`) |
| Publications, patents | `data/publications.yaml`, `data/patents.yaml` |
| Talks, press | `data/talks.yaml`, `data/press.yaml` |
| News (hidden unless `show_news = true`) | `data/news.yaml` |

The career drawing on the home page is generated: edit milestones, eras or scenery in
`tools/journey_layout.py`, then run `python3 tools/journey_layout.py data/journey.yaml`.

## Launch mode

The site has two states, switched by `launch` in `hugo.toml`:

- **`launch = false`** (current): no current employer is named anywhere.
- **`launch = true`**: the site also reads `data/launch.yaml`, which holds all launch-only wording (mission line,
  description, social card subtitle, structured data, the next milestone in the career drawing, the launch essay,
  the Work with me page and its footer link).

`data/launch.yaml` is gitignored and must not be committed before launch day, because this repository is public.
To preview launch mode locally without changing `hugo.toml`, create a config override containing
`[params] launch = true` and run `hugo server --config hugo.toml,<override>.toml`.

Launch-only copy that is still missing is left out of the built site rather than shown empty; `hugo server`
shows a TODO marker for each gap.

On launch day: remove `/data/launch.yaml` from `.gitignore`, commit it, set `launch = true`, push, and check the
live site. The deploy runs on GitHub, so it only sees `data/launch.yaml` once it is committed.
