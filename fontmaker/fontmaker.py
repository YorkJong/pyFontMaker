# -*- coding: utf-8 -*-
"""
Generate charater pictures, character list file, and test message with a font.
"""
__software__ = "Font Maker"
__version__ = "0.01"
__author__ = "Jiang Yu-Kuan <yukuan.jiang@gmail.com>"
__date__ = "2016/04/19 (initial version); 2016/04/25 (last revision)"

import os
import sys
from itertools import izip
import argparse

from PIL import ImageFont, Image, ImageDraw, ImageColor

import decor

#------------------------------------------------------------------------------

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
    for i in xrange(70, 7, -1):
        font = ImageFont.truetype(filename, i)
        w, h = font.getsize('W')    # Character 'W' may be the largest one.
        if h <= height:
            break
    return h, font


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


def gen_ch_pic(ch, font, color='White'):
    canvas = Image.new('RGBA', font.getsize(ch))
    draw = ImageDraw.Draw(canvas)
    draw.text((0,0), ch, font=font, fill=color)
    del draw
    return canvas

#------------------------------------------------------------------------------

def gen_fore_pics(chars, filenames, font, color):
    for ch, fn in zip(chars, filenames):
        im = gen_ch_pic(ch, font, color)
        im.save(fn)


def _apply_color(im, fg_color, eg_color):
    im = im.convert('L')
    im = im.convert('P', palette=Image.ADAPTIVE, colors=3, dither=Image.NONE)
    bg_color = ImageColor.getrgb('black')
    im.putpalette(list(fg_color) + list(eg_color) + list(bg_color))
    return im


def gen_edge_pics(chars, filenames, font, fg_color, eg_color):
    for ch, fn in zip(chars, filenames):
        im = gen_ch_pic(ch, font, 'White')
        im = decor.add_edge(im, fg_color=255, eg_color=128)
        im = _apply_color(im, fg_color, eg_color)
        im.save(fn, transparency=2)


def gen_shadow11_pics(chars, filenames, font, fg_color, eg_color):
    for ch, fn in zip(chars, filenames):
        im = gen_ch_pic(ch, font, 'White')
        im = decor.add_shadow11(im, fg_color=255, eg_color=128)
        im = _apply_color(im, fg_color, eg_color)
        im.save(fn, transparency=2)


def gen_shadow21_pics(chars, filenames, font, fg_color, eg_color):
    for ch, fn in zip(chars, filenames):
        im = gen_ch_pic(ch, font, 'White')
        im = decor.add_shadow21(im, fg_color=255, eg_color=128)
        im = _apply_color(im, fg_color, eg_color)
        im.save(fn, transparency=2)

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
        pass

    def do_fore(args):
        fns = ['{}/{}'.format(args.dir, fn) for fn in args.filenames]
        h, font = select_font(args.font, args.size)
        gen_fore_pics(args.chars, fns, font, args.fore)

    def do_edge(args):
        fns = ['{}/{}'.format(args.dir, fn) for fn in args.filenames]
        h, font = select_font(args.font, args.size)
        gen_edge_pics(args.chars, fns, font, args.fore, args.edge)

    def do_shadow11(args):
        fns = ['{}/{}'.format(args.dir, fn) for fn in args.filenames]
        h, font = select_font(args.font, args.size)
        gen_shadow11_pics(args.chars, fns, font, args.fore, args.edge)

    def do_shadow21(args):
        fns = ['{}/{}'.format(args.dir, fn) for fn in args.filenames]
        h, font = select_font(args.font, args.size)
        gen_shadow21_pics(args.chars, fns, font, args.fore, args.edge)

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
        type=int, choices=range(7, 200),
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
        parents=[src, name, dir, font, size, fore, edge],
        help='Generate font pictures with 1-pixel edge.')
    sub.set_defaults(func=do_edge)

    # create the parser for the "shadow11" command
    sub = subparsers.add_parser('shadow11',
        parents=[src, name, dir, font, size, fore, edge],
        help='''Generate font pictures with shadow of 1 pixel on right, 1 pixel
            on bottom''')
    sub.set_defaults(func=do_shadow11)

    # create the parser for the "shadow21" command
    sub = subparsers.add_parser('shadow21',
        parents=[src, name, dir, font, size, fore, edge],
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
    im = gen_ch_pic('A', font)

    #im = decor.extract_fore(im, fg_color=255)
    #im = decor.add_edge(im, fg_color=255, eg_color=128)
    im = decor.add_shadow11(im, fg_color=255, eg_color=128)
    #im = decor.add_shadow21(im, fg_color=255, eg_color=128)

    #lum = im.convert('L')
    #alpha = lum.point(lambda x: x != 0 and 255)
    #im = Image.merge('RGBA', (lum, lum, lum, alpha))
    #im = im.convert('P')
    im = im.convert('RGB')
    im = im.convert('P', palette=Image.ADAPTIVE, colors=4, dither=Image.NONE)

    bg = ImageColor.getrgb('black')
    fg = ImageColor.getrgb('red')
    eg = ImageColor.getrgb('green')
    im.putpalette(list(bg) + list(fg) + list(eg))
    im.save('A1.png', transparency=2)


if __name__ == '__main__':
    #main()
    parse_args(sys.argv[1:])
    #test()

