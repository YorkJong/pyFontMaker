# -*- coding: utf-8 -*-
"""
FontMaker is an open source Python application to generate character pictures
with given font. A character list file lists characters to be generated. This
application also provides color assignment features and edging/shadowing effects
on generacted pictures.
"""
__software__ = "Font Maker"
__version__ = "0.21"
__author__ = "Jiang Yu-Kuan <yukuan.jiang@gmail.com>"
__date__ = "2016/04/19 (initial version); 2016/04/28 (last revision)"

import os
import sys
from itertools import izip
import argparse

from PIL import ImageFont, Image, ImageDraw, ImageColor

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

def select_font(filename, height):
    """
    Return an (actual height, font) pair with given truetype font file and
    the upper bound of height.

    Arguments
    ---------
    filename
        a filename of a truetype font
    height
        the upper bound of height of the givent font
    """
    for i in xrange(MAX_FONT_SIZE, MIN_FONT_SIZE-1, -1):
        font = ImageFont.truetype(filename, i)
        w, h = font.getsize('W')    # Character 'W' may be the largest one.
        if h <= height:
            break
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

def gen_fore_pics(chars, filenames, font, color):
    def gen_ch_pic(ch, font, fg_color):
        canvas = Image.new('RGBA', font.getsize(ch))
        draw = ImageDraw.Draw(canvas)
        draw.text((0,0), ch, font=font, fill=fg_color)
        del draw
        return canvas

    for ch, fn in zip(chars, filenames):
        im = gen_ch_pic(ch, font, color)
        im.save(fn)


def _gen_ch_pic(ch, font, fg_level, bg_level):
    canvas = Image.new('L', font.getsize(ch), bg_level)
    draw = ImageDraw.Draw(canvas)
    draw.text((0,0), ch, font=font, fill=fg_level)
    del draw
    return canvas


def _apply_color(im, fg_level, eg_level, bg_level):
    im = im.convert('P', palette=Image.ADAPTIVE, colors=3)
    im.putpalette(list(bg_level) + list(eg_level) + list(fg_level))
    return im


def gen_edge_pics(chars, filenames, font, fg_color, eg_color, bg_color):
    fg_level, eg_level, bg_level = 0, 128, 255
    for ch, fn in zip(chars, filenames):
        im = _gen_ch_pic(ch, font, fg_level, bg_level)
        im = decor.add_edge(im, fg_level, eg_level, bg_level)
        im = _apply_color(im, fg_color, eg_color, bg_color)
        im.save(fn, transparency=0)


def gen_shadow11_pics(chars, filenames, font, fg_color, eg_color, bg_color):
    fg_level, eg_level, bg_level = 0, 128, 255
    for ch, fn in zip(chars, filenames):
        im = _gen_ch_pic(ch, font, fg_level, bg_level)
        im = decor.add_shadow11(im, fg_level, eg_level, bg_level)
        im = _apply_color(im, fg_color, eg_color, bg_color)
        im.save(fn, transparency=0)


def gen_shadow21_pics(chars, filenames, font, fg_color, eg_color, bg_color):
    fg_level, eg_level, bg_level = 0, 128, 255
    for ch, fn in zip(chars, filenames):
        im = _gen_ch_pic(ch, font, fg_level, bg_level)
        im = decor.add_shadow21(im, fg_level, eg_level, bg_level)
        im = _apply_color(im, fg_color, eg_color, bg_color)
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
        gen_fore_pics(args.chars, fns, font, args.fore)

    def do_edge(args):
        fns = ['{}/{}'.format(args.dir, fn) for fn in args.filenames]
        h, font = select_font(args.font, args.size)
        gen_edge_pics(args.chars, fns, font, args.fore, args.edge, args.back)

    def do_shadow11(args):
        fns = ['{}/{}'.format(args.dir, fn) for fn in args.filenames]
        h, font = select_font(args.font, args.size)
        gen_shadow11_pics(args.chars, fns, font,
                          args.fore, args.edge, args.back)

    def do_shadow21(args):
        fns = ['{}/{}'.format(args.dir, fn) for fn in args.filenames]
        h, font = select_font(args.font, args.size)
        gen_shadow21_pics(args.chars, fns, font,
                          args.fore, args.edge, args.back)

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

    # create the parent parser of edge/shadow color
    edge = argparse.ArgumentParser(add_help=False)
    edge.set_defaults(edge='gray')
    edge.add_argument('-e', '--edge', metavar='<color>', type=rgb,
        help='''assign the <color> of edge/shadow.
            The default <color> is "%s".
            ''' % edge.get_default('edge'))

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

    # create the parent parser of font name
    size = argparse.ArgumentParser(add_help=False)
    size.set_defaults(size=40)
    size.add_argument('-s', '--size', metavar='<number>',
        type=int, choices=range(MIN_FONT_SIZE, MAX_FONT_SIZE+1),
        help='''assign a font size.
            The default size is "%d".
            ''' % size.get_default('size'))

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
        parents=[src, name, dir, font, size, fore],
        help='Generate font pictures of only foreground.')
    sub.set_defaults(func=do_fore)

    # create the parser for the "edge" command
    sub = subparsers.add_parser('edge',
        parents=[src, name, dir, font, size, fore, edge, back],
        help='Generate font pictures with 1-pixel edge.')
    sub.set_defaults(func=do_edge)

    # create the parser for the "shadow11" command
    sub = subparsers.add_parser('shadow11',
        parents=[src, name, dir, font, size, fore, edge, back],
        help='''Generate font pictures with shadow of 1 pixel on right, 1 pixel
            on bottom''')
    sub.set_defaults(func=do_shadow11)

    # create the parser for the "shadow21" command
    sub = subparsers.add_parser('shadow21',
        parents=[src, name, dir, font, size, fore, edge, back],
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

    fg_level, eg_level, bg_level = 0, 128, 255
    im = _gen_ch_pic('A', font, fg_level, bg_level)
    im.save('A0.png')

    #im = decor.add_edge(im, fg_level, eg_level, bg_level)
    #im = decor.add_shadow11(im, fg_level, eg_level, bg_level)
    im = decor.add_shadow21(im, fg_level, eg_level, bg_level)

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

