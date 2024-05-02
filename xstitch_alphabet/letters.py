import copy

class Cell:
    def __init__(self, x, y, cellContents):
        self.x = x
        self.y = y
        self.contents = cellContents
        pass

    def getLocation(self):
        return (self.x, self.y)

    def isBaseline(self):
        return self.contents.find("b") > -1 or self.contents.find("B") > -1

    def getNorth(self):
        return (self.x, self.y - 1)

    def getSouth(self):
        return (self.x, self.y + 1)

    def getEast(self):
        return (self.x + 1, self.y)

    def getWest(self):
        return (self.x - 1, self.y)

    def getNortheast(self):
        return (self.x + 1, self.y - 1)

    def getSoutheast(self):
        return (self.x + 1, self.y + 1)

    def getNorthwest(self):
        return (self.x - 1, self.y - 1)

    def getSouthwest(self):
        return (self.x - 1, self.y + 1)

    def cardinals(self):
        return [self.getNorth(), self.getNortheast(),
                self.getEast(), self.getSoutheast(),
                self.getSouth(), self.getSouthwest(),
                self.getWest(), self.getNorthwest()]
    

    def __str__(self):
        return "(({}, {}): {})".format(self.x, self.y, self.contents)
    pass

# class CrossStitchContents:
def formatContents(contents, sep="\n", letterSep="", show_invisible=False, render=True):
    def formatCell(cell):
        if not show_invisible and cell == "|":
            return " "
        if not show_invisible and cell == "B":
            return " "
        if render and cell == "b":
            return "x"
        return "{:<1}".format(cell)
    
    def formatRow(row):
        return letterSep.join(list(map(formatCell, row)))
    return sep.join(list(map(formatRow, contents)))

class CrossStitchLetter:
    def __init__(self, contents, name=""):
        self.contents = contents
        self.baselineIndex = -1
        for i in range(len(contents)):
            for j in range(len(contents[i])):
                if contents[i][j].find("b") > -1:
                    self.baselineIndex = i
                    pass
                pass
            pass
        
        self.name = name
        pass

    def __iter__(self):
        return iter(self.contents)

    def hasName(self):
        return len(self.name) > 0

    def setName(self, name: str):
        self.name = name
        return self

    def getBaseline(self):
        return self.baselineIndex
    
    def getHeight(self):
        return len(self.contents)

    def getWidth(self):
        assert self.contents and len(self.contents[0]) > 0
        return len(self.contents[0])

    def withPadding(self, above=0, below=0):
        if (above == 0 and below == 0):
            return copy.deepcopy(self.contents)
        content = copy.deepcopy(self.contents)
        width = self.getWidth()
        if above > 0 and below == 0:
            return [([""]) * width] * above + content
        if below > 0 and above == 0:
            return content + [([""]) * width] * below
        
        return [([""] * width)] * above + content + [([""] * width)] * below

    def formatContents(self, sep="\n", show_invisible=False, render=True):
        return formatContents(self.contents, sep=sep, show_invisible=show_invisible, render=render)
        # def formatCell(cell):
        #     if not show_invisible and cell == "|":
        #         return " "
        #     if not show_invisible and cell == "B":
        #         return " "
        #     if render and cell == "b":
        #         return "x"
        #     return "{:<1}".format(cell)

        # def formatRow(row, sep=""):
        #     return sep.join(list(map(formatCell, row)))
        # return sep.join(list(map(formatRow, self.contents)))

    def __str__(self):
        return self.formatContents()
    pass

def addPaddingRow(letterRows, numRows=1, above=True):
    assert len(letterRows) > 0
    if (numRows > 0):
        width = len(letterRows[0])
        padding = [""] * width
        if above:
            return ([padding] * numRows) + letterRows
        else:
            return letterRows + ([padding] * numRows)
    return letterRows

def concatWriting(pre, nxt):
    assert len(pre) == len(nxt), "Error: pre and nxt should have the same length, but got {} vs {}".format(len(pre), len(nxt))
    return [pre[i] + nxt[i] for i in range(len(pre))]
    

class CrossStitchMessage:
    def __init__(self, *letters, letterSepOther=" "):
        self.message = []
        self.baselineIndex = -1
        print(type(letters))
        for l in letters:
            print(type(l))
            print(l)
            print(l.getWidth())
            lpaddingAbove = 0
            lpaddingBelow = 0
            if l.getBaseline() > self.baselineIndex:
                if self.baselineIndex == -1:
                    for row in l:
                        self.message.append(copy.deepcopy(row))
                        pass
                    self.baselineIndex = l.getBaseline()
                    self.addHorizontalPadding()
                    continue
                else:
                    # need to pad out the message, this letter is taller than previous ones
                    self.message = addPaddingRow(self.message, numRows=l.getBaseline() - self.baselineIndex)
                    if l.getHeight() > self.getHeight():
                        self.message = addPaddingRow(self.message, numRows=l.getHeight() - self.getHeight(), above=False)
                        pass
                    else:
                        lpaddingBelow = self.getHeight() - l.getHeight()
                    pass
                pass
            else:
                lpaddingAbove = self.baselineIndex - l.getBaseline()
                if l.getHeight() + lpaddingAbove > self.getHeight():
                    self.message = addPaddingRow(self.message, numRows=l.getHeight() + lpaddingAbove - self.getHeight())
                    pass
                else:
                    lpaddingBelow = self.getHeight() - l.getHeight() - lpaddingAbove
                    pass
                pass
            print(len(self.message), lpaddingAbove, lpaddingBelow, l.getHeight() + lpaddingAbove + lpaddingBelow)
            self.baselineIndex = max(self.baselineIndex, l.getBaseline() + lpaddingAbove)
            self.message = concatWriting(self.message, l.withPadding(above=lpaddingAbove, below=lpaddingBelow))
            self.addHorizontalPadding()
            pass
        pass

    def addHorizontalPadding(self, pad=1):
        index = 0
        while index < pad:
            for i in range(len(self.message)):
                self.message[i].append("")
                pass
            index += 1
            pass
        return self

    def getBaseline(self):
        return self.baselineIndex
    

    def getHeight(self):
        return len(self.message)

    def getWidth(self):
        assert self.getHeight() > 0
        return len(self.message[0])


    def formatContents(self, sep="\n", letterSep="", show_invisible=False, render=True):
        return formatContents(self.message, sep=sep, letterSep=letterSep, show_invisible=show_invisible, render=render)

    def __str__(self):
        return self.formatContents()
