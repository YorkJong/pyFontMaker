# -*- coding: utf-8 -*-
"""
FontMaker is an open source Python application to generate character pictures
with given font. A character list file lists characters to be generated. This
application also provides color assignment features and edging/shadowing effects
on generated pictures.
"""
__software__ = "Font Maker"
__version__ = "0.24"
__author__ = "Jiang Yu-Kuan <yukuan.jiang@gmail.com>"
__date__ = "2016/04/19 (initial version); 2019/03/20 (last revision)"

import os
import sys
from itertools import izip
import argparse

from PIL import ImageFont, Image, ImageDraw, ImageColor
from PIL import BdfFontFile, PcfFontFile

import decor

#------------------------------------------------------------------------------
# Text File Read/Write
#------------------------------------------------------------------------------

def read_unicode(fn):
    """Read an Unicode file that may encode with utf_16_le, utf_16_be, or utf_8.
    """
    from codecs import BOM_UTF16_LE, BOM_UTF16_BE, BOM_UTF8

    with open(fn, "rb") as in_file:
        bs = in_file.read()

    if  bs.startswith(BOM_UTF16_LE):
        us = bs.decode("utf_16_le").lstrip(BOM_UTF16_LE.decode("utf_16_le"))
    elif  bs.startswith(BOM_UTF16_BE):
        us = bs.decode("utf_16_be").lstrip(BOM_UTF16_BE.decode("utf_16_be"))
    else:
        us = bs.decode("utf_8").lstrip(BOM_UTF8.decode("utf_8"))

    return us


def read_char_list(fn):
    lines = read_unicode(fn).splitlines()
    lines = (x.rstrip() for x in lines)
    lines = (x for x in lines if len(x) > 0 and not x.startswith('#'))
    lines = (x for x in lines if not x.startswith(':'))
    chars = []
    for line in lines:
        chars += line

    return chars


def read_filename_list(fn):
    lines = read_unicode(fn).splitlines()
    lines = (x.rstrip() for x in lines)
    lines = (x for x in lines if len(x) > 0 and not x.startswith('#'))
    lines = (x for x in lines if not x.startswith(':'))

    return list(lines)

#------------------------------------------------------------------------------

def save_utf8_file(fn, lines):
    """Save string lines into an UTF8 text files.
    """
    with open(fn, 'w') as out_file:
        out_file.write("\n".join(lines).encode('utf-8'))

#------------------------------------------------------------------------------
# Misc
#------------------------------------------------------------------------------

MIN_FONT_SIZE = 7
MAX_FONT_SIZE = 100


def font_max_size(font):
    """Return maxima (width, height) of a font between char ' ' to char '~'.

    Arguments
    ---------
    font (ImageFont)
        An ImageFont
    """
    w_max, h_max = 0, 0
    for i in range(ord(' '), ord('~')+1):
        w, h = font.getsize(chr(i))
        if w > w_max:
            w_max = w
        if h > h_max:
            h_max = h
    return w_max, h_max


def gen_pil_if_necessary(filename):
    """Generate PIL bitmap font if the input is a X Window bitmap font (.bdf
    or .pcf); and return the modified (if conversion happen) filename.
    """
    f_main, f_ext = os.path.splitext(filename)

    if f_ext.lower() in ['.bdf', '.pcf']:
        with open(filename, 'rb') as f:
            try:
                p = PcfFontFile.PcfFontFile(f)
            except SyntaxError:
                f.seek(0)
                p = BdfFontFile.BdfFontFile(f)
            p.save(filename)
            filename = f_main + '.pil'
    return filename


def select_font(filename, height):
    """
    Return an (actual height, font) pair with given truetype font file (or PIL
    bitmap font file) and the upper bound of width.

    Arguments
    ---------
    filename (str)
        The font filename. It can be a TrueType (.ttf) or OpenType (.otf)
        fonts. It also can be a X Window bitmap font (.bdf, .pcf) or PIL bitmap
        font (.pil).
    height (int)
        the upper bound of height of the givent font
    """
    filename = gen_pil_if_necessary(filename)
    if filename.lower().endswith('.pil'):
        font = ImageFont.load(filename)
        w, h = font_max_size(font)
    else:
        for i in xrange(height*3/2, MIN_FONT_SIZE-1, -1):
            font = ImageFont.truetype(filename, i)
            w, h = font_max_size(font)
            if h <= height:
                break
    #print "[INF] Font:{}; size:{}".format(filename, i)
    #ascent, descent = font.getmetrics()
    #(width, baseline), (offset_x, offset_y) = font.font.getsize(text)
    return h, font

