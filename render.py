#!/usr/bin/env python3
"""Draw the front page for Sunday 22 November 2026.

Build tool for the make.fun bounty news-image-20261122, "Sum up
22 November's world news in one image". It reads news.json — seven
headlines checked against reporting dated 22 November 2026 — and
draws a 1024x1024 newspaper front page with Pillow, writing entry.png
next to this script (override with the OUT environment variable).

This file is only the build tool. The graded entrypoint is main.py,
which copies the committed entry.png to /output/entry.png using the
standard library alone: the grader runs in a bare python:3.13-slim
container with no Pillow and no system fonts, so this renderer never
runs there.

Deterministic on purpose: no clock, no random numbers, no network,
fixed font files, so the same news.json always yields identical PNG
bytes.
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
EDGE = 48                      # side margin
PAPER = (248, 245, 238)        # newsprint off-white
INK = (17, 17, 17)             # near-black ink
RED = (185, 28, 28)            # accent red
GREY = (92, 88, 80)            # deck and footer grey
HAIRLINE = (200, 196, 186)     # hairline grey
WHITE = (255, 255, 255)

FONT_PATHS = ("/usr/share/fonts/truetype/liberation",
              "/usr/share/fonts/truetype/dejavu")


def find_font(names):
    """First font file that exists, searching the known font folders."""
    for folder in FONT_PATHS:
        for name in names:
            path = os.path.join(folder, name)
            if os.path.isfile(path):
                return path
    raise FileNotFoundError("no usable font among %r" % (names,))


SERIF_B = find_font(["LiberationSerif-Bold.ttf", "DejaVuSerif-Bold.ttf"])
SERIF_R = find_font(["LiberationSerif-Regular.ttf", "DejaVuSerif.ttf"])
SANS_B = find_font(["LiberationSans-Bold.ttf", "DejaVuSans-Bold.ttf"])
SANS_R = find_font(["LiberationSans-Regular.ttf", "DejaVuSans.ttf"])


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; every returned line fits inside width pixels."""
    out, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


class Page:
    """One 1024x1024 front page, drawn section by section."""

    def __init__(self, news):
        self.news = news
        self.img = Image.new("RGB", (W, H), PAPER)
        self.d = ImageDraw.Draw(self.img)
        self.x0 = EDGE
        self.x1 = W - EDGE
        self.span = self.x1 - self.x0

    def hline(self, y, colour, thick):
        self.d.line([(self.x0, y), (self.x1, y)], fill=colour, width=thick)

    def put_lines(self, lines, x, y, fnt, colour, step):
        """Draw pre-wrapped lines from (x, y); return the y below them."""
        for line in lines:
            self.d.text((x, y), line, font=fnt, fill=colour, anchor="la")
            y += step
        return y

    def nameplate(self, y):
        d = self.d
        d.text((W // 2, y), self.news["masthead"],
               font=font(SERIF_B, 92), fill=INK, anchor="ma")
        y += 96
        self.hline(y, INK, 3)
        y += 13
        d.text((self.x0, y), self.news["dateline_left"],
               font=font(SANS_B, 20), fill=INK, anchor="la")
        d.text((self.x1, y), self.news["dateline_right"],
               font=font(SANS_B, 20), fill=RED, anchor="ra")
        y += 29
        self.hline(y, RED, 4)
        return y + 24

    def lead_story(self, y):
        d = self.d
        lead = self.news["lead"]
        d.text((self.x0, y), lead["kicker"],
               font=font(SANS_B, 19), fill=RED, anchor="la")
        y += 29
        head = font(SERIF_B, 44)
        y = self.put_lines(wrap(d, lead["headline"], head, self.span),
                           self.x0, y, head, INK, 52)
        y += 6
        deck = font(SERIF_R, 23)
        y = self.put_lines(wrap(d, lead["deck"], deck, self.span),
                           self.x0, y, deck, INK, 30)
        y += 20
        self.hline(y, INK, 2)
        return y + 22

    def story_size(self, story, width):
        """Height of one grid story: number row + headline + deck."""
        body = width - 40
        heads = wrap(self.d, story["headline"], font(SERIF_B, 24), body)
        decks = wrap(self.d, story["deck"], font(SERIF_R, 18), body)
        return 25 + len(heads) * 29 + 3 + len(decks) * 23

    def draw_story(self, item, number, x, y, width):
        """Draw one numbered grid story at (x, y); return its height."""
        d = self.d
        start = y
        d.ellipse([x, y + 1, x + 28, y + 29], fill=RED)
        d.text((x + 14, y + 15), str(number),
               font=font(SANS_B, 18), fill=WHITE, anchor="mm")
        tx, tw = x + 40, width - 40
        d.text((tx, y), item["kicker"], font=font(SANS_B, 15),
               fill=RED, anchor="la")
        y += 25
        head = font(SERIF_B, 24)
        y = self.put_lines(wrap(d, item["headline"], head, tw),
                           tx, y, head, INK, 29)
        y += 3
        deck = font(SERIF_R, 18)
        y = self.put_lines(wrap(d, item["deck"], deck, tw),
                           tx, y, deck, GREY, 23)
        return y - start

    def grid(self, y):
        d = self.d
        gap_x = 36
        col = (self.span - gap_x) // 2
        # Stop the grid a little above the footer rule so the last
        # deck line never sits on it.
        foot_y = H - 92
        stories = self.news["stories"]
        # A row is as tall as its taller story. Measure all three rows
        # first, then spread any leftover space evenly between rows so
        # the grid fills down to the footer instead of stopping short.
        heights = []
        for r in range(3):
            pair = stories[r * 2:(r + 1) * 2]
            heights.append(max(self.story_size(s, col) for s in pair))
        slack = max(0, (foot_y - y) - (sum(heights) + 2 * 26))
        gap = 26 + slack // 2
        for r in range(3):
            for i, item in enumerate(stories[r * 2:(r + 1) * 2]):
                cx = self.x0 + i * (col + gap_x)
                self.draw_story(item, r * 2 + i + 1, cx, y, col)
            # Hairline between the two columns.
            mid = self.x0 + col + gap_x // 2
            d.line([(mid, y + 4), (mid, y + heights[r] - 4)],
                   fill=HAIRLINE, width=1)
            y += heights[r]
            if r < 2:
                d.line([(self.x0, y + gap // 2),
                        (self.x1, y + gap // 2)], fill=HAIRLINE, width=1)
                y += gap

    def footer(self):
        d = self.d
        y = H - 84
        self.hline(y, INK, 2)
        y += 12
        small = font(SANS_R, 14)
        for line in wrap(d, self.news["footer"], small, self.span):
            d.text((W // 2, y), line, font=small, fill=GREY, anchor="ma")
            y += 19
        y += 4
        d.text((W // 2, y), self.news["credit"], font=small,
               fill=GREY, anchor="ma")

    def render(self):
        y = self.nameplate(26)
        y = self.lead_story(y)
        self.grid(y)
        self.footer()
        return self.img


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "news.json"), encoding="utf-8") as fh:
        news = json.load(fh)
    out = os.environ.get("OUT", os.path.join(here, "entry.png"))
    folder = os.path.dirname(out)
    if folder:
        os.makedirs(folder, exist_ok=True)
    Page(news).render().save(out, format="PNG")
    print("wrote", out, os.path.getsize(out), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
