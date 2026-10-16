#!/usr/bin/env python3
"""
Chouette score sheet generator (ReportLab).

    python chouette_sheet.py                  # the standard sheet -> chouette_sheet.pdf
    python chouette_sheet.py large            # a named size from PRESETS
    python chouette_sheet.py --players 7 --rows 14
    python chouette_sheet.py large --sheet-only   # page 1 only, no instructions

Page 1 = blank sheet.  Page 2 = instructions + worked example.

Line weights and the single grey tint are set in the CONFIG block.
"""
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Frame, Spacer, Flowable
from reportlab.lib import colors
import argparse
import os

# ----------------------------- CONFIG ---------------------------------
OUTFILE         = "chouette_sheet.pdf"
PAGESIZE        = letter
MARGIN          = 30
TITLE           = "Chouette Score Sheet"
CHK_W           = 24

# Sheet sizes.  Choose by name on the command line, or override with --players / --rows.
#   players  = columns for players        rows = total rows, including the opening-totals row
#   notes_w  = width of the Notes column (the player columns share what remains)
# Row height is NOT set here: it is worked out so the rows exactly fill the page, which
# means fewer rows automatically gives bigger boxes.  Column width works the same way.
PRESETS = {
    "standard": dict(players=10, rows=20, notes_w=62),
    "large":    dict(players=8,  rows=16, notes_w=70),
    "jumbo":    dict(players=6,  rows=12, notes_w=90),
}
DEFAULT_PRESET  = "standard"
HDR_RATIO       = 30 / 32        # name-header height as a fraction of the row height
OPTIONS         = ["Jacoby waived", "Beavers", "Partners", "Extras"]
INCLUDE_INSTRUCTIONS = True

LINE_THIN       = 0.4            # row lines, column lines, delta-box outlines
LINE_HEAVY      = 0.8            # outer frame and the rule under the header
LINE_FIELD      = 0.5            # underlines of fill-in fields
LINE_BOX        = 0.7            # option checkboxes
GRID            = 0.35           # grey level of row lines and delta-box outlines
TINT            = 0.95           # every grey area (delta boxes, check column); 1 = white
DELTA_W_FRAC    = 0.56
DELTA_H_FRAC    = 0.42

# Page 1 layout (points)
TITLE_SIZE      = 20
TITLE_DROP      = 18             # title baseline, below the top margin
STAKE_W         = 60             # width of the Stake field, label included
OPTIONS_DROP    = 48             # Options baseline, below the top margin
OPTIONS_INDENT  = 46             # first checkbox, from the left margin
TABLE_GAP       = 12             # Options baseline down to the top of the grid

# Page 2 layout (points).  Page 2 is a flowing document: everything between the
# margins is one list of paragraphs, spacers and the example table, so editing
# the text just moves what follows.  There are no coordinates to recompute.
TEXT_RIGHT_INDENT = 50           # keeps the instruction text a little narrower than the page
EXAMPLE_GAP     = 24             # space above the "Worked example" heading
EXAMPLE_TEXT_GAP = 10            # space between the example table and its explanation
EXAMPLE_COL_W   = 56             # width of each player column in the example
EXAMPLE_NOTES_W = 62
EXAMPLE_ROW_H   = 32             # the worked example keeps its own fixed cell size
EXAMPLE_HDR_H   = 30
EXAMPLE_SIDE_GAP = 14            # gap between the example table and the rotation shown beside it
EXAMPLE_SIDE_SIZE = 8            # type size of the rotation shown beside the example
# ----------------------------------------------------------------------

W, H = PAGESIZE
L, R = MARGIN, W - MARGIN
REG, BOLD, ITAL = "Helvetica", "Helvetica-Bold", "Helvetica-Oblique"
grey = colors.Color(TINT, TINT, TINT)
grid = colors.Color(GRID, GRID, GRID)


def field(c, x, y, label, width, size=9):
    """Label at x, then an underline out to x + width."""
    c.setFont(REG, size); c.setFillColor(colors.black)
    c.drawString(x, y, label)
    c.setLineWidth(LINE_FIELD); c.setStrokeColor(colors.black)
    c.line(x + c.stringWidth(label, REG, size) + 3, y - 1.5, x + width, y - 1.5)
    return x + width