#------------------------------------------------------------------------------

def sym_name(char):
    """Name a *char* if it is a reserved char in a filename on MS Windows.

    Example
    -------
    >>> sym_name('<')
    'less'
    >>> sym_name('A')
    'A'
    """
    sym_chars = r''' !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~'''
    names = ['space', 'exclam', 'dquotes', 'sharp', 'dollar', 'percent',
            'ampersand', 'quote', 'LParenthesis', 'RParenthesis', 'asterisk',
            'plus', 'comma', 'minus', 'period', 'slash', 'colon', 'semicolon',
            'less', 'equal', 'greater', 'question', 'at', 'LBracket',
            'backslash', 'RBracket', 'caret', 'underscore', 'grave', 'LBrace',
            'pipe', 'RBrace', 'tilde']

    name_from_char = dict(izip(sym_chars, names))
    return name_from_char.get(char, char)


def filename_from_chars(chars):
    low_if_low = lambda x: 'LOW_' + x if len(x)==1 and x.islower() else x
    upp_if_upp = lambda x: 'UPP_' + x if len(x)==1 and x.isupper() else x
    num_if_num = lambda x: 'NUM_' + x if len(x)==1 and x.isdigit() else x
    sym_if_sym = lambda x: 'SYM_' + sym_name(x) if len(x)==1 else x

    # apply name mangling
    chars = [low_if_low(x) for x in chars]
    chars = [upp_if_upp(x) for x in chars]
    chars = [num_if_num(x) for x in chars]
    chars = [sym_if_sym(x) for x in chars]
    return ['CH_'+x for x in chars]

#------------------------------------------------------------------------------
# Picture Generaors
#------------------------------------------------------------------------------

def gen_fore_pics(chars, filenames, font, color, fixed_height):
    """Generate pictures drawing given characters.

    Arguments
    ---------
    chars (str)
        List characters to draw.
    filenames (str, str...)
        List filenames of characters.
    font (ImageFont)
        A font to draw.
    color (ImageColor)
        The color of drawing characters.
    fixed_height (bool)
        Decide if use the maxima height to draw the character.
    """
    def gen_ch_pic(ch, font, fg_color):
        ch_w, ch_h = font.getsize(ch)
        if fixed_height:
            w, ch_h = font.getsize('g')     # get the max height of the font
        size = (ch_w, ch_h)
        canvas = Image.new('RGBA', size)
        draw = ImageDraw.Draw(canvas)
        draw.text((0,0), ch, font=font, fill=fg_color)
        del draw
        return canvas

    for ch, fn in zip(chars, filenames):
        im = gen_ch_pic(ch, font, color)
        im.save(fn)


def _gen_ch_pic(ch, font, fg_level, bg_level, fixed_height=True):
    """Generate an image drawing a given character.

    Arguments
    ---------
    ch (str)
        a character to draw.
    font (ImageFont)
        the font.
    fg_level (0..255)
        the level for foregournd color.
    bg_level (0..255)
        the level of background color
    fixed_height (bool)
        Decide if use the maxima height to draw the character.
    """
    ch_w, ch_h = font.getsize(ch)
    if fixed_height:
        w, ch_h = font.getsize('g')     # get the max height of the font
    size = (ch_w, ch_h)
    im = Image.new('1', size, color=1)
    draw = ImageDraw.Draw(im)
    draw.text((0, 0), ch, font=font, color=0)
    del draw
    im = im.convert('L')
    mask = im.point(lambda x: x == 0 and 255)
    text = mask.point(lambda x: x == 255 and fg_level)
    im = Image.new('L', size, bg_level)
    im.paste(text, (0, 0), mask)
    return im


def _apply_color(im, fg_color, ol_color, bg_color):
    """Put a palette for an image with given colors.
    """
    # using Image.ADAPTIVE to avoid dithering
    im = im.convert('P', palette=Image.ADAPTIVE, colors=3)

    # Index begins from maximal color value down to minimal color value
    im.putpalette(list(bg_color) + list(ol_color) + list(fg_color))
    return im


