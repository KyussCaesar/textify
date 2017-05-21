import argparse

def main():
    # process args
    argparser = argparse.ArgumentParser(description="Preprocesses textify")
    argparser.add_argument(
        "--file",
        type=open,
        help="The file to be processed")
    args = argparser.parse_args()

    sectioncounter = [0, 0, 0, 0]
    sectionlevel = 0

    # process file
    for line in args.file:

        # check for what rule applies
        # write result line to new file

        if "<section>" in line:
            sectioncounter[sectionlevel] += 1
            sectionlevel += 1

        if "</section>" in line:
            sectioncounter[sectionlevel] = 0
            sectionlevel -= 1

        numberstr = str(sectioncounter[0])

        for num in sectioncounter[1:]:
            if num != 0:
                numberstr += f".{num}"

        line = line.replace("<sectiontitle>", "<sectiontitle>"+numberstr+": ", 1)

        with open(str(args.file)+".html", "a") as output:
            output.write(line)

    return 0

if __name__ == "__main__":
    main()