def checkmark(c, cx, cy, size=6):
    """Vector check mark centred at (cx, cy); no font needed."""
    c.setStrokeColor(colors.black); c.setLineWidth(1.5); c.setLineCap(1)
    p = c.beginPath()
    p.moveTo(cx - size * .5, cy)
    p.lineTo(cx - size * .12, cy - size * .45)
    p.lineTo(cx + size * .55, cy + size * .5)
    c.drawPath(p, stroke=1, fill=0)


def checkbox(c, x, y, label, size=9):
    c.setLineWidth(LINE_BOX); c.setStrokeColor(colors.black)
    c.rect(x, y - 1, 8, 8)
    c.setFont(REG, size); c.drawString(x + 12, y, label)
    return x + 12 + c.stringWidth(label, REG, size) + 14


def draw_table(c, x0, ytop, ncols, cw, nrows, row_h, hdr_h, notes_w, names=None, data=None, fs=9):
    """Header + nrows rows.  data = list of dicts {cells:[(delta,total)], chk, note}."""
    dw, dh = cw * DELTA_W_FRAC, row_h * DELTA_H_FRAC
    chk_x = x0 + ncols * cw
    notes_x = chk_x + CHK_W
    xr = notes_x + notes_w
    y_hdr = ytop - hdr_h
    y_bot = y_hdr - nrows * row_h

    # grey areas
    c.setFillColor(grey)
    c.rect(chk_x, y_bot, CHK_W, nrows * row_h, stroke=0, fill=1)
    for r in range(nrows):
        yy = y_hdr - (r + 1) * row_h
        for p in range(ncols):
            c.rect(x0 + p * cw, yy + row_h - dh, dw, dh, stroke=0, fill=1)

    # lines: grey rows and delta boxes, black columns, heavier frame and header rule
    c.setStrokeColor(grid); c.setLineWidth(LINE_THIN)
    for r in range(nrows + 1):
        c.line(x0, y_hdr - r * row_h, xr, y_hdr - r * row_h)
    for r in range(nrows):
        yy = y_hdr - (r + 1) * row_h
        for p in range(ncols):
            c.rect(x0 + p * cw, yy + row_h - dh, dw, dh)
    c.setStrokeColor(colors.black)
    for x in [x0 + p * cw for p in range(ncols + 1)] + [notes_x, xr]:
        c.line(x, ytop, x, y_bot)
    c.setLineWidth(LINE_HEAVY)
    c.rect(x0, y_bot, xr - x0, ytop - y_bot)
    c.line(x0, y_hdr, xr, y_hdr)

    # header text
    c.setFillColor(colors.black)
    mid = y_hdr + hdr_h / 2 - 3
    if names:
        c.setFont(BOLD, 9)
        for p, n in enumerate(names):
            c.drawCentredString(x0 + p * cw + cw / 2, mid, n)
    checkmark(c, chk_x + CHK_W / 2, mid + 3, 5)
    c.setFont(BOLD, 8); c.drawCentredString(notes_x + notes_w / 2, mid, "Notes")

    # data
    for r, row in enumerate(data or []):
        yy = y_hdr - (r + 1) * row_h
        for p, (d, t) in enumerate(row['cells']):
            bx = x0 + p * cw
            if d:
                c.setFont(REG, fs - 1.5)
                c.drawCentredString(bx + dw / 2, yy + row_h - dh / 2 - 2.5, d)
            c.setFont(BOLD, fs + 1)
            c.drawCentredString(bx + cw / 2, yy + 5, t)
        if row.get('chk'):
            checkmark(c, chk_x + CHK_W / 2, yy + row_h / 2, 6)
        c.setFont(ITAL, 6.8)
        for i, ln in enumerate(row.get('note', "").split("\n")):
            c.drawString(notes_x + 4, yy + row_h / 2 + 4 - i * 8, ln)


def page1(c, players, rows, notes_w):
    top = H - MARGIN
    c.setFillColor(colors.black)
    c.setFont(BOLD, TITLE_SIZE); c.drawString(L, top - TITLE_DROP, TITLE)
    field(c, R - STAKE_W, top - TITLE_DROP, "Stake:", STAKE_W)    # ends at the right margin

    y = top - OPTIONS_DROP
    c.setFont(BOLD, 9); c.drawString(L, y, "Options:")
    x = L + OPTIONS_INDENT
    for lab in OPTIONS:
        x = checkbox(c, x, y, lab)
    field(c, x, y, "Other", R - x)

    cw = (R - L - CHK_W - notes_w) / players
    y_top = y - TABLE_GAP
    row_h = (y_top - MARGIN) / (rows + HDR_RATIO)       # rows + header fill the page exactly
    draw_table(c, L, y_top, players, cw, rows, row_h, row_h * HDR_RATIO, notes_w)


