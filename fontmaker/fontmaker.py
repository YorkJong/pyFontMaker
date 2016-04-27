# -*- coding: utf-8 -*-
"""
Generate charater pictures, character list file, and test message with a font.
"""
__software__ = "Font Maker"
__version__ = "0.01"
__author__ = "Jiang Yu-Kuan <yukuan.jiang@gmail.com>"
__date__ = "2016/04/19 (initial version); 2016/04/25 (last revision)"

import os
from itertools import izip

from PIL import ImageFont, Image, ImageDraw, ImageColor


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

    with open(fn, "rb") as f:
        bs = f.read()

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


def test_decor():
    import decor
    h, font = select_font('arial.ttf', 40)
    im = gen_ch_pic('A', font)

    #im = decor.extract_fore(im, fg_color=255)
    im = decor.add_edge(im, fg_color=255, eg_color=128)
    #im = decor.add_shadow11(im, fg_color=255)
    #im = decor.add_shadow21(im, fg_color=255)

    lum = im.convert('L')
    #alpha = lum.point(lambda x: x != 0 and 255)
    #im = Image.merge('RGBA', (lum, lum, lum, alpha))
    #im = im.convert('P')
    im = im.convert('P', palette=Image.ADAPTIVE, colors=3, dither=Image.NONE)
    bg = ImageColor.getrgb('black')
    fg = ImageColor.getrgb('red')
    eg = ImageColor.getrgb('green')
    im.putpalette(list(bg) + list(fg) + list(eg))
    im.save('A.png', transparency=0)


def main():
    #test_decor()
    fns = read_filename_list('../bin/filename.lst')
    print fns
    chars = read_char_list('../bin/char.lst')
    assert len(fns) == len(chars)


if __name__ == '__main__':
    main()

