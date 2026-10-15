#!/usr/bin/env python3
"""
Chouette score sheet generator (ReportLab).  Run:  python chouette_sheet.py
Page 1 = blank sheet.  Page 2 = instructions + worked example.

Line weights and the single grey tint are set in the CONFIG block.
"""
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Frame
from reportlab.lib import colors

# ----------------------------- CONFIG ---------------------------------
OUTFILE         = "chouette_sheet.pdf"
PAGESIZE        = letter
MARGIN          = 30
TITLE           = "Chouette Score Sheet"
NUM_PLAYERS     = 10
NUM_ROWS        = 20             # total rows, including the opening-totals row
ROW_H           = 32
HDR_H           = 30
NOTES_W         = 62
CHK_W           = 24
OPTIONS         = ["Jacoby waived", "Beavers", "Extras", "Partners"]
INCLUDE_INSTRUCTIONS = True

LINE_THIN       = 0.4            # row lines, column lines, delta-box outlines
LINE_HEAVY      = 0.8            # outer frame and the rule under the header
LINE_FIELD      = 0.5            # underlines of fill-in fields
LINE_BOX        = 0.7            # option checkboxes
GRID            = 0.35           # grey level of row lines and delta-box outlines
TINT            = 0.95           # every grey area (delta boxes, check column); 1 = white
DELTA_W_FRAC    = 0.56
DELTA_H_FRAC    = 0.42
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


def draw_table(c, x0, ytop, ncols, cw, nrows, notes_w, names=None, data=None, fs=9):
    """Header + nrows rows.  data = list of dicts {cells:[(delta,total)], chk, note}."""
    dw, dh = cw * DELTA_W_FRAC, ROW_H * DELTA_H_FRAC
    chk_x = x0 + ncols * cw
    notes_x = chk_x + CHK_W
    xr = notes_x + notes_w
    y_hdr = ytop - HDR_H
    y_bot = y_hdr - nrows * ROW_H

    # grey areas
    c.setFillColor(grey)
    c.rect(chk_x, y_bot, CHK_W, nrows * ROW_H, stroke=0, fill=1)
    for r in range(nrows):
        yy = y_hdr - (r + 1) * ROW_H
        for p in range(ncols):
            c.rect(x0 + p * cw, yy + ROW_H - dh, dw, dh, stroke=0, fill=1)

    # lines: grey rows and delta boxes, black columns, heavier frame and header rule
    c.setStrokeColor(grid); c.setLineWidth(LINE_THIN)
    for r in range(nrows + 1):
        c.line(x0, y_hdr - r * ROW_H, xr, y_hdr - r * ROW_H)
    for r in range(nrows):
        yy = y_hdr - (r + 1) * ROW_H
        for p in range(ncols):
            c.rect(x0 + p * cw, yy + ROW_H - dh, dw, dh)
    c.setStrokeColor(colors.black)
    for x in [x0 + p * cw for p in range(ncols + 1)] + [notes_x, xr]:
        c.line(x, ytop, x, y_bot)
    c.setLineWidth(LINE_HEAVY)
    c.rect(x0, y_bot, xr - x0, ytop - y_bot)
    c.line(x0, y_hdr, xr, y_hdr)

    # header text
    c.setFillColor(colors.black)
    mid = y_hdr + HDR_H / 2 - 3
    if names:
        c.setFont(BOLD, 9)
        for p, n in enumerate(names):
            c.drawCentredString(x0 + p * cw + cw / 2, mid, n)
    checkmark(c, chk_x + CHK_W / 2, mid + 3, 5)
    c.setFont(BOLD, 8); c.drawCentredString(notes_x + notes_w / 2, mid, "Notes")

    # data
    for r, row in enumerate(data or []):
        yy = y_hdr - (r + 1) * ROW_H
        for p, (d, t) in enumerate(row['cells']):
            bx = x0 + p * cw
            if d:
                c.setFont(REG, fs - 1.5)
                c.drawCentredString(bx + dw / 2, yy + ROW_H - dh / 2 - 2.5, d)
            c.setFont(BOLD, fs + 1)
            c.drawCentredString(bx + cw / 2, yy + 5, t)
        if row.get('chk'):
            checkmark(c, chk_x + CHK_W / 2, yy + ROW_H / 2, 6)
        c.setFont(ITAL, 6.8)
        for i, ln in enumerate(row.get('note', "").split("\n")):
            c.drawString(notes_x + 4, yy + ROW_H / 2 + 4 - i * 8, ln)


def page1(c):
    top = H - MARGIN
    c.setFillColor(colors.black)
    c.setFont(BOLD, 20); c.drawString(L, top - 18, TITLE)
    field(c, R - 60, top - 18, "Stake:", 60)          # right-justified, ends at the margin

    y = top - 48
    c.setFont(BOLD, 9); c.drawString(L, y, "Options:")
    x = L + 46
    for lab in OPTIONS:
        x = checkbox(c, x, y, lab)
    field(c, x, y, "Other", R - x)

    cw = (R - L - CHK_W - NOTES_W) / NUM_PLAYERS
    draw_table(c, L, y - 12, NUM_PLAYERS, cw, NUM_ROWS, NOTES_W)


