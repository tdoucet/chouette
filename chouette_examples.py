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

# --- A new example: copy this skeleton, fill it in, and add it to EXAMPLES. ---
#
# TRICKY = dict(
#     title="A short heading",              # shown above the example when there are several
#     intro="One or two sentences setting up the situation.",
#     names=["Anne", "Bob", "Caleb", "Daria"],
#     rows=[
#         dict(cells=[("+2", "2"), ("-1", "-1"), ("-1", "-1"), ("0", "0")],
#              note="Short note.",                          # Notes column
#              rotation="Anne / Bob / Caleb / Daria",       # shown beside the row
#              text="What happened and how it is scored."), # explanation below the table
#         # ... one dict per row ...
#     ],
#     outro="Anything to say after the explanations.",
# )

EXTRAS_EXAMPLE = dict(
    title="Cube Extras",
    names=["Chris", "Todd", "Pete", "Steve"],
    rows=[
        dict(cells=[("", "3"), ("", "-2"), ("", "7"), ("", "-8")],
             text="Prior games.", rotation="",
             ),
                  
        dict(cells=[("+2", "5"), ("-1", "-3"), ("0", "7"), ("-1", "-9")],
             note = "drops",
             rotation="Chris / Pete / Steve / Todd",
             text="Box Chris doubles all from center.  Captain Pete is the lone "
                  "taker. Record the drops now."),

        dict(cells=[("0", "5"), ("-1", "-4"), ("+2", "9"), ("-1", "-10")],
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
             text="Steve is next up as Captain."),
    ],
)

EXTRAS_EXAMPLE_2 = dict(
    title="Cube Extras: streamlined",
    names=["Chris", "Todd", "Pete", "Steve"],
    outro="Same game, with the intermediate totals omitted. Each total includes the "
          "sum of the small boxes above it.",
    rows=[
        dict(cells=[("", "3"), ("", "-2"), ("", "7"), ("", "-8")],
             rotation="",
             ),
                  
        dict(cells=[("+2", ""), ("-1", ""), ("0", ""), ("-1", "")],
             note = "drops",
             rotation="Chris / Pete / Steve / Todd",
             ),

        dict(cells=[("0", ""), ("-1", ""), ("+2", ""), ("-1", "")],
             note="extras",
             rotation="Chris / Pete / Steve / Todd",
             ),

        dict(cells=[("+4", "9"), ("+4", "0"), ("-12", "-3"), ("+4", "-6")],
             rotation="Chris / Pete / Steve / Todd",
             note="end of game",
             ),

        dict(cells=[("", ""), ("", ""), ("", ""), ("", "")],
             note="",
             chk=False,
             rotation="Chris / Steve / Todd / Pete",
             ),
    ],
)


EXAMPLES = [EXTRAS_EXAMPLE, EXTRAS_EXAMPLE_2]




if __name__ == "__main__":
    write_examples(OUTFILE, DOC_TITLE, EXAMPLES, intro=INTRO)
    print("wrote", OUTFILE)
