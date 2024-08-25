# djvu2char_index
Create character index for a DjVu document

Designed by Janusz S. Bień (jsbien@uw.edu.pl).
To be implemented by ChatGPT.

The program at present doesn't accept as the input an DjVu document,
but the hidden text in the format used by the djvused program. We call
it briefly the dsed format and use 'dsed' as file extension.

The djvused format is described in the man page of the program,
cf. e.g.  https://djvu.sourceforge.net/doc/man/djvused.html.

The file starts with a 'select' command followed by the document file
name and the 'set-txt' command followed by the text representation,
which is described in the following excerpt:

START QUOTE

Djvused uses a simple parenthesized syntax to represent both
annotations and hidden text.

The building blocks of the hidden text syntax are lists representing
each structural component of the hidden text. Structural components
have the following form:

    (type xmin ymin xmax ymax ... ) 

 The symbol type must be one of page, column, region, para, line,
 word, or char, listed here by decreasing order of importance. The
 integers xmin, ymin, xmax, and ymax represent the coordinates of a
 rectangle indicating the position of the structural component in the
 page. Coordinates are measured in pixels and have their origin at the
 bottom left corner of the page. The remaining expressions in the list
 either is a single string representing the encoded text associated
 with this structural component, or is a sequence of structural
 components with a lesser type.

The hidden text for each page is simply represented by a single
structural element of type page. Various level of structural
information are acceptable. For instance, the page level component
might only specify a page level string, or might only provide a list
of lines, or might provide a full hierarchy down to the individual
characters.

END QUOTE

The dsed file for a document is created with ocrodjvu program,
cf.https://github.com/FriedrichFroebel/ocrodjvu. The following
invocation is used:

ocrodjvu -e tesseract -t chars --save-script=<document name>.dsed  -l lat <document name>

The '-l' (language) parameter can be changed, if needed, from 'lat'
(Latin) to some other language code supported by Tesseract, cf.
https://github.com/tesseract-ocr/tesseract/blob/main/doc/tesseract.1.asc#languages-and-scripts

Here is an example of a dsed file:

select 'Hochfeder-08_PT01_020.djvu' set-txt (page 0 0 3360 906 (column
17 72 3217 844 (para 49 673 3197 844 (line 49 673 3197 844 (word 49
681 3197 840 (char 49 721 159 837 "a") (char 177 720 316 840 "x")
(char 330 719 412 827 "c") [...]

For every character representation we need to do two things:

1. Determine its location in the document by counting pages, columns,
paragraphs. lines (both in paragraphs and on the page), words and the
character position in the word. All counting starts at 1.

So for (char 49 721 159 837 "a") we get
'p 1 c 1 pa 1 l 1 1 w 1 c 1'

2. Convert the character coordinates to the format used by the djview4
program, cf. e.g.  https://github.com/barak/djview4.

Here are the relenat excerpts from the man page (https://djvu.sourceforge.net/doc/man/djview4.html)

START QUOTE

    A local DjVu document URL of the form: 
    file:///path/name.djvu[?djvuopts&keyword=value&...] 

The square brackets delimit the optional components of the
URL.

-highlight=x,y,w,h[,color]

Display a highlighted rectangle at the specified coordinates in the
current page and with the specified color. Coordinates x, y, w, and h
are measured in document image coordinates (not screen
coordinates). The origin is set at the bottom left corner of the
image. The color color must be given in hexadecimal RRGGBB or #RRGGBB
format. 

END QUOTE

'w' and 'h' stand of course for width and height.

We don't use colors and skip the path, so for (char 49 721 159 837 "a")
we get

Hochfeder-02_PT01_020bisOCR.djvu?djvuopts=&page=1&highlight=49,721,110,116

The document name comes from the 'select' command mentioned earlier,
and the page number comes from the count described in the previous
paragraph.

The final step to consolidate all the relevant data into an index
supported by 'djview4poliqarp' program
(https://github.com/jsbien/djview-poliqarp_fork). For the time being
the best description of the index format can be found in the my paper
"Towards an inventory of old print characters: Ungler’s Rubricella, a
case study" (http://dx.doi.org/10.47397/tb/44-3/tb138bien-rubricella).

Here are the relevant fragments:

START QUOTE

From the technical point of view the indexes
are just simple CSV files (using semicolon as the
separator). Every line of an index file consists of
three or four fields:

1. The text used for sorting and incremental search.

2. The reference to the relevant image fragment in
the form used by the djview4 viewer mentioned
earlier, namely a Universal Resource Locator.
[...]

3. A description: text displayed for the current
entry in a small window under the index.

4. An optional comment displayed after the entry;
we precede it by ※ (U+203B reference mark)
for a more distinctive display.

END QUOTE

In our case we decide that the first element will be the cgaracter
itself, the third element will be its location, and the fourth the
base name of the file document preceded by a single space and ※. For
example:

a;file:Hochfeder-02_PT01_020bisOCR.djvu?djvuopts=&page=1&highlight=49,721,110,116;p 1 c 1 pa 1 l 1 1 w 1 c 1; ※ Hochfeder-02_PT01_020bisOCR

The name of the index should the document base name with the extension
csv, e.g. Hochfeder-02_PT01_020bisOCR.csv.


