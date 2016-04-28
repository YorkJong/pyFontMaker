# LangConvert #

FontMaker is an open source Python application to generate character pictures
with given font. A character list file lists characters to be generated. This
application also provides color assignment feature and edging/shadowing effect
on generacted pictures.

## Install ##

1. Download a binary distribution of FontMaker (e.g.,
   *FontMaker-0.21-bin.zip*) from [Downloads][] page.
2. Uncompress the binary distribution.

[Downloads]: https://bitbucket.org/YorkJong/pyfontmaker/downloads


## Getting Started ##

1. Install FontMaker.
2. Edit the *char.lst*
4. Run `demo.bat`.
    - This will generate filename.lst and character pictures.
    - The character pictures are classified with specific directories
        - *fore* directory contains undecorated/raw character pictures.
        - *edge* directory contains those pictures with adding edge.
        - *shadow11* directory contains those pictures with light shadow.
        - *shadow21* directory contains those pictures with enhanced shadow.

### Note ###
- Run `clean.bat` to remove generated files.

### A sample *char.lst* ###
```sh
# A sample character list file

 !"#$%&'()*+,-./0123456789:;<=>?
@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_
`abcdefghijklmnopqrstuvwxyz{|}~
```
- The character list file lists characters to be generated.
- A line prefixing `#` denotes a comment line.


