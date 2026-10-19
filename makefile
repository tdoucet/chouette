chouette.pdf : chouette_rules.pdf \
               chouette_sheet_8x16.pdf \
               chouette_instructions.pdf
	qpdf --empty --pages chouette_rules.pdf \
                         chouette_sheet_8x16.pdf \
                         chouette_sheet_8x16.pdf \
                         chouette_instructions.pdf \
                         -- chouette.pdf

chouette_rules.pdf : chouette_rules.tex
	xelatex chouette_rules.tex

chouette_sheet.pdf :
	~/env/bin/python chouette_sheet.py --sheet-only standard

chouette_sheet_8x16.pdf :
	~/env/bin/python chouette_sheet.py --sheet-only large

chouette_sheet_6x12.pdf :
	~/env/bin/python chouette_sheet.py --sheet-only jumbo

chouette_instructions.pdf :
	~/env/bin/python chouette_sheet.py --guide-only

deploy : chouette.pdf \
         chouette_sheet.pdf \
         chouette_sheet_8x16.pdf \
         chouette_sheet_6x12.pdf
	cp chouette.pdf rules/
	cp chouette_sheet.pdf \
       chouette_sheet_8x16.pdf \
       chouette_sheet_6x12.pdf \
       sheets/

clean :
	rm -f *.pdf *.aux *.log
