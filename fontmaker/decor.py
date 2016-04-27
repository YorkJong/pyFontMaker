# -*- coding: utf-8 -*-
"""
This tool decorates OSD .BMP file, e.g., add, shadows
"""
__software__ = "OSD Decorate"
__version__ = "1.1"
__author__ = "Jiang Yu-Kuan <yukuan.jiang@gmail.com>"
__date__ = "2012/03/19 (initial version); 2016/04/28 (last revision)"

import argparse
import sys
import os
import glob

from PIL import Image, ImageFilter

clBLACK = 0
clWHITE = 255

clEDGE = 64
clFORE = 192


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


def add_edge(im, fg_color=clFORE, eg_color=clEDGE, bg_color=clBLACK):
    """Add edge to an image
    """
    out = im.copy()
    mask = im.point(lambda x: x != bg_color and clWHITE).convert('L')
    out.paste(im, (0, 0), mask)
    mask = find_edge(im, fg_color)
    edge = mask.point(lambda x: x == clWHITE and eg_color)
    out.paste(edge, (0, 0), mask)
    return out


def add_shadow11(im, fg_color=clFORE, eg_color=clEDGE, bg_color=clBLACK):
    """Add shadow of 1 pixel on right, 1 pixel on bottom
    """
    shadow = im.point(lambda x: x == fg_color and eg_color)
    mask = im.point(lambda x: x == fg_color and clWHITE).convert('L')

    w, h = im.size
    out = Image.new('L', (w + 1, h + 1), bg_color)
    out.paste(shadow, (1, 0), mask)     # umbra
    out.paste(shadow, (1, 1), mask)     # penumbra
    out.paste(im, (0, 0), mask)         # foreground
    out = out.crop((0, 0, w, h))
    return out


def add_shadow21(im, fg_color=clFORE, eg_color=clEDGE, bg_color=clBLACK):
    """Add shadow of 2 pixels on right, 1 pixel on bottom
    """
    shadow = im.point(lambda x: x == fg_color and eg_color)
    mask = im.point(lambda x: x == fg_color and clWHITE).convert('L')

    w, h = im.size
    out = Image.new('L', (w + 2, h + 1), bg_color)
    out.paste(shadow, (1, 0), mask)     # umbra
    out.paste(shadow, (2, 1), mask)     # penumbra
    out.paste(im, (0, 0), mask)         # foreground
    out = out.crop((0, 0, w, h))
    return out

