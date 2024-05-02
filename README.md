xstitch-abcs
===============

Parses letter patterns from spreadsheets so that you can generate a
message in that alphabet.

(Hopefully in the future, some kind of computer vision/ML solution can
be created to automatically ingest pattern PDFs)

This README contains the following topics:

1. [Why spreadsheets?](#why-spreadsheets)
2. [How it works](#how-it-works)
3. [Installation](#installation)
 - [Demo](#demo)
4. [Parsing](#parsing)
5. [Message generation](#message-generation)
6. [Current issues](#current-issues)


# Why spreadsheets?

I like to use spreadsheets to tweak and design cross stitch
patterns. Using [conditional formatting](https://support.google.com/docs/answer/78413?hl=en&co=GENIE.Platform%3DDesktop), you can color each square
with just a single letter.

![A screenshot of a spreadsheet. Empty cells are blank. 10 cells are
marked with "x"'s, and are highlighted in green. The 10 cells are in
the shape of an "s".](img/s_google_sheets.png)

![A screenshot of a Google Sheets conditional formatting configuration
widget. It applies a conditional formatting rule to a range of cells
on the spreadsheet, and when the rule is met, it applies a
format.](img/conditional_formatting.png)

Moving elements around is as easy as copying and pasting the text
inside. But copying and pasting, when you need to create a whole
message, can be tedious! Even if the message has a lot of repeated
letters, you'll have to go back and forth a lot. This is where this
Python module comes in.

# How it works

Suppose you have an alphabet that you've designed in a spreadsheet,
and you'd like to be able to write fluently in it. If you have a
message, you'd like to just instantly translate it into your
cross stitch alphabet!

You can feed the spreadsheet into the cross stitch parser program, and
this will create a JSON file containing a mapping of characters, like
"A" or "b", to their cross stitch alphabet representation. It does
this by detecting each connected component in the spreadsheet, which
usually identifies a letter. The produced JSON file can then be used
by the writing program to transcribe your desired text.

This tool has two parts: a parser, which turns spreadsheets into
alphabets, and the translator, which turns your desired message into a
cross stitch pattern.


# Installation

## Demo

After installing, you can access the `xstitch_alphabet`
python module from the command line.

Running `python -m xstitch_alphabet.parse --help` produces the output:

```
usage: parse.py [-h] [--output OUTPUT] [--auto-assign] [--static] file

positional arguments:
  file                  A CSV file containing the cross stitch alphabet you'd like to parse. x represents a normal stitch, b represents the baseline of the type, / represents a single leg of a cross,
                        and | connects multi-part letters and punctuation, i.e., lowercase i and exclamation marks. 'B' may be used to indicate the baseline for punctuation such as apostrophes, and will
                        be treated as being invisible.

optional arguments:
  -h, --help            show this help message and exit
  --output OUTPUT, -o OUTPUT
                        Where to store the JSON representation of this cross stitch alphabet.
  --auto-assign, -a     Automatically assign letters, and then confirm
  --static, -s          Don't assign letters names interactively. Just
  output a JSON file containing each identified individual letter.
```

There are a couple of sample files that you can download as well, in
`samples/alphabets/myalphabet.json` and `samples/csvs/myalphabet.csv`.

To test out parsing, you can run `python -m xstitch_alphabet.parse -a
-s myalphabet.csv -o myalphabet.json`, which will produce a
`myalphabet.json` file.

Then you can try out the transcriber by running `python -m
xstitch_alphabet.write --message 'HelloWorld!' myalphabet1.json`,
which should produce

```
x   x      x x      x     x          x    x x 
x   x      x x      x     x          x    x x 
x   x  xx  x x      x     x          x    x x 
xxxxx x  x x x  xx  x  x  x  xx   xx x  xxx x 
x   x xxx  x x x  x x  x  x x  x x   x x  x x 
x   x x    x x x  x  x x x  x  x x   x x  x 
x   x  xxx x x  xx    x x    xx  x   x  xxx x 
```
You can also use the `--sep` option to specify a different spacer. If
you use a tab character, then you can copy that output and paste it
back into a spreadsheet, where you're designing your cross stitch!


# Parsing

## Preparing your alphabet

### Dotting your i's...

![A screenshot of a spreadsheet where G and H are displayed. They are
completely connected, and will be detected accurately by the parser program.](img/gh.png)

For most letters, like G and H, the connected component method works
out just fine. There are just a few that might give you trouble, such
as "i" or some punctuation. In order connect the dots to the rest of
the letter or symbol, we use "|" as a "connecting" character. These
"connecting characters" won't show up in any generated messages, and
are just there to tell the parser that seemingly disconnected
components are actually connected.

![A screenshot of an exclamation point in a spreadsheet, where between
the dot and the line of the exclamation point is a "|" character that
connects them.](img/exclamation.png)


`TODO: Add an option to specify a different connecting character.`

### Identifying the baseline

The _baseline_ is a [concept in typography](https://en.wikipedia.org/wiki/Baseline_(typography)). Most Latin-based scripts
have writing that sits on top of the baseline, unless you have a tail
like the letters "y", "g", etc. We need to identify the baseline in
order to determine how to align the letters.

`TODO: Add an option to turn on/off automatic baseline identification`

You can indicate the baseline of the characters to the parser by using
the letter `b` in the squares that are on the baseline. Any square
with a `b` will be turned into whatever normal character (e.g., `x`)
you used to fill the other squares. In the previous screenshots, the
baseline has been colored red.

`TODO: Provide an option to set the normal character`

#### Prepping characters that do _not_ touch the baseline

A few characters, such as quotes or apostrophes, do not touch the
baseline. To indicate the baseline for these, you can use the
character `B`, like in this apostrophe (the tail is indicated by
`/`). When a word with an apostrophe is generated, the `B` will _not_
be rendered as an `x` (or whatever the default character is).

![The apostrophe character, represented in a spreadsheet. The dot with
its little tail does not even get anywhere near the baseline. Instead,
`B` is used to indicate the apostrophe's baseline, and the apostrophe
is connected to the baseline by a series of `|` characters.](img/apostrophe.png)

## Running the parser

Once you have prepped your cross stitch alphabet, it's time to run the
parser.

```
usage: parse.py [-h] [--output OUTPUT] [--auto-assign] [--static]
                file

positional arguments:
  file                  A CSV file containing the cross stitch
                        alphabet you'd like to parse. x represents a
                        normal stitch, b represents the baseline of
                        the type, / representns a single leg of a
                        cross, and | connects multi-part letters and
                        punctuation, i.e., lowercase i and
                        exclamation marks. 'B' may be used to
                        indicate the baseline for punctuation such
                        as apostrophes, and will be treated as being
                        invisible.

optional arguments:
  -h, --help            show this help message and exit
  --output OUTPUT, -o OUTPUT
                        Where to store the JSON representation of
                        this cross stitch alphabet.
  --auto-assign, -a     Automatically assign letters, and then
                        confirm
  --static, -s          Don't assign letters names interactively.
                        Just output a JSON file containing each
                        identified individual letter.
```

You run the parser from the command line (you'll need to [install
it](#Installation) first). The parser requires one argument, a CSV
file containing your alphabet. You can invoke it like this:

```
$ python3 parse.py alphabet.csv
```

### Character identification

The `parse.py` program will find all of the connected components, and
at the end, ask you to identify each letter.

```
 xxx 
x   x
x   x
xxxxx
x   x
x   x
x   x
Please give the (case-sensitive) alphabetic character of the above
 letter: 
```

Here, it's printed out an `A`, and at the prompt, you should type an
`A`, and then it will proceed with `a`, `B`, `b`, `C`, `c`, etc.

This can be pretty tedious, and most cross stitch alphabets will be
listed in the same order: `A a B b C c D d E e ... X x Y y Z z 0 1 2
... 8 9 . , ! ? '`, or a similar order. The `-a` option will
automatically assign letters based on the above order, and then you
just have to confirm that it is actually the character.

```
 xxx 
x   x
x   x
xxxxx
x   x
x   x
x   x
Would you like to reassign a new character to the above letter
 (current character is A): [y/n] 
```
 
`TODO: Extend the logic for the user interaction`

After assigning all of the characters, the program will end and output
a JSON file, containing your alphabet. You will need this program for
the next step, generating messages.

# Message Generation

Once you have a `json` file containing an alphabet, you can generate a
message. [See the demo](#Demo) for an example.

```
usage: write.py [-h] [--message MESSAGE] [--interactive] [--sep SEP] file

positional arguments:
  file                  The JSON file containing the letters in the cross stitch alphabet you'd like to use

optional arguments:
  -h, --help            show this help message and exit
  --message MESSAGE, -m MESSAGE
                        The message you would like to display in the cross stitch alphabet
  --interactive, -i     Instead of providing a message through the command line, give the message to the program interactively.
  --sep SEP, -s SEP     The separator between columns
```

The `xstitch_abcs.write` requires two arguments, the name of the file
containing the alphabet, and your message. The message generator will
align the baselines of the letters. For instance, typesetting `grow`
will produce:

```
 xxx  xx  xx  x x x 
x  x x   x  x x x x 
x  x x   x  x x x x 
 xxx x    xx   x x 
   x 
xxx 
```

You can see that the baseline of `g` is aligned with the baseline of `row`.



# Current Issues

Things that need to be fixed, including the TODOs above:

- Accounting for ` `, spaces -- if not included (they could be encoded
  with any number of `B`, the transparent baseline character)

