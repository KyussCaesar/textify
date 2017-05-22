#!/usr/bin/env python3.6

import argparse

def main():
    # process args
#{
    # at the moment there is only one argument:
    # --file FILE : The file to be processed
    argparser = argparse.ArgumentParser(description="Processes textify files")
    argparser.add_argument(
        "file",
        type=open,
        help="The file to be processed")

    # TODO Add check for if nothing was passed to skip
    args = argparser.parse_args()
#}

    # define counters
#{
    # There is one counter per "level" of section (e.g 1.2.3)
    # We inc/decrement the section level when we enter or leave a section, respectively.
    sectioncounter = [0, 0, 0, 0]
    sectionlevel = 0

    # likewise, count references for Chicago style
    refcounter = 0

#}

    # setup output
#{
    # section and reference numbering
    outfilename = args.file.name.replace(".text", ".html", 1)
    outreffilename = args.file.name.replace(".text", ".references", 1)
    with open(outfilename, "w") as outputfile:
#}

    # process file
#{
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

            # handle reference numbering
        #{
            if "<reference>" in line:
            # increment the reference counter
                refcounter += 1
        #}

            outputfile.write(line)

#}

    return 0
    # end main

if __name__ == "__main__":
    main()
