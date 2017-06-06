clean:
	rm -r ./testing/out
	mkdir ./testing/out

test: clean test1 test2

TEXTIFYPATH=./textify.py
TESTINGFOLDER=./testing
TESTINGOUTPUT=$(TESTINGFOLDER)/out
TESTINGCOMP=$(TESTINGFOLDER)/eout
TESTINGREPORTS=$(TESTINGFOLDER)/reports
TESTREPORTNAME=`date +%Y_%m_%d-%H_%M_%S`

test1: ./textify.py
	$(TEXTIFYPATH) $(TESTINGFOLDER)/test1.text --out $(TESTINGOUTPUT)/test1
	diff $(TESTINGOUTPUT)/test1.html ./testing/eout/test1-cmp.html >> ./testing/reports/test1_$(TESTREPORTNAME)

test2: ./textify.py
	$(TEXTIFYPATH) $(TESTINGFOLDER)/test2.text --out $(TESTINGOUTPUT)/test2 --ref $(TESTINGFOLDER)/test2.references
	diff $(TESTINGOUTPUT)/test2.html $(TESTINGCOMP)/test2-cmp.html >> $(TESTINGREPORTS)/test2_$(TESTREPORTNAME)
	diff $(TESTINGOUTPUT)/test2.refs $(TESTINGCOMP)/test2-cmp.refs >> $(TESTINGREPORTS)/test2_$(TESTREPORTNAME)
