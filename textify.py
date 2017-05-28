#!/usr/bin/env python3.6
import sys

import argparse
import json
import re

def main():
	# process args
#{
	argparser = argparse.ArgumentParser(description="Processes textify files. Requires Python3.6 or later.")
	argparser.add_argument(
		"file",
		type=open,
		help="the file to be processed")
	argparser.add_argument(
		"--refs", "-r",
		type=open,
		help="references for the file. JSON formatting.")

	args = argparser.parse_args()
#}

	# define counters
#{
	# There is one counter per "level" of section (e.g 1.2.3)
	# We inc/decrement the section level when we enter or leave a section, respectively.
	sectioncounter = [0, 0, 0, 0]
	sectionlevel = 0
#}

	# build internal reference dict
#{
	references = {}
	if args.refs:
		references = json.load(args.refs)

	# this is the list of references that were actually used in the doc
	referencesUsed = []
#}

	# setup output
#{
	# section and reference numbering
	outfilename = args.file.name.replace(".text", ".html", 1)
	outreffilename = args.file.name.replace(".text", ".refs", 1)
#}

	# process file
#{
	with open(outfilename, "w") as outputfile:
		for line in args.file:

			# handle section numbering
		#{
			if "<section>" in line:
			# Increment section counter for this level, and go up one level
				sectioncounter[sectionlevel] += 1
				sectionlevel += 1

			if "</section>" in line:
			# reset section counter for this level and go down one level
				sectioncounter[sectionlevel] = 0
				sectionlevel -= 1

			sectionnumber = str(sectioncounter[0])
			# we always want the top-level section number

			for num in sectioncounter[1:]:
			# append sub-section numbers if they are not zero
				if num != 0:
					sectionnumber += f".{num}"

			line = line.replace("<sectiontitle>", "<sectiontitle>"+sectionnumber+": ", 1)
			# prepend section number to section title
#}

			# handle references
#{
			if references is not {}:
			# if reference file was specified, do referencing
				# search for pattern, and build a list of the reference ids.
				refTagPattern = "(<reference>)(.*)(</reference>)"
				referenceRegexMatches = re.finditer(refTagPattern, line)
				refIds = [match.group(2) for match in referenceRegexMatches]

				for refId in refIds:
				# check that refId is in refDict
					if refId in references:
					# get inline reference info
						inlineAuthorName = references[refId]['inlineAuthorName']
						year_pub = str(references[refId]['inlineDate'])
					
					# build the inline refernce string
						inlineReference = "(" + inlineAuthorName + ", " + year_pub + ")"

					# do a regex search and replace
						toReplace = r"<reference>" + refId + r"</reference>" 
						replacement = r"<reference>" + inlineReference + r"</reference>"
						line = re.sub(toReplace, replacement, line)
					
					# finally, add it to the list of used references
						referencesUsed.append(references[refId])
					
					else:
					# reference with id refId was not found in refDict
						sys.stderr.write(f"error: reference not found in references file: {refId}\n")
#}

			# handle bibliography
#{
			if "<bibliography>" in line:
			# first sort the list of references based on inline author name
				referencesUsed = sorted(referencesUsed, key=lambda d: d['inlineAuthorName'])
			
			# now iterate over the list of references
				for ref in referencesUsed:
				# build a string for the bibliography for this reference
					refString = ""
#{
					refString += ref["bibAuthorName"] + ", "

					if "inlineDate" in ref:
						refString += "(" + ref["inlineDate"] + "). "
					else:
						refString += "(n.d). "

					refString += "<referenceTitle>" + ref["bibTitle"] + "</referenceTitle> "

					if "bibEdition" in ref:
						refString += "(" + ref["bibEdition"]

						if "bibPageNum" in ref:
							refString += ", " + ref["bibPageNum"]

						refString += "). "
					
					if "bibPlaceOfPub" in ref:
						refString += ref["bibPlaceOfPub"] + ". "

					if "bibPublisher" in ref:
						refString += ref["bibPublisher"] + ". "

					if "bibDateRetrieved" in ref:
						refString += "Retrieved: " + ref["bibDateRetrieved"] + ". "
#}
					line += "<br><br>" + refString

#}

			outputfile.write(line)
#}

	# create bibliography file
#{
	with open(outreffilename, "w") as bib:
		bib.write("<bibliography>")
	# first sort the list of references based on inline author name
		referencesUsed = sorted(referencesUsed, key=lambda d: d['inlineAuthorName'])
	
	# now iterate over the list of references
		for ref in referencesUsed:
		# build a string for the bibliography for this reference
			refString = ""
			refString += ref["bibAuthorName"] + ", "

			if "inlineDate" in ref:
				refString += "(" + ref["inlineDate"] + "). "
			else:
				refString += "(n.d). "

			refString += "<referenceTitle>" + ref["bibTitle"] + "</referenceTitle> "

			if "bibEdition" in ref:
				refString += "(" + ref["bibEdition"]

				if "bibPageNum" in ref:
					refString += ", " + ref["bibPageNum"]

				refString += "). "
			
			if "bibPlaceOfPub" in ref:
				refString += ref["bibPlaceOfPub"] + ". "

			if "bibPublisher" in ref:
				refString += ref["bibPublisher"] + ". "

			if "bibDateRetrieved" in ref:
				refString += "Retrieved: " + ref["bibDateRetrieved"] + ". "

			bib.write(refString)

		bib.write("</bibliography>")
#}

	return 0
	# end main

if __name__ == "__main__":
	main()
