# -*- coding: utf-8 -*-
"""
This tool decorates OSD .BMP file, e.g., add, shadows
"""
__software__ = "OSD Decorate"
__version__ = "1.1"
__author__ = "Jiang Yu-Kuan <yukuan.jiang@gmail.com>"
__date__ = "2016/04/19 (initial version); 2016/04/28 (last revision)"

import argparse
import sys
import os
import glob

from PIL import Image, ImageFilter


def _find_edge(im, fg_level, bg_level):
    """Find and mask out the edge
    """
    w, h = im.size
    im_out = Image.new('L', (w + 2, h + 2), bg_level)
    im_out.paste(im, (1, 1))
    im_out = im_out.point(lambda x: x != fg_level and 255)
    im_out = im_out.filter(ImageFilter.FIND_EDGES)
    im_out = im_out.crop((1, 1, 1 + w, 1 + h))
    return im_out


def add_edge(im, fg_level, eg_level, bg_level):
    """Add edge to an image
    """
    assert fg_level != eg_level != bg_level

    out = im.copy()
    mask = im.point(lambda x: x != bg_level and 255).convert('L')
    out.paste(im, (0, 0), mask)     # foreground

    mask = _find_edge(im, fg_level, bg_level)
    edge = mask.point(lambda x: x == 255 and eg_level)
    out.paste(edge, (0, 0), mask)   # edge

    return out


def add_shadow11(im, fg_level, eg_level, bg_level):
    """Add shadow of 1 pixel on right, 1 pixel on bottom
    """
    assert fg_level != eg_level != bg_level

    shadow = im.point(lambda x: x == fg_level and eg_level)
    mask = im.point(lambda x: x == fg_level and 255).convert('L')

    w, h = im.size
    out = Image.new('L', (w + 1, h + 1), bg_level)
    out.paste(shadow, (1, 0), mask)     # umbra
    out.paste(shadow, (1, 1), mask)     # penumbra
    out.paste(im, (0, 0), mask)         # foreground

    out = out.crop((0, 0, w, h))
    return out


def add_shadow21(im, fg_level, eg_level, bg_level):
    """Add shadow of 2 pixels on right, 1 pixel on bottom
    """
    assert fg_level != eg_level != bg_level

    shadow = im.point(lambda x: x == fg_level and eg_level)
    mask = im.point(lambda x: x == fg_level and 255).convert('L')

    w, h = im.size
    out = Image.new('L', (w + 2, h + 1), bg_level)
    out.paste(shadow, (1, 0), mask)     # umbra
    out.paste(shadow, (2, 1), mask)     # penumbra
    out.paste(im, (0, 0), mask)         # foreground

    out = out.crop((0, 0, w, h))
    return out