def gen_outline_pics(chars, filenames, font,
                  fg_color, ol_color, bg_color, fixed_height):
    """Genarate a character image with a generated outline.
    """
    fg_level, ol_level, bg_level = 0, 128, 255
    for ch, fn in zip(chars, filenames):
        im = _gen_ch_pic(ch, font, fg_level, bg_level, fixed_height)
        im = decor.add_outline(im, fg_level, ol_level, bg_level)
        im = _apply_color(im, fg_color, ol_color, bg_color)
        im.save(fn, transparency=0)


def gen_shadow11_pics(chars, filenames, font,
                      fg_color, ol_color, bg_color, fixed_height):
    """Genarate a character image with a generated 1x1 shadow.
    """
    fg_level, ol_level, bg_level = 0, 128, 255
    for ch, fn in zip(chars, filenames):
        im = _gen_ch_pic(ch, font, fg_level, bg_level, fixed_height)
        im = decor.add_shadow11(im, fg_level, ol_level, bg_level)
        im = _apply_color(im, fg_color, ol_color, bg_color)
        im.save(fn, transparency=0)


def gen_shadow21_pics(chars, filenames, font,
                      fg_color, ol_color, bg_color, fixed_height):
    """Genarate a character image with a generated 2x1 shadow.
    """
    fg_level, ol_level, bg_level = 0, 128, 255
    for ch, fn in zip(chars, filenames):
        im = _gen_ch_pic(ch, font, fg_level, bg_level, fixed_height)
        im = decor.add_shadow21(im, fg_level, ol_level, bg_level)
        im = _apply_color(im, fg_color, ol_color, bg_color)
        im.save(fn, transparency=0)

#------------------------------------------------------------------------------
# Command Line Interface
#------------------------------------------------------------------------------

