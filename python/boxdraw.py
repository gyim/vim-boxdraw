#!/usr/bin/env python
import textwrap

# -------- Utility functions --------

def split_nl(line):
    if len(line) > 0 and line[-1] == '\n':
        return line[:-1], line[-1]
    else:
        return line, ''

def expand_line(line, width):
    line, nl = split_nl(line)
    if len(line) < width:
        line += ' ' * (width-len(line))
    return line + nl

def replace_at(line, pos, s):
    line = expand_line(line, pos + len(s))
    return line[:pos] + s + line[pos+len(s):]

def align_h(line, width, where):
    line, nl = split_nl(line)
    if where == 'left':
        fmt = '{:<%ds}' % width
    elif where == 'right':
        fmt = '{:>%ds}' % width
    else:
        fmt = '{:^%ds}' % width
    return fmt.format(line[:width]) + nl

def align_v(lines, height, where):
    lines = lines[:height]
    if where == 'top':
        lines += [''] * (height - len(lines))
    elif where == 'bottom':
        lines = [''] * (height - len(lines)) + lines
    else:
        lines = [''] * ((height - len(lines)) // 2) + lines
        lines += [''] * (height - len(lines))

    return lines

# -------- Box drawing --------

def draw_box(lines, y1, x1, y2, x2):
    "Draws a box and clears its contents with spaces."
    y1, y2 = min(y1,y2), max(y1,y2)
    x1, x2 = min(x1,x2), max(x1,x2)
    w = x2 - x1 + 1
    h = y2 - y1 + 1

    for l, line in enumerate(lines):
        if w < 3 or h < 3:
            yield line
        elif l == y1 or l == y2:
            yield replace_at(line, x1, '+' + '-'*(w-2) + '+')
        elif y1 < l < y2:
            yield replace_at(line, x1, '|' + ' '*(w-2) + '|')
        else:
            yield line

def fill_box(lines, y1, x1, y2, x2, yalign, xalign, text):
    "Fills a rectangular area with text."
    y1, y2 = min(y1,y2), max(y1,y2)
    x1, x2 = min(x1,x2), max(x1,x2)
    w = x2 - x1 + 1
    h = y2 - y1 + 1
    if w > 0:
        text = textwrap.wrap(text, w, break_long_words=False)
        text = [align_h(l, w, xalign) for l in text]
        text = align_v(text, h, yalign)
    else:
        text = []

    for l, line in enumerate(lines):
        if y1 <= l <= y2:
            line = replace_at(line, x1, ' ' * w)
        if y1 <= l < y1+len(text):
            line = replace_at(line, x1, text[l-y1])
        yield line

def draw_box_with_label(lines, y1, x1, y2, x2, yalign, xalign, text):
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