def page2(c):
    top = H - MARGIN
    c.setFillColor(colors.black)
    c.setFont(BOLD, 16); c.drawString(L, top - 14, "Using the chouette score sheet")
    body = ParagraphStyle("b", fontName=REG, fontSize=8.8, leading=11.2, spaceAfter=3.5)
    head = ParagraphStyle("h", fontName=BOLD, fontSize=9.8, leading=12, spaceBefore=4, spaceAfter=2)
    P = lambda t: Paragraph(t, body)
    Hh = lambda t: Paragraph(t, head)
    story = [
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
          "in points. In the Box's small box write the total of what he won (+) or lost (&minus). "
          "Then, in the large area of each cell, "
          "write the new total: the previous total plus the figure in the small box."),
        P("<b>Check</b>: Add the small-box figures across the row. They must sum to zero. Add the totals in the boxes "
          "across the row.  They must sum to zero also.  Check the box and start the next game."),
        Hh("Entering and leaving"),
        P("A new player entering takes a blank column and starts at 0 on the row where he joins.  Note his entry in the column at the right. "),
        P("A player who steps away temporarily keeps his column and his total.  For all the games he is away, record 0 in the small "
          "box and carry his total down."),
        P("A player who leaves for good cashes out.  Record the amount he pays (+) or receives (&minus) in "
          "his small box, and record the amount each player pays him (+) or receives from him (&minus) in "
          "the appropriate column.  Total up and Check as above: the rows sum to zero, and the cashed-out player "
          "has a zero total also.  Note his exit in the column at the right."
          ),
        Hh("Finishing"),
        P("At the end of the chouette, each player cashes out as described above.  The total of each player "
          "is now 0.  Wait for the next chouette.")
    ]
    fh = 300
    fy = top - 24 - fh
    Frame(L,
          fy,
          R - L - 50,
          fh, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0).addFromList(story, c)
    assert not story, "page-2 text overflowed"

    y = fy - 10
    c.setFont(BOLD, 9.8); c.setFillColor(colors.black)
    c.drawString(L, y, "Worked example")
    data = [
        dict(cells=[("+4", "4"), ("-2", "-2"), ("-1", "-1"), ("-1", "-1")], chk=True,
             note="Start of chouette."),
        dict(cells=[("-2", "2"), ("+1", "-1"), ("+2", "1"), ("-1", "-2")], chk=True,
             note=""),
        dict(cells=[("0", "2"), ("+1", "0"), ("-1", "0"), ("0", "-2")], chk=True,
             note="Bob is out."),
        dict(cells=[("-1", "1"), ("", ""), ("+1", "1"), ("0", "-2")], chk=True,
             note=""),
        dict(cells=[("-1", "0"), ("", ""), ("-1", "0"), ("+2", "0")], chk=True,
             note="End of chouette."),
    ]
    draw_table(c, L, y - 8, 4, 56, 5, NOTES_W, names=["Anne", "Bob", "Caleb", "Daria"], data=data)

    ns = ParagraphStyle("n", fontName=REG, fontSize=8.4, leading=10.6, spaceAfter=3)
    st = [
        Paragraph("<b>Line 1.</b> Anne, in the Box, beats Bob (Captain) with the cube at 2, and beats Caleb and Daria with the cube at 1. "
                  "Her small box shows +4, and the others show &minus;2, &minus;1 and &minus;1.", ns),
        Paragraph("<b>Line 2.</b> Caleb is now Captain, Bob is Crew. Caleb wins with his cube at 2 and Bob with his at 1; Daria had already "
                  "passed Anne's double, so Anne wins 1 from Daria. Anne's net is &minus;2 &minus;1 +1 = &minus;2. "
                  "Each row's small boxes sum to 0, and the totals do too.", ns),
        Paragraph("<b>Line 3.</b> Bob leaves the chouette and pays 1 point to Caleb.", ns),
        Paragraph("<b>Line 4.</b> Daria wins a single from Anne and loses a single to Caleb.", ns),
        Paragraph("<b>Line 5.</b> Everybody cashes out: Daria pays a point each to Anne and Caleb.", ns),

    ]
    yb = y - 8 - HDR_H - 2 * ROW_H - 10
    Frame(L,
          yb - 200 - 20,
          R - L - 235,
          125, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0).addFromList(st, c)
    assert not st, "example text overflowed"

def main():
    c = canvas.Canvas(OUTFILE, pagesize=PAGESIZE)
    c.setTitle(TITLE)
    page1(c)
    if INCLUDE_INSTRUCTIONS:
        c.showPage(); page2(c)
    c.save()
    print("wrote", OUTFILE)


if __name__ == "__main__":
    main()
