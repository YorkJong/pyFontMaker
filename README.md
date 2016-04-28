# LangConvert #

FontMaker is an open source Python application to generate character pictures
with given font. A character list file lists characters to be generated. This
application also provides color assignment feature and edging/shadowing effect
on generated pictures.

## Install ##

1. Download a binary distribution of FontMaker (e.g.,
   *FontMaker-0.21-bin.zip*) from [Downloads][] page.
2. Uncompress the binary distribution.

[Downloads]: https://bitbucket.org/YorkJong/pyfontmaker/downloads


## Getting Started ##

1. Install FontMaker.
2. Edit the *char.lst*
4. Run `demo.bat`.
    - This will generate *filename.lst* and character pictures.
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

### Sample pictures in *fore* directory ###
![CH_UPP_A.png](https://bitbucket.org/repo/LBeE8q/images/4150482962-CH_UPP_A.png)
![CH_UPP_B.png](https://bitbucket.org/repo/LBeE8q/images/964284856-CH_UPP_B.png)
![CH_UPP_C.png](https://bitbucket.org/repo/LBeE8q/images/577090888-CH_UPP_C.png)
![CH_UPP_D.png](https://bitbucket.org/repo/LBeE8q/images/2647317553-CH_UPP_D.png)
![CH_UPP_E.png](https://bitbucket.org/repo/LBeE8q/images/1037804330-CH_UPP_E.png)

### Sample pictures in *edge* directory ###
![CH_UPP_A.png](https://bitbucket.org/repo/LBeE8q/images/4181468742-CH_UPP_A.png)
![CH_UPP_B.png](https://bitbucket.org/repo/LBeE8q/images/1260088721-CH_UPP_B.png)
![CH_UPP_C.png](https://bitbucket.org/repo/LBeE8q/images/1193707189-CH_UPP_C.png)
![CH_UPP_D.png](https://bitbucket.org/repo/LBeE8q/images/3547108568-CH_UPP_D.png)
![CH_UPP_E.png](https://bitbucket.org/repo/LBeE8q/images/2844905517-CH_UPP_E.png)

### Sample pictures in *shadow11* directory ###
![CH_UPP_A.png](https://bitbucket.org/repo/LBeE8q/images/2890280662-CH_UPP_A.png)
![CH_UPP_B.png](https://bitbucket.org/repo/LBeE8q/images/971463941-CH_UPP_B.png)
![CH_UPP_C.png](https://bitbucket.org/repo/LBeE8q/images/1298220557-CH_UPP_C.png)
![CH_UPP_D.png](https://bitbucket.org/repo/LBeE8q/images/3289542670-CH_UPP_D.png)
![CH_UPP_E.png](https://bitbucket.org/repo/LBeE8q/images/399595151-CH_UPP_E.png)

### Sample pictures in *shadow21* directory ###
![CH_UPP_A.png](https://bitbucket.org/repo/LBeE8q/images/1779304773-CH_UPP_A.png)
![CH_UPP_B.png](https://bitbucket.org/repo/LBeE8q/images/1169028918-CH_UPP_B.png)
![CH_UPP_C.png](https://bitbucket.org/repo/LBeE8q/images/2137979987-CH_UPP_C.png)
![CH_UPP_D.png](https://bitbucket.org/repo/LBeE8q/images/1158313839-CH_UPP_D.png)
![CH_UPP_E.png](https://bitbucket.org/repo/LBeE8q/images/3408953778-CH_UPP_E.png)


## Command Line ##
### Top level ###
```
usage: fontmaker.exe [-h] [-v] {name,fore,edge,shadow11,shadow21} ...

Generate charater pictures with edge/shadow.

positional arguments:
  {name,fore,edge,shadow11,shadow21}
                        commands
    name                Generate a filename-list file according to a char-list
                        file.
    fore                Generate font pictures of only foreground.
    edge                Generate font pictures with 1-pixel edge.
    shadow11            Generate font pictures with shadow of 1 pixel on
                        right, 1 pixel on bottom
    shadow21            Generate font pictures with shadow of 2 pixel on
                        right, 1 pixel on bottom.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
```

### name command ###
```
usage: fontmaker.exe name [-h] [-o <file>] char-list-file

positional arguments:
  char-list-file        The char list file.

optional arguments:
  -h, --help            show this help message and exit
  -o <file>, --outfile <file>
                        assign a <file> to put the filename list. The default
                        <file> is "filename.lst".
```

### fore command ###
```
usage: fontmaker.exe fore [-h] [-n <file>] [-d <directory>] [-f <file>]
                          [-s <number>] [-c <color>]
                          char-list-file

positional arguments:
  char-list-file        The char list file.

optional arguments:
  -h, --help            show this help message and exit
  -n <file>, --name <file>
                        assign a <file> to get the filename list. The default
                        <file> is "filename.lst".
  -d <directory>, --dir <directory>
                        assign the <directory> to store output files. The
                        default directory is "out".
  -f <file>, --font <file>
                        assign a font filename. The default font is
                        "arial.ttf".
  -s <number>, --size <number>
                        assign a font size. The default size is "40".
  -c <color>, --fore <color>
                        assign the <color> of foreground. The default <color>
                        is "white".
```

### edge command ###
```
usage: fontmaker.exe edge [-h] [-n <file>] [-d <directory>] [-f <file>]
                          [-s <number>] [-c <color>] [-e <color>] [-b <color>]
                          char-list-file

positional arguments:
  char-list-file        The char list file.

optional arguments:
  -h, --help            show this help message and exit
  -n <file>, --name <file>
                        assign a <file> to get the filename list. The default
                        <file> is "filename.lst".
  -d <directory>, --dir <directory>
                        assign the <directory> to store output files. The
                        default directory is "out".
  -f <file>, --font <file>
                        assign a font filename. The default font is
                        "arial.ttf".
  -s <number>, --size <number>
                        assign a font size. The default size is "40".
  -c <color>, --fore <color>
                        assign the <color> of foreground. The default <color>
                        is "white".
  -e <color>, --edge <color>
                        assign the <color> of edge/shadow. The default <color>
                        is "gray".
  -b <color>, --back <color>
                        assign the <color> of background. The default <color>
                        is "black".
```

### shadow11 command ###
```
usage: fontmaker.exe shadow11 [-h] [-n <file>] [-d <directory>] [-f <file>]
                              [-s <number>] [-c <color>] [-e <color>]
                              [-b <color>]
                              char-list-file

positional arguments:
  char-list-file        The char list file.

optional arguments:
  -h, --help            show this help message and exit
  -n <file>, --name <file>
                        assign a <file> to get the filename list. The default
                        <file> is "filename.lst".
  -d <directory>, --dir <directory>
                        assign the <directory> to store output files. The
                        default directory is "out".
  -f <file>, --font <file>
                        assign a font filename. The default font is
                        "arial.ttf".
  -s <number>, --size <number>
                        assign a font size. The default size is "40".
  -c <color>, --fore <color>
                        assign the <color> of foreground. The default <color>
                        is "white".
  -e <color>, --edge <color>
                        assign the <color> of edge/shadow. The default <color>
                        is "gray".
  -b <color>, --back <color>
                        assign the <color> of background. The default <color>
                        is "black".
```

### shadow21 command ###
```
usage: fontmaker.exe shadow21 [-h] [-n <file>] [-d <directory>] [-f <file>]
                              [-s <number>] [-c <color>] [-e <color>]
                              [-b <color>]
                              char-list-file

positional arguments:
  char-list-file        The char list file.

optional arguments:
  -h, --help            show this help message and exit
  -n <file>, --name <file>
                        assign a <file> to get the filename list. The default
                        <file> is "filename.lst".
  -d <directory>, --dir <directory>
                        assign the <directory> to store output files. The
                        default directory is "out".
  -f <file>, --font <file>
                        assign a font filename. The default font is
                        "arial.ttf".
  -s <number>, --size <number>
                        assign a font size. The default size is "40".
  -c <color>, --fore <color>
                        assign the <color> of foreground. The default <color>
                        is "white".
  -e <color>, --edge <color>
                        assign the <color> of edge/shadow. The default <color>
                        is "gray".
  -b <color>, --back <color>
                        assign the <color> of background. The default <color>
                        is "black".
```
