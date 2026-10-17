#!/usr/bin/env python3
"""
Standalone worked-example documents, built on chouette_sheet.py.

    python chouette_examples.py        # writes chouette_examples.pdf

An example is plain data (see the comment above BASIC_EXAMPLE in chouette_sheet.py
for every key).  Put one or several in EXAMPLES and they flow into one document,
onto as many pages as needed.  Layout, spacing and cell size are shared with the
main sheet, so changing a constant in chouette_sheet.py changes both.
"""
from chouette_sheet import write_examples, BASIC_EXAMPLE

OUTFILE   = "chouette_examples.pdf"
DOC_TITLE = None        # None: each example's own title is its heading
INTRO     = None        # optional paragraph (or list of paragraphs) under the document title

EXTRAS_EXAMPLE = dict(
    title="Cube Extras",
    side_note="Rotation in effect at start of period.  Leftmost is box.",
    names=["Chris", "Todd", "Pete", "Steve"],
    rows=[
        dict(cells=[("", "3"), ("", "-2"), ("", "7"), ("", "-8")],
             text="Prior games.",
             rotation=""
             ),
                  
        dict(cells=[("+2", ""), ("-1", ""), ("", ""), ("-1", "")],
             note = "drops",
             rotation="Chris / Pete / Steve / Todd",
             text="Box Chris doubles all from center.  Captain Pete is the lone "
                  "taker. Record the drops now."
             ),

        dict(cells=[("", ""), ("-1", ""), ("+2", ""), ("-1", "")],
             note="extras",
             rotation="Chris / Pete / Steve / Todd",
             text="Crew gives Extras.  Record those payments now."
             ),

        dict(cells=[("+4", "9"), ("+4", "0"), ("-12", "-3"), ("+4", "-6")],
             rotation="Chris / Pete / Steve / Todd",
             note="end of game",
             text="Box & Captain play with one cube visible.  Box gammons Captain. "
                  "Record gammon for box, copy same value to each extra giver, extra "
                  "taker makes up the balance."
             ),

        dict(cells=[("", ""), ("", ""), ("", ""), ("", "")],
             note="",
             chk=False,
             rotation="Chris / Steve / Todd / Pete",
             text="Steve is next up as Captain."
             ),
    ],
)

PARTNERS_EXAMPLE = dict(
    title="Partners",
    side_note="* marks this game's Partner.",
    names=["Chris", "Todd", "Pete", "Steve", "Gerry", "Hana"],
    rows=[
        dict(cells=[("", "9"), ("", "0"), ("", "-3"), ("", "-6"), ("", "0"), ("", "0")],
             note="Hana is in.\nGerry is in.",
             rotation="Chris / Steve / Todd* / Pete / Gerry / Hana",
             text="Hana joins at the bottom. Box Chris invites Todd, next in line after Captain Steve, "
                  "to be his Partner. Todd accepts."),

        dict(cells=[("+1", ""), ("+1", ""), ("", ""), ("", ""), ("-1", ""), ("-1", "")],
             rotation="Chris / Steve / Todd* / Pete / Gerry / Hana",
             text="Box doubles everyone. Gerry and Hana pass. Steve and Pete take, so their boxes stay open. "
                  "The partners split the two points."),

        dict(cells=[("+1", ""), ("+1", ""), ("", ""), ("-2", ""), ("0", ""), ("0", "")],
             rotation="Chris / Steve / Todd* / Pete / Gerry / Hana",
             text="Box redoubles and Captain Steve drops, losing 2. Pete is Acting Captain."),

        dict(cells=[("-1", "10"), ("-1", "1"), ("+2", "-1"), ("0", "-8"), ("0", "-1"), ("0", "-1")],
             rotation="Chris / Steve / Todd* / Pete / Gerry / Hana",
             text="Pete wins a single with the cube at 2, so the partners lose 2 and split it. "
                  "Together they are up 2 on the game, and they beat the Captain."),

        dict(cells=[("", ""), ("", ""), ("", ""), ("", ""), ("", ""), ("", "")],
             chk=False,
             rotation="Chris / Todd / Pete / Gerry / Hana / Steve",
             text="Chris keeps the Box and Steve goes to the bottom. The partnership is over. "
                  "Todd is now Captain, and Chris may invite Pete."),
    ],
)



EXAMPLES = [EXTRAS_EXAMPLE, PARTNERS_EXAMPLE]


if __name__ == "__main__":
    write_examples(OUTFILE, DOC_TITLE, EXAMPLES, intro=INTRO)
    print("wrote", OUTFILE)
