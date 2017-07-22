#!/usr/bin/env python
import textwrap
from pprint import pprint

# -------- Utility functions --------

def block_pos(y1, x1, y2, x2):
    "Returns y, x, height, width"
    return min(y1,y2), min(x1,x2), max(y1,y2) - min(y1,y2) + 1, max(x1,x2) - min(x1,x2) + 1

def split_nl(line):
    "Returns the contents of the line without the newline, and the newline if exists."
    if len(line) > 0 and line[-1] == '\n':
        return line[:-1], line[-1]
    else:
        return line, ''

def expand_line(line, width):
    "Ensures that line is at least `width` character long."
    line, nl = split_nl(line)
    if len(line) < width:
        line += ' ' * (width-len(line))
    return line + nl

def replace_at(line, pos, s):
    "Replaces part of the line starting at `pos`."
    line = expand_line(line, pos + len(s))
    return line[:pos] + s + line[pos+len(s):]

def replace_block(lines, y, x, block):
    "Replaces a rectangular block inside the given lines."
    h = len(block)
    w = max(len(line) for line in block) if h>0 else 0

    for l, line in enumerate(lines):
        line, nl = split_nl(line)
        if h > 0 and w > 0 and y <= l < y+h:
            yield replace_at(line, x, block[l-y]) + nl
        else:
            yield line

def line(pattern, w):
    "Returns pattern enlarged to fit width `w`"
    result = pattern[0] + pattern[1] * max(1, w-2) + pattern[2]
    return result[:w]

def align_h(line, width, where):
    "Returns fixed-width, aligned text. Text is trucated if longer than width."
    line, nl = split_nl(line)
    if where == 'left':
        fmt = '{:<%ds}' % width
    elif where == 'right':
        fmt = '{:>%ds}' % width
    else:
        fmt = '{:^%ds}' % width
    return fmt.format(line[:width]) + nl

def align_v(lines, height, where, empty):
    "Adds empty lines before/after the given `lines` according to alignment."
    lines = lines[:height]
    if where == 'top':
        lines += [empty] * (height - len(lines))
    elif where == 'bottom':
        lines = [empty] * (height - len(lines)) + lines
    else:
        lines = [empty] * ((height - len(lines)) // 2) + lines
        lines += [empty] * (height - len(lines))

    return lines

# -------- Box drawing --------

def draw_box(lines, y1, x1, y2, x2):
    "Draws a box and clears its contents with spaces."
    y, x, h, w = block_pos(y1, x1, y2, x2)
    box = line([[line('+-+',w)], [line('| |',w)], [line('+-+',w)]], h)
    return replace_block(lines, y, x, box)

def fill_box(lines, y1, x1, y2, x2, yalign, xalign, text):
    "Fills a rectangular area with text."
    y, x, h, w = block_pos(y1, x1, y2, x2)
    if h > 0 and w > 0:
        text = textwrap.wrap(text, w, break_long_words=False)
        text = [align_h(l, w, xalign) for l in text]
        text = align_v(text, h, yalign, line('   ', w))
        return replace_block(lines, y, x, text)
    else:
        return lines

def draw_box_with_label(lines, y1, x1, y2, x2, yalign, xalign, text):
    "Draws a box and fills it with text."
    y1, y2 = min(y1,y2), max(y1,y2)
    x1, x2 = min(x1,x2), max(x1,x2)

    lines = draw_box(lines, y1, x1, y2, x2)
    if x2-x1 > 2:
        lines = fill_box(lines, y1+1, x1+2, y2-1, x2-2, yalign, xalign, text)
    return lines

# -------- Main --------

CMDS = {
    '+o': [draw_box],
    '+O': [draw_box_with_label, 'middle', 'center'],
    '+[O': [draw_box_with_label, 'middle', 'left'],
    '+]O': [draw_box_with_label, 'middle', 'right'],
    '+{[O': [draw_box_with_label, 'top', 'left'],
    '+{]O': [draw_box_with_label, 'top', 'right'],
    '+}[O': [draw_box_with_label, 'bottom', 'left'],
    '+}]O': [draw_box_with_label, 'bottom', 'right'],

    '+c': [fill_box, 'middle', 'center'],
    '+[c': [fill_box, 'middle', 'left'],
    '+]c': [fill_box, 'middle', 'right'],
    '+{[c': [fill_box, 'top', 'left'],
    '+{]c': [fill_box, 'top', 'right'],
    '+}[c': [fill_box, 'bottom', 'left'],
    '+}]c': [fill_box, 'bottom', 'right'],
}

if __name__ == '__main__':
    import sys
    cmd, y1, x1, y2, x2 = sys.argv[1:6]
    y1, x1, y2, x2 = int(y1), int(x1), int(y2), int(x2)

    f = CMDS[cmd][0]
    args = CMDS[cmd][1:] + sys.argv[6:]

    lines = sys.stdin.readlines()
    for line in f(lines, y1, x1, y2, x2, *args):
        sys.stdout.write(line)