class ExampleTable(Flowable):
    """The worked-example grid as a flowable: it reports its own height."""
    def __init__(self, ncols, cw, notes_w, names, data, side=None):
        super().__init__()
        self.ncols, self.cw, self.notes_w = ncols, cw, notes_w
        self.names, self.data = names, data
        self.side = side or []
        self.width = ncols * cw + CHK_W + notes_w
        self.height = EXAMPLE_HDR_H + len(data) * EXAMPLE_ROW_H

    def wrap(self, avail_w, avail_h):
        return self.width, self.height

    def draw(self):      # origin is the flowable's lower-left corner
        draw_table(self.canv, 0, self.height, self.ncols, self.cw, len(self.data),
                   EXAMPLE_ROW_H, EXAMPLE_HDR_H, self.notes_w, names=self.names, data=self.data)
        if self.side:        # one line of text beside each row, to the right of the table
            c, x = self.canv, self.width + EXAMPLE_SIDE_GAP
            c.setFillColor(colors.black)
            c.setFont(REG, EXAMPLE_SIDE_SIZE)
            for r, text in enumerate(self.side):     # baseline offset keeps the text centered on the row
                c.drawString(x, self.height - EXAMPLE_HDR_H - (r + 0.5) * EXAMPLE_ROW_H - EXAMPLE_SIDE_SIZE * 0.33, text)


