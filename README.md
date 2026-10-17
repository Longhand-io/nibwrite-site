# oakfall-site

The public face of [Oakfall](https://github.com/oakfall/oakfall): the website, the brand, and shared resources.

- The pages (`index.html`, `features.html`, `gall.html`, `pricing.html`, `download.html`, `faq.html`) are **generated** by `hack/build-site.py` and served by GitHub Pages at https://oakfall.app/
- `assets/site.css` and `assets/site.js`: the shared styles and behaviour (theme toggle, the typed banner, Gall in the word, Gall the scroll guide, the arrow-key easter egg).
- `assets/shots/`: screenshots of the app's desk used on the pages.
- `preview/index.html`: the in-browser desk at https://oakfall.app/preview, copied from the app's preview build.
- `brand/`: logo files, colours, type, and voice. Start with [brand/README.md](brand/README.md).
- `CNAME`: the custom domain for GitHub Pages. Do not delete it, or oakfall.app stops serving.

## Updating the site

1. Edit the page content in `hack/build-site.py` (one shell for the header, tabs and footer, then one block per page) or the shared files in `assets/`. Do not hand-edit the generated `.html` pages; the next build overwrites them.
2. Build: `python3 hack/build-site.py`.
3. Look at it: open `index.html` in a browser, or run `python3 -m http.server` in this folder and visit http://localhost:8000.
4. Commit with `git commit -s` and push to `main`. GitHub Pages rebuilds on push, usually within a minute; https://oakfall.app may serve the old copy from cache for another few seconds.

The FAQ's questions live in `hack/faq-body.html` between the `faq:start` and `faq:end` markers, which the importer's FAQ sync replaces. The social card is `brand/social/social-preview.html`, rendered to `social-preview.png` at 1280×640 with any headless browser.

Brand rules that the pages follow: the wordmark is Plus Jakarta Sans 700 with Gall as the l, in every layout; the look is Moss (green-tinted paper, deep moss for action), light by default, with a forest-green dark mode on the toggle; no orange-and-black.

The plugin and spec live in [oakfall](https://github.com/oakfall/oakfall). The importer lives in [scrivener-to-obsidian](https://github.com/oakfall/scrivener-to-obsidian).

Oakfall is independent. Product names belong to their owners.

Text and design: Apache License 2.0, copyright 0xSpectra LLC and the Oakfall Authors. Logo files: trademarks of 0xSpectra LLC; use them to refer to Oakfall, never to imply endorsement. See TRADEMARKS.md in the oakfall repository.
