import argparse
import os
import sys
import json
from xstitch_alphabet.letters import Cell, CrossStitchLetter

def parse_args():
    ap = argparse.ArgumentParser()

    ap.add_argument("file", help="A CSV file containing the cross stitch alphabet you'd like to parse. x represents a normal stitch, b represents the baseline of the type, / represents a single leg of a cross, and | connects multi-part letters and punctuation, i.e., lowercase i and exclamation marks. 'B' may be used to indicate the baseline for punctuation such as apostrophes, and will be treated as being invisible.")

    ap.add_argument("--output", "-o", default="output.json",
                    help="Where to store the JSON representation of this cross stitch alphabet.")

    ap.add_argument("--auto-assign", "-a", action="store_true",
                    help="Automatically assign letters, and then confirm")

    ap.add_argument("--static", "-s", action="store_true",
                    help="Don't assign letters names interactively. Just output a JSON file containing each identified individual letter.")

    return ap.parse_args()
        

def getConnected(cell, nonempties, baselines):
    connected = [cell]
    # print(cell)
    # print(cell.cardinals())
    for c in cell.cardinals():
        # print("Cardinal:", c)
        if c in nonempties:
            if c in baselines:
                baselines.pop(c)
                pass
            cardinal_cell = nonempties.pop(c)
            connected.append(cardinal_cell)
            connected.extend(getConnected(cardinal_cell, nonempties, baselines))
            pass
        pass
    return connected

def getBounds(connectedCells):
    assert (len(connectedCells) != 0), "Connected cells length must be greater than 0"

    left = connectedCells[0].x
    right = left
    up = connectedCells[0].y
    down = up

    for c in connectedCells[1:]:
        x, y = c.getLocation()
        if x < left:
            left = x
            pass
        if y <  up:
            # counterintuitively, smaller indices are higher
            up = y
            pass
        if x > right:
            right = x
            pass
        if y > down:
            down = y
            pass
        pass
    # return the upper left most point, and the lower right most point
    return ((left, up), (right, down))
    

    

def parse_out_filled_cells(contents: str):
    lines = [l.split(",") for l in contents.split("\n")]
    lines = [[l.strip() for l in line] for line in lines]
    nonempty = []
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j]:
                nonempty.append(Cell(j, i, lines[i][j]))
                pass
            pass
        pass
    # print(" ".join(list(map(str, nonempty[:min(10, len(nonempty))]))))
    nonempties = { c.getLocation(): c for c in nonempty }
    # print(nonempties)
    baselines = [c for c in nonempty if c.isBaseline()]

    # print(" ".join(list(map(str, baselines[:min(10, len(baselines))]))))

    baselineDict = { c.getLocation(): c for c in baselines }
    basekeys = list(baselineDict.keys())
    if len(basekeys) > 0:
        used = set()
        letters = []
        for k in basekeys:
            if k not in used:
                connected = getConnected(baselineDict[k], nonempties, baselineDict)
                # print(connected)
                upperLeft, lowerRight = getBounds(connected)
                ulx, uly = upperLeft
                lrx, lry = lowerRight
                # print(upperLeft, lowerRight)
                # first have to do the vertical part, then the horizontal part
                rows = [line[ulx:lrx+1] for line in lines[uly:lry + 1]]
                xs_letter = CrossStitchLetter(rows)
                print(xs_letter)
                used.update([c.getLocation() for c in connected if c.isBaseline()])
                letters.append(xs_letter)
                pass
            pass
        return letters
    pass
            


def interactiveAssign(letters, doubleCheck=False):
    letterNames = [l.name for l in letters if l.hasName()]
    noNameLetters = [l for l in letters if doubleCheck or not l.hasName()]
    for l in noNameLetters:
        print(l)
        if not l.hasName():
            newName = input("Please give the (case-sensitive) alphabetic character of the above letter: ")
            brk = False
            while newName in letterNames:
                print("Sorry, {} is already taken, and was assigned to {}.".format(newName, list(filter(lambda x: x.name == newName, letters))))
                tryagain = input("Would you like to try again? [y/n] ")
                if tryagain.lower().find("y") > -1:
                    newName = input("Please give the (case-sensitive) alphabetic character of the above letter: ")
                    pass
                else:
                    brk = True
                    break
                pass
            if brk:
                break
            else:
                l.setName(newName)
                letterNames.append(newName)
                pass
            pass
        elif doubleCheck:
            rename = input("Would you like to reassign a new character to the above letter (current character is {}): [y/n] ".format(l.name))
            if rename.lower().find("y") > -1:
                newName = input("Please input a new character: ")
                while newName in letterNames:
                    newName = input("Sorry, character {} is already taken, and was assigned to {}. Please give a new character: ".format(newName, list(filter(lambda x: x.name == newName, letters))))
                    pass
                l.setName(newName)
                pass
            pass
        pass
    pass
        
def assignLetterNames(letters, args):
    if args.auto_assign:
        ls = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789.,!?'"
        for i in range(min(len(letters), len(ls))):
            letters[i].setName(ls[i])
            pass
        pass
    if not args.static:
        interactiveAssign(letters, doubleCheck=args.auto_assign)

    



if __name__ == "__main__":
    args = parse_args()

    if not os.path.exists(args.file):
        print("Path {} does not exist -- need an actual file containing the cross stitch alphabet you'd like to parse!".format(args.file), file=sys.stderr)
        pass

    contents = ""
    with open(args.file, "r") as f:
        contents = f.read()
        pass

    letters = parse_out_filled_cells(contents)

    
    assignLetterNames(letters, args)

    
    unknowns = 0

    lettersDict = {}

    for l in letters:
        if l.hasName() and l.name not in lettersDict:
            lettersDict[l.name] = l.contents
            pass
        else:
            # l doesn't have a name or l.name is already in lettersDict
            if l.name in lettersDict:
                print("Name {} is already in letters dictionary, will give it an unknown name for now.".format(l.name), file=sys.stderr)
                pass
            elif not l.hasName():
                print(l, file=sys.stderr)
                print("Above letter doesn't have a name, will give it an unknown name for now.")
                pass
            lettersDict["<unknown" + str(unknowns) + ">"] = l.contents
            unknowns += 1
            pass
        pass
    
    

    with open(args.output, "w") as f:
        f.write(json.dumps(lettersDict))
        f.flush()
        pass
    pass
                
            
            
