# -*- coding: utf-8 -*-
"""
This tool decorates OSD .BMP file, e.g., add, shadows
"""
__software__ = "OSD Decorate"
__version__ = "1.1"
__author__ = "Jiang Yu-Kuan <yukuan.jiang@gmail.com>"
__date__ = "2012/03/19 (initial version); 2016/04/19 (last revision)"

import argparse
import sys
import os
import glob

from PIL import Image, ImageFilter

clBLACK = 0
clWHITE = 255

clEDGE = 64
clFORE = 192


def extract_fore(im, fg_color):
    """Extract foreground from an image
    """
    #im.convert('L')
    im = im.point(lambda x: x == fg_color and fg_color)
    return im


def make_mask(im, bg_color):
    """Make a mask from an image
    """
    return im.point(lambda x: x != bg_color and clWHITE).convert('L')


def find_edge(im, fg_color):
    """Find and mask out the dege
    """
    w, h = im.size
    im_out = Image.new('L', (w + 2, h + 2))
    im_out.paste(im, (1, 1))
    im_out = im_out.point(lambda x: x != fg_color and clWHITE)
    im_out = im_out.filter(ImageFilter.FIND_EDGES)
    im_out = im_out.crop((1, 1, 1 + w, 1 + h))
    return im_out


def add_edge(im, fg_color=clFORE, eg_color=clEDGE):
    """Add edge to an image
    """
    im = extract_fore(im, fg_color)
    mask = find_edge(im, fg_color)
    edge = mask.point(lambda x: x == clWHITE and eg_color)
    im.paste(edge, (0, 0), mask)
    return im


def add_shadow11(im, fg_color=clFORE, eg_color=clEDGE):
    """Add shadow of 1 pixel on right, 1 pixel on bottom
    """
    shadow = im.point(lambda x: x == fg_color and eg_color)
    mask = shadow.point(lambda x: x == eg_color and clWHITE).convert('L')

    w, h = im.size
    out = Image.new('L', (w + 1, h + 1))
    out.paste(shadow, (0, 0))           # umbra
    out.paste(shadow, (1, 1), mask)     # penumbra
    out.paste(extract_fore(im, fg_color), (0, 0), mask)
    out = out.crop((0, 0, w, h))
    return out


def add_shadow21(im, fg_color=clFORE, eg_color=clEDGE):
    """Add shadow of 2 pixels on right, 1 pixel on bottom
    """
    shadow = im.point(lambda x: x == fg_color and eg_color)
    mask = make_mask(shadow, bg_color=clBLACK)

    w, h = im.size
    out = Image.new('L', (w + 2, h + 1))
    out.paste(shadow, (1, 0))           # umbra
    out.paste(shadow, (2, 1), mask)     # penumbra
    out.paste(extract_fore(im, fg_color), (0, 0), mask)
    out = out.crop((0, 0, w, h))
    return out


#------------------------------------------------------------------------------

def parse_args(args):
    # create top-level parser
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-v', '--version', action='version',
                        version='%s v%s by %s' %
                        (__software__, __version__, __author__))
    subparsers = parser.add_subparsers(help='commands')

    # create the parser for the "edge" command
    sub = subparsers.add_parser('edge',
        help='add edge with 1 pixel width')
    sub.set_defaults(op=add_edge, pattern='*.BMP', dir='.')
    sub.add_argument('pattern', nargs='?',
        help='''file pattern with simple shell-style wildcards to match
            pictures to add edge. The default pattern is "%s".
            ''' % sub.get_default('pattern'))
    sub.add_argument('-d', '--dir', metavar='<directory>',
        help='''assign the <directory> to store pictures after adding edge.
            The default directory is "%s".
            ''' % sub.get_default('dir'))

    # create the parser for the "shadow11" command
    sub = subparsers.add_parser('shadow11',
        help='add shadow of 1 pixel on right, 1 pixel on bottom')
    sub.set_defaults(op=add_shadow11, pattern='*.BMP', dir='.')
    sub.add_argument('pattern', nargs='?',
        help='''file pattern with simple shell-style wildcards to match
            pictures to add shadow. The default pattern is "%s".
            ''' % sub.get_default('pattern'))
    sub.add_argument('-d', '--dir', metavar='<directory>',
        help='''assign the <directory> to store pictures after adding shadow.
            The default directory is "%s".
            ''' % sub.get_default('dir'))

    # create the parser for the "shadow21" command
    sub = subparsers.add_parser('shadow21',
        help='add shadow of 2 pixels on right, 1 pixel on bottom')
    sub.set_defaults(op=add_shadow21, pattern='*.BMP', dir='.')
    sub.add_argument('pattern', nargs='?',
        help='''file pattern with simple shell-style wildcards to match
            pictures to add shadow. The default pattern is "%s".
            ''' % sub.get_default('pattern'))
    sub.add_argument('-d', '--dir', metavar='<directory>',
        help='''assign the <directory> to store pictures after adding shadow.
            The default directory is "%s".
            ''' % sub.get_default('dir'))

    # parse args and execute functions
    args = parser.parse_args(args)

    # operation and saving
    for filename in glob.glob(unicode(args.pattern)):
        im = Image.open(open(filename, 'rb'))
        im = args.op(im)
        filename = os.path.basename(filename)
        im.save(u'%s/%s' % (args.dir, filename))


def main():
    """Start point of this module.
    """
    try:
        parse_args(sys.argv[1:])
    except IOError as err:
        print err
    except ValueError as err:
        print err

if __name__ == '__main__':
    main()
    #parse_args(sys.argv[1:])
