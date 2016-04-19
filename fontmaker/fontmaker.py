# -*- coding: utf-8 -*-
"""
Generate charater pictures, character list file, and test message with a font.
"""
__software__ = "Font Maker"
__version__ = "0.01"
__author__ = "Jiang Yu-Kuan <yukuan.jiang@gmail.com>"
__date__ = "2016/04/19 (initial version); 2016/04/19 (last revision)"

import os
from itertools import izip

from PIL import ImageFont, Image, ImageDraw


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

    in_file = open(fn, "rb")
    bs = in_file.read()
    in_file.close()

    if  bs.startswith(BOM_UTF16_LE):
        us = bs.decode("utf_16_le").lstrip(BOM_UTF16_LE.decode("utf_16_le"))
    elif  bs.startswith(BOM_UTF16_BE):
        us = bs.decode("utf_16_be").lstrip(BOM_UTF16_BE.decode("utf_16_be"))
    else:
        us = bs.decode("utf_8").lstrip(BOM_UTF8.decode("utf_8"))

    return us


def save_utf8_file(fn, lines):
    """Save string lines into an UTF8 text files.
    """
    out_file = open(fn, 'w')
    out_file.write("\n".join(lines).encode('utf-8'))
    out_file.close()


def read_char_list(fn):
    lines = read_unicode(fn).splitlines()
    lines = (x.rstrip() for x in lines)
    lines = (x for x in lines if len(x) > 0 and not x.startswith('#'))
    lines = (x for x in lines if not x.startswith(':'))
    chars = []
    for line in lines:
        chars += line

    return chars


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


def gen_ch_pic(ch, font, color='White'):
    canvas = Image.new('RGBA', font.getsize(ch))
    draw = ImageDraw.Draw(canvas)
    draw.text((0,0), ch, font=font, fill=color)
    del draw
    return canvas

#------------------------------------------------------------------------------


def gen_ch():
    h, font = select_font('arial.ttf', 40)
    #h, font = select_font('Monaco.ttf', 40)
    chars = read_char_list('char.lst')
    fns = ['%s.png' % x for x in filename_from_chars(chars)]
    save_utf8_file('res_font.lst', fns)

    dir_name = 'font'
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
    fns = [dir_name + '/' + x for x in fns]
    for ch, fn in zip(chars, fns):
        im = gen_ch_pic(ch, font)
        im.save(fn)


def test_decor():
    import decor
    h, font = select_font('Arial.ttf', 40)
    im = gen_ch_pic('A', font)

    #im = decor.extract_fore(im, fg_color=255)
    #im = decor.add_edge(im, fg_color=255)
    #im = decor.add_shadow11(im, fg_color=255)
    #im = decor.add_shadow21(im, fg_color=255)
    im.show()


def test_font():
    def draw_txt(txt):
        w, h = font.getsize(txt)
        canvas_w, canvas_h = canvas.size
        x = (canvas_w - w) / 2
        print w
        draw.text((x, y[0]), txt, font=font, fill='White')
        y[0] += h

    h, font = select_font('arial.ttf', 40)
    canvas = Image.new('RGBA', (640, 480))
    draw = ImageDraw.Draw(canvas)
    y = [0]

    draw_txt('File Name     Date              Time      ')
    draw_txt('000000C1    2014/10/21    02:12:22')
    canvas.show()


def main():
    #gen_ch()
    #test_font()
    test_decor()

if __name__ == '__main__':
    main()

