# FontMaker #

FontMaker is an open source Python application to generate character pictures
with given font. A character list file lists characters to be generated. This
application also provides color assignment feature and edging/shadowing effect
on generated pictures.

## Install ##

1. Download a binary distribution of FontMaker (e.g.,
   *FontMaker-0.24-bin.zip*) from [Downloads][] page.
2. Uncompress the binary distribution.

[Downloads]: https://bitbucket.org/YorkJong/pyfontmaker/downloads


## Getting Started ##

1. Install FontMaker.
2. Edit the *char.lst*
3. Edit the `demo.bat`
4. Run `demo.bat`.
    - This will generate *filename.lst* and character pictures.
    - The character pictures are classified with specific directories
        - *fore* directory contains undecorated/raw character pictures.
        - *outline* directory contains those pictures with adding outline.
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

### A sample *demo.bat* ###
```batch
@echo off
set fontmaker=fontmaker.exe


set outfile=filename.lst
echo =^> Generate a filename list file (%outfile%).
%fontmaker% name -o%outfile% char.lst

set name=%outfile%
set chars=char.lst
set font=arial.ttf

set dir=fore
echo =^> Generate font picture of only foreground.
%fontmaker% fore -n%name% -d%dir% -cGreen -f%font% -s40 %chars%

set dir=outline
echo =^> Generate font pictures with 1-pixel outline.
%fontmaker% outline -n%name% -d%dir% -cRed -lGreen -f%font% -s40 %chars%

set dir=shadow11
echo =^> Generate font pictures with 1x1 shadow.
%fontmaker% shadow11 -n%name% -d%dir% -cRed -lGreen -f%font% -s40 %chars%

set dir=shadow21
echo =^> Generate font pictures with 2x1 shadow.
%fontmaker% shadow21 -n%name% -d%dir% -cRed -lGreen -f%font% -s40 %chars%

pause
```

### Sample pictures in *fore* directory ###
![CH_UPP_A.png](https://bitbucket.org/repo/LBeE8q/images/4150482962-CH_UPP_A.png)
![CH_UPP_B.png](https://bitbucket.org/repo/LBeE8q/images/964284856-CH_UPP_B.png)
![CH_UPP_C.png](https://bitbucket.org/repo/LBeE8q/images/577090888-CH_UPP_C.png)
![CH_UPP_D.png](https://bitbucket.org/repo/LBeE8q/images/2647317553-CH_UPP_D.png)
![CH_UPP_E.png](https://bitbucket.org/repo/LBeE8q/images/1037804330-CH_UPP_E.png)

### Sample pictures in *outline* directory ###
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
usage: fontmaker.exe [-h] [-v] {name,fore,outline,shadow11,shadow21} ...

Generate charater pictures with outline/shadow.

positional arguments:
  {name,fore,outline,shadow11,shadow21}
                        commands
    name                Generate a filename-list file according to a char-list
                        file.
    fore                Generate font pictures of only foreground.
    outline             Generate font pictures with 1-pixel outline.
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
  -H, --fixed           turn on the switch to use fixed height of the font.
```

### outline command ###
```
usage: fontmaker.exe outline [-h] [-n <file>] [-d <directory>] [-f <file>]
                             [-s <number>] [-c <color>] [-l <color>] [-b <color>]
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
  -l <color>, --outline <color>
                        assign the <color> of outline/shadow. The default <color>
                        is "gray".
  -b <color>, --back <color>
                        assign the <color> of background. The default <color>
                        is "black".
  -H, --fixed           turn on the switch to use fixed height of the font.
```

### shadow11 command ###
```
usage: fontmaker.exe shadow11 [-h] [-n <file>] [-d <directory>] [-f <file>]
                              [-s <number>] [-c <color>] [-l <color>]
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
  -l <color>, --outline <color>
                        assign the <color> of outline/shadow. The default
                        <color> is "gray".
  -b <color>, --back <color>
                        assign the <color> of background. The default <color>
                        is "black".
  -H, --fixed           turn on the switch to use fixed height of the font.
```

### shadow21 command ###
```
usage: fontmaker.exe shadow21 [-h] [-n <file>] [-d <directory>] [-f <file>]
                              [-s <number>] [-c <color>] [-l <color>]
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
  -l <color>, --outline <color>
                        assign the <color> of outline/shadow. The default
                        <color> is "gray".
  -b <color>, --back <color>
                        assign the <color> of background. The default <color>
                        is "black".
  -H, --fixed           turn on the switch to use fixed height of the font.
```
