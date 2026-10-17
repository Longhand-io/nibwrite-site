#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 0xSpectra LLC and the Oakfall Authors.
"""Build the Oakfall site's pages from one shared shell.

    python3 hack/build-site.py

Writes index.html, features.html, gall.html, pricing.html, download.html and faq.html at the
repo root. The FAQ's questions live in hack/faq-body.html between the faq markers, which the
importer's FAQ sync replaces; everything else is here.
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEAF = "M50 4 C 74 14, 84 40, 72 66 C 66 78, 58 84, 50 92 C 42 84, 34 78, 28 66 C 16 40, 26 14, 50 4Z"


def body(cut):
    return (f'<g transform="rotate(-10 50 50)"><path d="{LEAF}" fill="currentColor"/><g class="eyes">'
            f'<circle cx="42" cy="32" r="4.2" fill="{cut}"/><circle cx="58" cy="32" r="4.2" fill="{cut}"/>'
            f'<circle cx="43" cy="32.6" r="1.8" fill="currentColor"/><circle cx="59" cy="32.6" r="1.8" fill="currentColor"/></g>'
            f'<circle cx="50" cy="52" r="3.2" fill="{cut}"/><path d="M50 56 V 80" stroke="{cut}" stroke-width="2.4" stroke-linecap="round"/>'
            f'<path d="M50 92 V 99" stroke="currentColor" stroke-width="4" stroke-linecap="round"/></g>')


GALL_L = (f'<svg viewBox="10 -2 80 104" aria-hidden="true"><g class="gl">{body("var(--paper)")}</g>'
          f'<path class="ghost" transform="rotate(-10 50 50)" d="{LEAF}" fill="none" stroke="currentColor" stroke-width="3" stroke-dasharray="4 4"/></svg>')
GALL_AV = f'<svg viewBox="-6 -4 112 108" aria-hidden="true">{body("var(--ink)")}</svg>'
HAT = ('<path d="M26 16 C 36 10, 64 10, 74 16" stroke="currentColor" stroke-width="4" stroke-linecap="round" fill="none"/>'
       '<path d="M36 14 L 38 -2 L 62 -3 L 64 13 Z" fill="currentColor"/>'
       '<path d="M40 0 C 30 -8, 18 -6, 10 4" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" fill="none"/>')
WAND = ('<g class="wand"><path d="M62 50 C 68 50, 72 48, 76 44" stroke="currentColor" stroke-width="4" stroke-linecap="round" fill="none"/>'
        '<path d="M76 44 L 94 20" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>'
        '<path class="star" d="M94 20 l 2.5 -6 l 2.5 6 l 6 2.5 l -6 2.5 l -2.5 6 l -2.5 -6 l -6 -2.5 Z" fill="var(--moss)"/></g>')
GUIDE = (f'<div class="guide" id="guide" aria-hidden="true"><svg viewBox="-14 -22 128 128"><g class="skate">{body("var(--paper)")}'
         f'<g transform="rotate(-10 50 50)">{HAT}<path d="M38 50 C 30 58, 30 66, 36 72" stroke="currentColor" stroke-width="4" stroke-linecap="round" fill="none"/>{WAND}</g></g></svg></div>'
         '<div class="say" id="say" role="status"></div>')

OUTFITS = {
    "Tutorial": f'<g transform="rotate(-10 50 50)">{HAT}{WAND}</g>',
    "Editor": '<g transform="rotate(-10 50 50)"><circle cx="42" cy="32" r="7.5" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="58" cy="32" r="7.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M49.5 32 H 50.5 M34.5 31 L 27 28 M65.5 31 L 73 28" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></g>',
    "Winter": '<g transform="rotate(-10 50 50)"><path d="M28 22 C 30 4, 70 4, 72 22 Z" fill="#5e8a5c"/><path d="M26 20 H 74" stroke="#c9a24a" stroke-width="7" stroke-linecap="round"/><circle cx="50" cy="4" r="5" fill="#c9a24a"/><path d="M30 60 C 40 66, 60 66, 70 60" stroke="#b4491b" stroke-width="8" stroke-linecap="round" fill="none"/><path d="M66 62 L 72 80" stroke="#b4491b" stroke-width="7" stroke-linecap="round"/></g>',
    "Spring": '<g transform="rotate(-10 50 50) translate(66 12)"><circle r="4" fill="#c9a24a"/><circle cx="0" cy="-6" r="3.2" fill="#e8a0b4"/><circle cx="5.7" cy="-1.8" r="3.2" fill="#e8a0b4"/><circle cx="3.5" cy="4.9" r="3.2" fill="#e8a0b4"/><circle cx="-3.5" cy="4.9" r="3.2" fill="#e8a0b4"/><circle cx="-5.7" cy="-1.8" r="3.2" fill="#e8a0b4"/></g>',
    "Summer": '<g transform="rotate(-10 50 50)"><path d="M33 29 H 49 V 36 Q 49 40 44 40 H 38 Q 33 40 33 36 Z M51 29 H 67 V 36 Q 67 40 62 40 H 56 Q 51 40 51 36 Z" fill="#1a1b20"/><path d="M49 31 H 51 M33 30 L 27 27 M67 30 L 73 27" stroke="#1a1b20" stroke-width="1.8" stroke-linecap="round"/></g>',
    "Autumn": '<g transform="rotate(-10 50 50) translate(0 -3)"><path d="M30 20 C 30 4, 70 4, 70 20 Z" fill="#8c6a2e"/><path d="M28 20 H 72" stroke="#8c6a2e" stroke-width="5" stroke-linecap="round"/><path d="M50 4 V -2" stroke="#8c6a2e" stroke-width="3" stroke-linecap="round"/></g>',
    "Milestone": '<g transform="rotate(-10 50 50) translate(0 -2)"><path d="M40 16 L 50 -14 L 60 16 Z" fill="#5e8a5c"/><path d="M44 6 L 56 6 M42 12 L 58 12" stroke="#c9a24a" stroke-width="2.4"/><circle cx="50" cy="-14" r="3.5" fill="#c9a24a"/></g>',
    "Laurels": '<g transform="rotate(-10 50 50)"><path d="M26 30 C 22 20, 30 10, 40 8 M74 30 C 78 20, 70 10, 60 8" stroke="#5e8a5c" stroke-width="2.4" stroke-linecap="round" fill="none"/><g fill="#5e8a5c"><ellipse cx="28" cy="22" rx="2.2" ry="4" transform="rotate(30 28 22)"/><ellipse cx="33" cy="13" rx="2.2" ry="4" transform="rotate(50 33 13)"/><ellipse cx="72" cy="22" rx="2.2" ry="4" transform="rotate(-30 72 22)"/><ellipse cx="67" cy="13" rx="2.2" ry="4" transform="rotate(-50 67 13)"/></g></g>',
}


def outfit_cards():
    return "".join(f'<div class="outfit"><span class="gall"><svg viewBox="-14 -22 128 128" aria-hidden="true">{body("var(--card)")}{o}</svg></span>{n}</div>' for n, o in OUTFITS.items())


def ic(d):
    return f'<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{d}</svg>'


I = {
    "binder": ic('<rect x="3" y="3" width="18" height="18" rx="2.5"/><path d="M9 3v18M12.5 8h5M12.5 12h5M12.5 16h3"/>'),
    "inspector": ic('<rect x="3" y="3" width="18" height="18" rx="2.5"/><path d="M15 3v18"/><path d="M6.5 8h5M6.5 12h5"/>'),
    "cast": ic('<circle cx="9" cy="8" r="3.2"/><path d="M3.5 19c.6-3 2.8-5 5.5-5s4.9 2 5.5 5"/><circle cx="17" cy="9" r="2.4"/><path d="M15.5 14.2c2.4.2 4.2 2 4.8 4.8"/>'),
    "map": ic('<path d="M3 6l6-3 6 3 6-3v15l-6 3-6-3-6 3z"/><path d="M9 3v15M15 6v15"/>'),
    "threads": ic('<path d="M3 7h6M3 12h10M3 17h7"/><circle cx="12" cy="7" r="1.6"/><circle cx="16" cy="12" r="1.6"/><circle cx="13" cy="17" r="1.6"/><path d="M14 7h7M18 12h3M15 17h6"/>'),
    "look": ic('<circle cx="12" cy="12" r="9"/><path d="M12 3a9 9 0 000 18z" fill="currentColor"/>'),
    "snap": ic('<path d="M4 7h3l2-3h6l2 3h3v12H4z"/><circle cx="12" cy="13" r="3.5"/>'),
    "compile": ic('<path d="M6 3h9l4 4v14H6z"/><path d="M14 3v5h5M9 12h7M9 16h7"/>'),
    "apple": '<svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" aria-hidden="true"><path d="M16.4 12.6c0-2.4 2-3.6 2.1-3.7-1.1-1.7-2.9-1.9-3.5-1.9-1.5-.2-2.9.9-3.7.9-.8 0-1.9-.9-3.2-.8-1.6 0-3.1 1-4 2.4-1.7 3-.4 7.4 1.2 9.8.8 1.2 1.8 2.5 3 2.4 1.2 0 1.7-.8 3.1-.8 1.5 0 1.9.8 3.2.8s2.1-1.2 2.9-2.4c.9-1.4 1.3-2.7 1.3-2.8 0 0-2.4-1-2.4-3.9zM14 5.5c.7-.8 1.1-1.9 1-3-1 0-2.1.7-2.8 1.5-.6.7-1.2 1.8-1 2.9 1.1.1 2.2-.6 2.8-1.4z"/></svg>',
}

TABS = [("index.html", "Home"), ("features.html", "Features"), ("gall.html", "Gall"), ("pricing.html", "Pricing"), ("download.html", "Download"), ("faq.html", "FAQ")]


def wm():
    return f'<span class="gall-l" title="Gall">{GALL_L}</span>'


def shell(page, title, desc, main):
    current = ' aria-current="page"'
    tabs = "".join(f'<a href="{h}"{current if h == page else ""}>{n}</a>' for h, n in TABS)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="canonical" href="https://oakfall.app/{'' if page == 'index.html' else page}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://oakfall.app/brand/social/social-preview.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="color-scheme" content="light">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700&family=Plus+Jakarta+Sans:wght@600;700;800&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/site.css">
</head>
<body>
<header class="bar">
  <div class="wrap">
    <a class="wm" href="index.html" aria-label="Oakfall home">Oakfa{wm()}l</a>
    <nav class="tabs" aria-label="Pages">{tabs}</nav>
    <div class="right">
      <button class="theme" id="theme" type="button">Dark</button>
      <a class="btn sm primary" href="download.html">Download <span class="soon">Soon</span></a>
    </div>
  </div>
</header>
<main>
{main}
</main>
<footer>
  <div class="wrap">
    <a class="wm" href="index.html" aria-label="Oakfall home">Oakfa{wm()}l</a>
    <nav aria-label="Footer">
      {"".join(f'<a href="{h}">{n}</a>' for h, n in TABS[1:])}
      <a href="https://github.com/oakfall/oakfall/blob/main/docs/spec.md">Vault spec</a>
      <a href="https://github.com/oakfall">GitHub</a>
      <span>hello@oakfall.app</span>
    </nav>
    <p>Oakfall is made by grassclaw and published by 0xSpectra LLC. The spec, the importer and the plugin are open source under Apache-2.0. Product names belong to their owners.</p>
  </div>
</footer>
{GUIDE if page == 'index.html' else ''}
<script src="assets/site.js" defer></script>
</body>
</html>
'''


COMPARE = '''<div class="compare quiet" id="compare" aria-label="Comparing a snapshot with the live text">
      <div class="cbar"><div><strong>First draft</strong>, snapshot taken 19 Jan 2020</div><div><strong>Now</strong>, editing</div></div>
      <div class="panes">
        <div class="pane">
          <p>Mara found the letter <del>under the floorboard where her mother had always said nothing was hidden</del>. She read it twice <del>and then a third time</del>, standing, because sitting felt like agreeing to it.</p>
          <p>Outside, the rain <del>had not stopped</del>.</p>
        </div>
        <div class="pane">
          <p>Mara found the letter <ins>in the tin with the buttons, which was the one place her mother never looked</ins>. She read it twice, standing, because sitting felt like agreeing to it.</p>
          <p>Outside, the rain <ins>kept its own counsel</ins>.</p>
        </div>
      </div>
      <div class="foot">snap(Manuscript/01 Part One/02 The Letter.md): First draft &nbsp; Snapshot-Doc-Id: 9B2C1F7A… &nbsp; Word-Count: 61</div>
    </div>'''

CHAT = f'''<div class="chat" aria-label="Example conversation with Gall">
          <div class="msg"><div class="av">You</div><div class="bub you">what changed in the tin since the june snapshot?</div></div>
          <div class="msg"><div class="av g">{GALL_AV}</div><div class="bub">Two things in <i>02 The Tin</i>: the dream sequence is gone, 412 words, and Mara now opens the tin in the kitchen instead of the yard.<div class="chips"><span>Compare side by side</span><span>Restore the dream</span></div></div></div>
          <div class="msg"><div class="av">You</div><div class="bub you">did i lose anything other scenes depend on?</div></div>
          <div class="msg"><div class="av g">{GALL_AV}</div><div class="bub">One thing. <i>08 Last Stall</i> mentions "the dream about the buttons", which only existed in the cut passage.<div class="chips"><span>Open 08 Last Stall at that line</span></div></div></div>
        </div>'''

FORMATS = '''<div class="formats">
      <div class="format"><span class="ext">.md</span><div><b>Markdown folders</b><small>Open any folder of Markdown as a project; nothing is converted.</small></div><span class="state now">Today</span></div>
      <div class="format"><span class="ext">vault</span><div><b>Obsidian vaults</b><small>The same files open in Oakfall and in Obsidian, with the Oakfall plugin or without.</small></div><span class="state now">Today</span></div>
      <div class="format"><span class="ext">.scriv</span><div><b>.scriv projects</b><small>Binder, metadata, research and every snapshot, replayed as history with original titles and dates.</small></div><span class="state now">Today</span></div>
      <div class="format"><span class="ext">git</span><div><b>Git history</b><small>Snapshots can be ordinary commits; push the project anywhere you already keep code or notes.</small></div><span class="state now">Today</span></div>
      <div class="format"><span class="ext">.docx</span><div><b>Word documents</b><small>Send a manuscript out, bring an editor's redlines and comments back in as suggestions.</small></div><span class="state">Editorial</span></div>
      <div class="format"><span class="ext">.epub</span><div><b>Compile to PDF, EPUB, DOCX</b><small>Manuscript format, paperback spread, ebook, from presets.</small></div><span class="state">Sync</span></div>
    </div>'''

PLANS = '''<div class="plans">
      <div class="plan"><h3>Oakfall</h3><div class="price">Free</div><p class="pitch">Everything you need to write a book.</p><ul><li>Binder, page, inspector, snapshots and compare</li><li>Cast, places, maps, threads and timeline</li><li>Gall's lookups offline, or your own key or local model</li><li>Every look and layout, Focus</li></ul></div>
      <div class="plan"><h3>Sync</h3><div class="price">$5<small> / month</small></div><p class="pitch">$4 a month billed yearly.</p><ul><li>End-to-end encrypted sync between desktop, tablet and phone</li><li>Snapshots and history on every device</li><li>Compile presets for manuscript, paperback and ebook</li></ul></div>
      <div class="plan pro"><h3>Gall</h3><div class="price">$20<small> / month</small></div><p class="pitch">Hosted models; nothing to set up.</p><ul><li>Gall reads your prose: what changed, what depends on a cut, does a synopsis still match</li><li>Continuity checks across the whole book</li><li>No key or local model needed</li><li>Includes Sync</li></ul></div>
      <div class="plan"><h3>Editorial</h3><div class="price">$25<small> / month</small></div><p class="pitch">For working with editors and readers.</p><ul><li>Collaborators on a project</li><li>Import an editor's review: redlines and comments back from Word</li><li>Beta-reader rounds, focus and audit passes</li><li>Includes Sync</li></ul></div>
    </div>'''

WAITLIST = '''<div class="cta-band">
      <h2>Be first to write in it.</h2>
      <p>Write to us and we will send the macOS build when it is ready. One email, then nothing until there is something to say.</p>
      <a class="btn" href="mailto:hello@oakfall.app?subject=Oakfall%20for%20macOS">Email hello@oakfall.app</a>
      <p style="font-size:.9rem">Or try the desk now, in your browser: <a href="preview/">oakfall.app/preview</a></p>
    </div>'''

HOME = f'''  <div class="banner" data-gall="Hello. I live in the l. I'll walk you down.">
    <div class="wrap">
      <div class="sheet">
        <div class="slug"><span>OAKFALL · DRAFT 3</span><span>p. 1</span></div>
        <h1 class="typed">Write the <span class="word" data-words="novel.|memoir.|screenplay.|thesis.|long thing.">novel.</span><span class="caret" aria-hidden="true"></span><span class="second">Keep every draft.</span></h1>
        <p class="lede">Oakfall is a writing studio for work that outgrows one file: a binder, snapshots you can compare side by side, your cast and places, maps and threads, over plain Markdown you own.</p>
        <div class="ctas"><a class="btn primary" href="download.html">{I["apple"]}Download for macOS <span class="soon">Coming soon</span></a><a class="btn" href="preview/">Try the desk in your browser</a></div>
        <p class="note">Free to write in. Windows, Linux, iPad and phone follow from the same app.</p>
      </div>
      <a href="preview/" class="window" aria-label="Open the desk in your browser"><img src="assets/shots/desk-light.webp" data-light="assets/shots/desk-light.webp" data-dark="assets/shots/desk-dark.webp" width="1440" height="900" alt="The Oakfall desk: the binder of the demo novel Harrowmere on the left, the scene The House on the page, the inspector on the right."></a>
      <div class="facts"><span>Plain Markdown files</span><span>Works offline</span><span>No account to write</span><span>Open spec, Apache-2.0</span></div>
    </div>
  </div>

  <section class="wrap" data-gall="This is the snapshot I keep for you. Try the rewrite.">
    <div class="head"><span class="eyebrow">Snapshots</span><h2>Try the risky rewrite. Keep the old one.</h2><p class="lede">Name a snapshot before a big edit. Later, open it beside the live text with every change tinted at the word level, and pull back a sentence or the whole scene. Restoring snapshots the current version first, so nothing is ever the last copy.</p></div>
    {COMPARE}
  </section>

  <section class="wrap" data-gall="Everything has a place on the desk. Turn off what you don't use.">
    <div class="head"><span class="eyebrow">The desk</span><h2>Everything a long work needs, in one place.</h2></div>
    <div class="cards">
      <a class="card" href="features.html#binder"><div class="ic">{I["binder"]}</div><h3>The binder</h3><p>Parts, chapters and scenes in manuscript order, with word counts and status on every row.</p><span class="more">More</span></a>
      <a class="card" href="features.html#cast"><div class="ic">{I["cast"]}</div><h3>Cast and places</h3><p>A character is a note; its appearances are the scenes that name it. The cast panel reads the book for you.</p><span class="more">More</span></a>
      <a class="card" href="features.html#maps"><div class="ic">{I["map"]}</div><h3>Maps</h3><p>Any image becomes a map. Pin places, draw roads and rivers, click through to the scenes.</p><span class="more">More</span></a>
    </div>
  </section>

  <section class="wrap" data-gall="Your files stay yours. I just know where they are.">
    <div class="head"><span class="eyebrow">Why it is different</span><h2>Your manuscript is never held hostage.</h2></div>
    <div class="nums">
      <div class="num"><b>0</b><small>Proprietary formats</small><p>A project is a folder of Markdown with a little frontmatter. Open it in any editor; read it in fifty years.</p></div>
      <div class="num"><b>1</b><small>Folder per project</small><p>Snapshots are plain copies or ordinary git commits. Uninstall Oakfall and every scene is still there.</p></div>
      <div class="num"><b>$0</b><small>To write a whole novel</small><p>The whole desk is free. Pay only for sync, hosted Gall, or the editorial pack.</p></div>
    </div>
  </section>

  <section class="wrap" data-gall="That's me. I dress for the season.">
    <div class="gall-grid">
      <div><div class="head" style="margin-bottom:0"><span class="eyebrow">Meet Gall</span><h2>Every studio has someone who knows where things are.</h2><p class="lede">Ask where someone was last seen, what changed since a snapshot, which scenes still mention the thing you just cut. Gall answers from your files and never writes your prose.</p></div>{CHAT}</div>
      <div class="outfits" aria-label="Gall's outfits">{outfit_cards()}</div>
    </div>
  </section>

  <section class="wrap" data-gall="Bring what you already have. I'll sort it.">
    <div class="head"><span class="eyebrow">Compatibility</span><h2>Bring your work in. Take it anywhere.</h2><p class="lede">Oakfall reads and writes ordinary files, so the work you have today comes with you and nothing is locked in tomorrow.</p></div>
    {FORMATS}
  </section>

  <section class="wrap" data-gall="Free to write in. Really.">
    <div class="head"><span class="eyebrow">Pricing</span><h2>Free to write in. Pay for what you add.</h2></div>
    <div class="strip"><div class="tiers"><div><b>Free</b><small>The whole desk</small></div><div><b>$5</b><small>Sync</small></div><div><b>$20</b><small>Gall, hosted</small></div><div><b>$25</b><small>Editorial</small></div></div><a class="btn" href="pricing.html">See the plans</a></div>
    {WAITLIST}
  </section>'''

FEATURES = f'''  <div class="wrap page-head"><span class="eyebrow">Features</span><h1>A desk built for the long work.</h1><p class="lede">Every part is a module you can turn off. They all read the same notes, so nothing is stranded when you do.</p></div>
  <section class="wrap" style="padding-top:48px">
    <div class="cards">
      <div class="card" id="binder"><div class="ic">{I["binder"]}</div><h3>The binder</h3><p>Parts, chapters and scenes in manuscript order, with a word count and status on every row. Drag to reorder; the order lives in the file names, so nothing hides in a database.</p></div>
      <div class="card" id="inspector"><div class="ic">{I["inspector"]}</div><h3>The inspector</h3><p>Synopsis, label, status, story date, notes and snapshots for the scene you are on, beside the page instead of in a dialog.</p></div>
      <div class="card" id="snapshots"><div class="ic">{I["snap"]}</div><h3>Snapshots and compare</h3><p>Named versions per scene. Compare any two side by side at the word level and pull back exactly what you want.</p></div>
      <div class="card" id="cast"><div class="ic">{I["cast"]}</div><h3>Cast and places</h3><p>A character is a note; its appearances are the scenes that link to it or name it. Places work the same way, and both show across the book in order.</p></div>
      <div class="card" id="maps"><div class="ic">{I["map"]}</div><h3>Maps</h3><p>Any image becomes a map: a drawn world, a town plan, the floor plan of the house. Pin places, draw roads and rivers, click through to scenes.</p></div>
      <div class="card" id="threads"><div class="ic">{I["threads"]}</div><h3>Threads and timeline</h3><p>Cards by thread, by label or by story date, from the same synopsis, label and date fields. Rearrange without retyping anything.</p></div>
      <div class="card" id="look"><div class="ic">{I["look"]}</div><h3>Your desk, your look</h3><p>Light or dark, Desk or Classic, five looks, the page's paper and type size. Focus clears everything but the page.</p></div>
      <div class="card" id="compile"><div class="ic">{I["compile"]}</div><h3>Compile</h3><p>Presets for manuscript format, paperback and ebook, to PDF, EPUB or DOCX, with your files untouched.</p></div>
      <div class="card"><div class="ic">{I["inspector"]}</div><h3>Gall in the margin</h3><p>Lookups across the book with no model at all, and with a model, answers about what changed and what depends on what. <a href="gall.html">Meet Gall</a>.</p></div>
    </div>
  </section>
  <section class="wrap"><div class="head"><span class="eyebrow">Snapshots</span><h2>Compare is the feature you will use most.</h2></div>{COMPARE}</section>
  <section class="wrap" id="compatibility"><div class="head"><span class="eyebrow">Compatibility</span><h2>Bring your work in. Take it anywhere.</h2></div>{FORMATS}
    <pre>go install github.com/oakfall/scrivener-to-obsidian/cmd/scriv2obsidian@latest
scriv2obsidian convert -out ~/Writing -git Novel.scriv</pre></section>
  <section class="wrap"><div class="head"><span class="eyebrow">Plainly</span><h2>What Oakfall does not do.</h2></div>
    <ul class="nots">
      <li><b>It does not write for you.</b>Gall answers, finds, checks and proposes edits you accept. The prose is yours.</li>
      <li><b>It does not need an account.</b>Writing, snapshots and every module work without signing in. Only sync needs one.</li>
      <li><b>It does not phone home.</b>No telemetry. Gall sends your manuscript nowhere you did not point him.</li>
      <li><b>It does not lock your files.</b>No database, no proprietary package. Markdown, frontmatter and images in folders.</li>
    </ul></section>'''

STATES = [("Idle", None), ("Smile", "smile"), ("Thinking", "think"), ("Delighted", "grin")]


def state_svg(kind):
    b = body("var(--card)")
    if kind == "smile":
        b = b.replace('<circle cx="50" cy="52" r="3.2" fill="var(--card)"/><path d="M50 56 V 80"', '<path d="M45 42 Q 50 47 55 42" stroke="var(--card)" stroke-width="2.2" stroke-linecap="round" fill="none"/><path d="M50 58 V 80"')
    elif kind == "think":
        b = b.replace('cy="32.6" r="1.8"', 'cy="30.4" r="1.8"').replace('<circle cx="50" cy="52" r="3.2"', '<circle cx="50" cy="45" r="2.6"')
    elif kind == "grin":
        b = re.sub(r'<g class="eyes">.*?</g>', '<g class="eyes"><path d="M38 33 Q 42 28 46 33 M54 33 Q 58 28 62 33" stroke="var(--card)" stroke-width="2.4" stroke-linecap="round" fill="none"/></g>', b, flags=re.S)
        b = b.replace('<circle cx="50" cy="52" r="3.2" fill="var(--card)"/><path d="M50 56 V 80"', '<path d="M43 42 Q 50 50 57 42 Z" fill="var(--card)"/><path d="M50 58 V 80"')
    return f'<svg viewBox="-14 -22 128 128" aria-hidden="true">{b}</svg>'


GALL_PAGE = f'''  <div class="wrap page-head"><span class="eyebrow">Gall</span><h1>Every studio has someone who knows where things are.</h1><p class="lede">Gall lives in the l of Oakfall. He steps out when you need him, knows the book through your files and their history, and stays out of your prose.</p></div>
  <section class="wrap" style="padding-top:48px"><div class="gall-grid"><div>
      <div class="head" style="margin-bottom:0"><h2>Ask him anything about the book.</h2><p class="lede">Where someone was last seen, what changed since a snapshot, which scenes still mention what you cut, whether a synopsis still matches its scene. Anything he changes lands as an ordinary edit you can undo.</p></div>{CHAT}</div>
      <div class="states" aria-label="Gall's moods">{"".join(f'<div class="outfit"><span class="gall">{state_svg(k)}</span>{n}</div>' for n, k in STATES)}</div></div></section>
  <section class="wrap"><div class="head"><span class="eyebrow">Half free, half hosted</span><h2>Half of Gall needs no model at all.</h2><p class="lede">Last seen, set at, who is in a scene, which places have no scene yet, how long a chapter is: those are lookups. They work offline, ship with the free app, and are open source. The half that reads your prose runs on your own key or a local model for free, or on our hosted models with the Gall plan.</p></div></section>
  <section class="wrap"><div class="head"><span class="eyebrow">Outfits</span><h2>He dresses for the season.</h2><p class="lede">A hat and wand for the tour, spectacles while he reads, a scarf in winter, a blossom in spring, shades in summer, an acorn cap in autumn, and a party hat the day you finish a draft. Pick his colour in Settings.</p></div><div class="outfits" style="grid-template-columns:repeat(8,minmax(0,1fr))">{outfit_cards()}</div></section>
  <section class="wrap"><div class="head"><span class="eyebrow">Promises</span><h2>What Gall will not do.</h2></div>
    <ul class="nots"><li><b>Write your prose.</b>He answers, finds, checks and proposes. You write.</li><li><b>Turn on by himself.</b>He is off until you switch him on.</li><li><b>Send your book anywhere you did not choose.</b>Your key, your local model, or our hosted models, and nothing else.</li><li><b>Report back.</b>No telemetry, from Gall or from Oakfall.</li></ul></section>'''

PRICING = f'''  <div class="wrap page-head"><span class="eyebrow">Pricing</span><h1>Free to write in. Pay for what you add.</h1><p class="lede">The whole desk is free. Each plan adds one thing, and every paid plan includes sync. Stop paying and every file stays exactly where it is.</p></div>
  <section class="wrap" style="padding-top:48px">{PLANS}</section>
  <section class="wrap"><div class="head"><span class="eyebrow">Questions</span><h2>Before you ask.</h2></div>
    <ul class="nots">
      <li><b>Can I write a whole book for free?</b>Yes. Every module, every look, snapshots and compare. Paid plans add sync, hosted Gall, or editorial tools.</li>
      <li><b>What happens if I stop paying?</b>Your files stay on your disk exactly as they are. Sync stops; nothing is deleted.</li>
      <li><b>Do I need the Gall plan to use Gall?</b>No. His lookups are free and offline, and you can bring your own model key or run a local model.</li>
      <li><b>Who is Editorial for?</b>Writers working with an editor, a co-author, or beta readers: shared projects, reviews back from Word, reader rounds.</li>
    </ul></section>
  <section class="wrap">{WAITLIST}</section>'''

DOWNLOAD = f'''  <div class="wrap page-head"><span class="eyebrow">Download</span><h1>Oakfall for macOS is coming soon.</h1><p class="lede">The app is in development and macOS comes first. Windows, Linux, iPad and phone follow from the same app. The Obsidian plugin and the importer are open source and usable today.</p></div>
  <section class="wrap" style="padding-top:48px">
    <div class="plats">
      <span class="plat">{I["apple"]} macOS <span class="state">Coming soon</span></span>
      <span class="plat">Windows <span class="state">Later</span></span>
      <span class="plat">Linux <span class="state">Later</span></span>
      <span class="plat">iPad <span class="state">Later</span></span>
      <span class="plat">iPhone and Android <span class="state">Later</span></span>
      <a class="plat" href="https://github.com/oakfall/oakfall">Obsidian plugin <span class="state now">Today</span></a>
      <a class="plat" href="https://github.com/oakfall/scrivener-to-obsidian">Importer <span class="state now">Today</span></a>
    </div>
    <a href="preview/" class="window" aria-label="Open the desk in your browser"><img src="assets/shots/desk-light.webp" data-light="assets/shots/desk-light.webp" data-dark="assets/shots/desk-dark.webp" width="1440" height="900" alt="The Oakfall desk."></a>
    {WAITLIST}
  </section>'''


def faq_page():
    body_html = open(os.path.join(ROOT, "hack", "faq-body.html")).read()
    return f'''  <div class="wrap page-head faq-page"><span class="eyebrow">FAQ</span><h1>Questions from the first week.</h1></div>
  <section class="wrap" style="padding-top:24px">
{body_html}
  </section>'''


PAGES = [
    ("index.html", "Oakfall, the writing studio", "A writing studio for work that outgrows one file: binder, snapshots with side-by-side compare, cast and places, maps, and Gall in the margin. Plain Markdown you own.", HOME),
    ("features.html", "Features · Oakfall", "The binder, inspector, snapshots and compare, cast and places, maps, threads and timeline, looks, compile, and what Oakfall reads and writes.", FEATURES),
    ("gall.html", "Gall · Oakfall", "Gall lives in the margin and knows where everything is in your book. He answers, finds and checks, and never writes your prose.", GALL_PAGE),
    ("pricing.html", "Pricing · Oakfall", "Free to write in. Sync $5 a month, hosted Gall $20, Editorial $25.", PRICING),
    ("download.html", "Download · Oakfall", "Oakfall for macOS is coming soon. Windows, Linux, iPad and phone follow.", DOWNLOAD),
    ("faq.html", "FAQ · Oakfall", "Questions writers ask after importing a project.", None),
]

for page, title, desc, main in PAGES:
    html = shell(page, title, desc, main if main is not None else faq_page())
    open(os.path.join(ROOT, page), "w").write(html)
    print("wrote", page, len(html) // 1024, "KB")
