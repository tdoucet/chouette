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
    names=["Chris", "Todd", "Pete", "Steve"],
    rows=[
        dict(cells=[("", "3"), ("", "-2"), ("", "7"), ("", "-8")],
             text="Prior games.",
             rotation=""
             ),
                  
        dict(cells=[("+2", ""), ("-1", ""), ("0", ""), ("-1", "")],
             note = "drops",
             rotation="Chris / Pete / Steve / Todd",
             text="Box Chris doubles all from center.  Captain Pete is the lone "
                  "taker. Record the drops now."
             ),

        dict(cells=[("0", ""), ("-1", ""), ("+2", ""), ("-1", "")],
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


EXAMPLES = [EXTRAS_EXAMPLE]


if __name__ == "__main__":
    write_examples(OUTFILE, DOC_TITLE, EXAMPLES, intro=INTRO)
    print("wrote", OUTFILE)