def parse_args(args):
    def check_dir(name):
        """Check if the given directory is existing.
        """
        if not os.path.isdir(name):
            os.makedirs(name)
        return name

    def rgb(color):
        return ImageColor.getrgb(color)

    def do_name(args):
        fns = ['%s.png' % x for x in filename_from_chars(args.chars)]
        save_utf8_file(args.outfile, fns)

    def do_fore(args):
        fns = ['{}/{}'.format(args.dir, fn) for fn in args.filenames]
        h, font = select_font(args.font, args.size)
        gen_fore_pics(args.chars, fns, font, args.fore, args.fixed)

    def do_outline(args):
        fns = ['{}/{}'.format(args.dir, fn) for fn in args.filenames]
        h, font = select_font(args.font, args.size)
        gen_outline_pics(args.chars, fns, font,
                      args.fore, args.outline, args.back, args.fixed)

    def do_shadow11(args):
        fns = ['{}/{}'.format(args.dir, fn) for fn in args.filenames]
        h, font = select_font(args.font, args.size)
        gen_shadow11_pics(args.chars, fns, font,
                          args.fore, args.outline, args.back, args.fixed)

    def do_shadow21(args):
        fns = ['{}/{}'.format(args.dir, fn) for fn in args.filenames]
        h, font = select_font(args.font, args.size)
        gen_shadow21_pics(args.chars, fns, font,
                          args.fore, args.outline, args.back, args.fixed)

    #--------------------------------------------------------------------------

    # create top-level parser
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-v', '--version', action='version',
                        version='%s v%s by %s' %
                        (__software__, __version__, __author__))
    subparsers = parser.add_subparsers(help='commands')

    # create the parent parser of src
    src = argparse.ArgumentParser(add_help=False)
    src.add_argument('chars', metavar='char-list-file',
        type=read_char_list,
        help='The char list file.')

    # create the parent parser of filename-list file
    name = argparse.ArgumentParser(add_help=False)
    name.set_defaults(name='filename.lst')
    name.add_argument('-n', '--name', metavar='<file>',
        dest='filenames', type=read_filename_list,
        help='''assign a <file> to get the filename list.
            The default <file> is "%s".
            ''' % name.get_default('name'))

    # create the parent parser of output dir
    dir = argparse.ArgumentParser(add_help=False)
    dir.set_defaults(dir='out')
    dir.add_argument('-d', '--dir', metavar='<directory>', type=check_dir,
        help='''assign the <directory> to store output files.
            The default directory is "%s".
            ''' % dir.get_default('dir'))

    # create the parent parser of foreground color
    fore = argparse.ArgumentParser(add_help=False)
    fore.set_defaults(fore='white')
    fore.add_argument('-c', '--fore', metavar='<color>', type=rgb,
        help='''assign the <color> of foreground.
            The default <color> is "%s".
            ''' % fore.get_default('fore'))

    # create the parent parser of outline/shadow color
    outline = argparse.ArgumentParser(add_help=False)
    outline.set_defaults(outline='gray')
    outline.add_argument('-l', '--outline', metavar='<color>', type=rgb,
        help='''assign the <color> of outline/shadow.
            The default <color> is "%s".
            ''' % outline.get_default('outline'))

    # create the parent parser of background color
    back = argparse.ArgumentParser(add_help=False)
    back.set_defaults(back='black')
    back.add_argument('-b', '--back', metavar='<color>', type=rgb,
        help='''assign the <color> of background.
            The default <color> is "%s".
            ''' % back.get_default('back'))

    # create the parent parser of font name
    font = argparse.ArgumentParser(add_help=False)
    font.set_defaults(font='arial.ttf')
    font.add_argument('-f', '--font', metavar='<file>',
        help='''assign a font filename.
            The default font is "%s".
            ''' % font.get_default('font'))

    # create the parent parser of size
    size = argparse.ArgumentParser(add_help=False)
    size.set_defaults(size=40)
    size.add_argument('-s', '--size', metavar='<number>',
        type=int, choices=range(MIN_FONT_SIZE, MAX_FONT_SIZE+1),
        help='''assign a font size.
            The default size is "%d".
            ''' % size.get_default('size'))

    # create the parent parser of fixed font height
    fixed = argparse.ArgumentParser(add_help=False)
    fixed.set_defaults(fixed=False)
    fixed.add_argument('-H', '--fixed', action='store_true',
        help='''turn on the switch to use fixed height of the font.''')

    #--------------------------------------------------------------------------

    # create the parser for the "name" command
    sub = subparsers.add_parser('name', parents=[src],
        help='Generate a filename-list file according to a char-list file.')
    sub.set_defaults(func=do_name, outfile='filename.lst')
    sub.add_argument('-o', '--outfile', metavar='<file>',
        help='''assign a <file> to put the filename list.
            The default <file> is "%s".
            ''' % sub.get_default('outfile'))

    # create the parser for the "fore" command
    sub = subparsers.add_parser('fore',
        parents=[src, name, dir, font, size, fore, fixed],
        help='Generate font pictures of only foreground.')
    sub.set_defaults(func=do_fore)

    # create the parser for the "outline" command
    sub = subparsers.add_parser('outline',
        parents=[src, name, dir, font, size, fore, outline, back, fixed],
        help='Generate font pictures with 1-pixel outline.')
    sub.set_defaults(func=do_outline)

    # create the parser for the "shadow11" command
    sub = subparsers.add_parser('shadow11',
        parents=[src, name, dir, font, size, fore, outline, back, fixed],
        help='''Generate font pictures with shadow of 1 pixel on right, 1 pixel
            on bottom''')
    sub.set_defaults(func=do_shadow11)

    # create the parser for the "shadow21" command
    sub = subparsers.add_parser('shadow21',
        parents=[src, name, dir, font, size, fore, outline, back, fixed],
        help='''Generate font pictures with shadow of 2 pixel on right, 1 pixel
            on bottom.''')
    sub.set_defaults(func=do_shadow21)

    #--------------------------------------------------------------------------

    # parse args and execute functions
    args = parser.parse_args(args)
    args.func(args)


def main():
    """Start point of this module.
    """
    try:
        parse_args(sys.argv[1:])
    except IOError as err:
        print err
    except ValueError as err:
        print err


def test():
    import decor
    h, font = select_font('arial.ttf', 40)

    fg_level, ol_level, bg_level = 0, 128, 255
    im = _gen_ch_pic('A', font, fg_level, bg_level)
    im.save('A0.png')

    #im = decor.add_outline(im, fg_level, ol_level, bg_level)
    #im = decor.add_shadow11(im, fg_level, ol_level, bg_level)
    im = decor.add_shadow21(im, fg_level, ol_level, bg_level)

    im = im.convert('P', palette=Image.ADAPTIVE, colors=3)
    im.save('A1.png')

    bg = ImageColor.getrgb('black')
    fg = ImageColor.getrgb('red')
    eg = ImageColor.getrgb('green')
    im.putpalette(list(bg) + list(eg) + list(fg))
    im.save('A2.png', transparency=0)

    os.system('pause')


if __name__ == '__main__':
    main()
    #parse_args(sys.argv[1:])
    #test()