def page2(c):
    title = ParagraphStyle("t", fontName=BOLD, fontSize=16, leading=20, spaceAfter=6)
    body = ParagraphStyle("b", fontName=REG, fontSize=8.8, leading=11.2, spaceAfter=3.5,
                          rightIndent=TEXT_RIGHT_INDENT)
    head = ParagraphStyle("h", fontName=BOLD, fontSize=9.8, leading=12, spaceBefore=4, spaceAfter=2)
    P = lambda t: Paragraph(t, body)
    Hh = lambda t: Paragraph(t, head)

    story = [
        Paragraph("Using the chouette score sheet", title),
        Hh("Starting"),
        P("Write the per-point stake at the top and tick the options in effect. The Jacoby rule "
          "applies unless waived. Write each player's name at the head of a column, in any order; column order "
          "has nothing to do with rotation order.  See the separate Chouette Rules for how to set up and maintain "
          "the rotation during the chouette. "
          "Blank columns can accommodate newcomers.  "),
        Hh("Scoring a game"),
        P("The Box's game against each opponent is scored "
          "separately according to that individual cube: the cube value finally held, or passed, times 1, 2 or 3 "
          "for a single, gammon or backgammon, as the Jacoby rule allows."),
        P("In each opponent's small box write what that opponent won (+) or lost (&minus;), "
          "in points. In the Box's small box write the total of what he won (+) or lost (&minus;). "
          "Then, in the large area of each cell, "
          "write the new total: the previous total plus the figure in the small box."),
        P("<b>Check</b>: Add the small-box figures across the row. They must sum to zero. Add the totals in the boxes "
          "across the row.  They must sum to zero also.  Check the box and start the next game."),
        Hh("Entering and leaving"),
        P("A new player entering takes a blank column and starts at 0 on the row where he joins.  Note his entry in the column at the right. "),
        P("A player who steps away temporarily keeps his column and his total.  For all the games he is away, record 0 in the small "
          "box and carry his total down."),
        P("A player who leaves for good cashes out.  Record the amount he pays (+) or receives (&minus;) in "
          "his small box, and record the amount each player pays him (+) or receives from him (&minus;) in "
          "the appropriate column.  Total up and Check as above: the rows sum to zero, and the cashed-out player "
          "has a zero total also.  Note his exit in the column at the right."
          ),
        Hh("Finishing"),
        P("At the end of the chouette, each player cashes out as described above.  The total of each player "
          "is now 0.  Wait for the next chouette."),
    ]

    # ---- worked example: table, then a line of explanation per row --------
    data = [
        dict(cells=[("+4", "4"), ("-2", "-2"), ("-1", "-1"), ("-1", "-1")], chk=True,
             note="Start of chouette."),
        dict(cells=[("-2", "2"), ("+1", "-1"), ("+2", "1"), ("-1", "-2")], chk=True,
             note=""),
        dict(cells=[("0", "2"), ("+1", "0"), ("-1", "0"), ("0", "-2")], chk=True,
             note="Bob is out."),
        dict(cells=[("-1", "1"), ("", ""), ("-1", "-1"), ("+2", "0")], chk=True,
             note=""),
        dict(cells=[("-1", "0"), ("", ""), ("+1", "0"), ("0", "0")], chk=True,
             note="End of chouette."),
    ]
    rotation = [                          # order at the start of each line: Box, Captain, Crew...
        "Anne / Bob / Caleb / Daria",
        "Anne / Caleb / Daria / Bob",
        "Caleb / Daria / Bob / Anne",
        "Caleb / Daria / Anne",
        "",
    ]
    table = ExampleTable(4, EXAMPLE_COL_W, EXAMPLE_NOTES_W,
                         ["Anne", "Bob", "Caleb", "Daria"], data, side=rotation)
    ns = ParagraphStyle("n", fontName=REG, fontSize=8.4, leading=10.6, spaceAfter=3,
                        rightIndent=(R - L) - table.width)     # text is as wide as the table
    N = lambda t: Paragraph(t, ns)

    story += [
        Spacer(1, EXAMPLE_GAP),
        Hh("Worked example"),
        Spacer(1, 4),
        table,
        Spacer(1, EXAMPLE_TEXT_GAP),
        N("<b>Line 1.</b> Anne, in the Box, beats Bob (Captain) with the cube at 2, and beats Caleb and Daria with the cube at 1. "
          "Her small box shows +4, and the others show &minus;2, &minus;1 and &minus;1."),
        N("<b>Line 2.</b> Caleb is now Captain, Bob is Crew. Caleb wins with his cube at 2 and Bob with his at 1; Daria had already "
          "passed Anne's double, so Anne wins 1 from Daria. Anne's net is &minus;2 &minus;1 +1 = &minus;2. "
          "Each row's small boxes sum to 0, and the totals do too."),
        N("<b>Line 3.</b> Bob leaves the chouette and pays 1 point to Caleb. His small box shows +1, bringing his "
          "total to 0; Caleb's shows &minus;1, bringing his to 0. The others record 0 and carry their totals down."),
        N("<b>Line 4.</b> Caleb, as Captain, beat the Box in Line 2, so he is now the Box; Daria is Captain and Anne is Crew. "
          "Caleb doubles them both. Anne passes, so Caleb wins 1 from her. Daria takes and wins a single with the cube at 2, "
          "so Caleb loses 2 to her. His net is &minus;2 +1 = &minus;1. Bob's column is closed and left blank."),
        N("<b>Line 5.</b> Everybody cashes out. Caleb pays 1 point to Anne; Daria, at zero, neither pays nor receives. "
          "Every total is now 0."),
    ]

    frame = Frame(L, MARGIN, R - L, H - 2 * MARGIN,
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    frame.addFromList(story, c)
    assert not story, "page 2 overflowed: trim text or spacing, or reduce MARGIN"


def main():
    ap = argparse.ArgumentParser(description="Generate the chouette score sheet.")
    ap.add_argument("preset", nargs="?", default=DEFAULT_PRESET, choices=sorted(PRESETS),
                    help="named size (default: %s)" % DEFAULT_PRESET)
    ap.add_argument("--players", type=int, help="override the number of player columns")
    ap.add_argument("--rows", type=int, help="override the number of rows")
    ap.add_argument("--notes", type=int, help="override the Notes column width (points)")
    ap.add_argument("--sheet-only", action="store_true", help="page 1 only; omit the instructions")
    ap.add_argument("--out", help="output file name")
    a = ap.parse_args()

    size = dict(PRESETS[a.preset])
    for key, val in (("players", a.players), ("rows", a.rows), ("notes_w", a.notes)):
        if val is not None:
            size[key] = val

    out = a.out
    if not out:                          # the standard sheet keeps the plain name
        stem, ext = os.path.splitext(OUTFILE)
        standard = size == PRESETS[DEFAULT_PRESET]
        out = OUTFILE if standard else "%s_%dx%d%s" % (stem, size["players"], size["rows"], ext)

    c = canvas.Canvas(out, pagesize=PAGESIZE)
    c.setTitle(TITLE)
    page1(c, size["players"], size["rows"], size["notes_w"])
    if INCLUDE_INSTRUCTIONS and not a.sheet_only:
        c.showPage(); page2(c)
    c.save()
    print("wrote", out)


if __name__ == "__main__":
    main()
