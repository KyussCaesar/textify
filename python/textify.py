import argparse

def main():
    # process args
#{
    # at the moment there is only one argument:
    # --file FILE : The file to be processed
    argparser = argparse.ArgumentParser(description="Processes textify files")
    argparser.add_argument(
        "--file",
        type=open,
        help="The file to be processed")

    # TODO Add check for if nothing was passed to skip
    args = argparser.parse_args()
#}

    # define counter
#{
    # There is one counter per "level" of section (e.g 1.2.3)
    # We inc/decrement the section level when we enter or leave a section, respectively.
    sectioncounter = [0, 0, 0, 0]
    sectionlevel = 0
#}

    # process file
#{
    for line in args.file:

        if "<section>" in line:
        # Increment section counter for this level, and go up one level
            sectioncounter[sectionlevel] += 1
            sectionlevel += 1

        if "</section>" in line:
        # reset section counter for this level and go down one level
            sectioncounter[sectionlevel] = 0
            sectionlevel -= 1

        numberstr = str(sectioncounter[0])
        # we always want the top-level section number

        for num in sectioncounter[1:]:
        # append sub-section numbers if they are not zero
            if num != 0:
                numberstr += f".{num}"

        line = line.replace("<sectiontitle>", "<sectiontitle>"+numberstr+": ", 1)
        # prepend section number to section title
#}

    # write output
#{
        outfilename = args.file.name.replace(".text", ".html", 1)
        with open(outfilename, "a") as output:
            output.write(line)
#}

    return 0
    # end main

if __name__ == "__main__":
    main()
