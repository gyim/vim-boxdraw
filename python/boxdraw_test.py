from boxdraw import *
from pprint import pprint

# --------- Test utilities --------

def assert_cmd(cmd, cur1, cur2, lines, *args):
    assert len(lines) % 2 == 0
    input_lines = [lines[i] for i in range(0, len(lines), 2)]
    output_lines = [lines[i] for i in range(1, len(lines), 2)]
    y1 = [i for i in range(len(input_lines)) if '1' in input_lines[i]][0]
    y2 = [i for i in range(len(input_lines)) if '2' in input_lines[i]][0]
    x1 = [l.index('1') for l in input_lines if '1' in l][0]
    x2 = [l.index('2') for l in input_lines if '2' in l][0]
    input_lines = [l.replace('1',cur1).replace('2',cur2) for l in input_lines]
    expected = output_lines
    actual = list(cmd(input_lines, y1, x1, y2, x2, *args))
    if expected != actual:
        print "Expected:"
        pprint(expected, width=1)
        print "Actual:"
        pprint(actual, width=1)
    assert expected == actual

# -------- Utility functions --------

def test_expand_line():
    assert expand_line('', 0) == ''
    assert expand_line('\n', 0) == '\n'
    assert expand_line('xx', 1) == 'xx'
    assert expand_line('xx\n', 1) == 'xx\n'
    assert expand_line('xxx\n', 6) == 'xxx   \n'
    assert expand_line('xxx', 6) == 'xxx   '

def test_replace_at():
    assert replace_at('----', 0, 'xx') == 'xx--'
    assert replace_at('----', 1, 'xx') == '-xx-'
    assert replace_at('----', 3, 'xx') == '---xx'
    assert replace_at('----', 3, 'xxx') == '---xxx'
    assert replace_at('----', 3, 'xx\n') == '---xx\n'

def test_overwrite_at():
    assert overwrite_at('----', 0, 'x x ') == 'x-x-'
    assert overwrite_at('----', 1, 'x x ') == '-x-x'
    assert overwrite_at('----', 2, 'x x ') == '--x-x'
    assert overwrite_at('----', 3, 'x x ') == '---x x'
    assert overwrite_at('----\n', 3, 'x x ') == '---x x\n'

def test_replace_block():
    lines = [
        'foo',
        'bar',
        'b',
    ]
    block = [
        '1234',
        '5678',
    ]
    assert list(replace_block(lines, 1, 2, block)) == [
        'foo',
        'ba1234',
        'b 5678',
    ]

def test_line():
    assert line('<->', 0) == ''
    assert line('<->', 1) == '<'
    assert line('<->', 2) == '<-'
    assert line('<->', 3) == '<->'
    assert line('<->', 4) == '<-->'
    assert line('<->', 5) == '<--->'

    assert line([['+---+'], ['|   |'], ['+---+']], 4) == [
        '+---+',
        '|   |',
        '|   |',
        '+---+',
    ]

# -------- Box drawing --------

def test_basic_box_drawing():
    assert_cmd(draw_box, '.', '.', [
        '........', '........',
        '..1.....', '..+---+.',
        '........', '..|   |.',
        '......2.', '..+---+.',
        '........', '........',
    ])

def test_box_drawing_after_line_end():
    assert_cmd(draw_box ,'.', '.', [
        '........', '........',
        '..1.'    , '..+---+',
        ''        , '  |   |',
        '......2' , '..+---+',
    ])

def test_fill_box_alignments():
    assert_cmd(fill_box, ' ', ' ', [
        '+------------+', '+------------+',
        '|1...........|', '|This is a   |',
        '|....FOO.....|', '|test.       |',
        '|............|', '|            |',
        '|...........2|', '|            |',
        '+------------+', '+------------+',
    ], 'top', 'left', 'This is a test.')

    assert_cmd(fill_box, ' ', ' ', [
        '+------------+', '+------------+',
        '|1...........|', '| This is a  |',
        '|....FOO.....|', '|   test.    |',
        '|............|', '|            |',
        '|...........2|', '|            |',
        '+------------+', '+------------+',
    ], 'top', 'center', 'This is a test.')

    assert_cmd(fill_box, ' ', ' ', [
        '+------------+', '+------------+',
        '|1...........|', '|   This is a|',
        '|....FOO.....|', '|       test.|',
        '|............|', '|            |',
        '|...........2|', '|            |',
        '+------------+', '+------------+',
    ], 'top', 'right', 'This is a test.')

    assert_cmd(fill_box, ' ', ' ', [
        '+------------+', '+------------+',
        '|1...........|', '|            |',
        '|....FOO.....|', '| This is a  |',
        '|............|', '|   test.    |',
        '|...........2|', '|            |',
        '+------------+', '+------------+',
    ], 'middle', 'center', 'This is a test.')

    assert_cmd(fill_box, ' ', ' ', [
        '+------------+', '+------------+',
        '|1...........|', '|            |',
        '|....FOO.....|', '|            |',
        '|............|', '|   This is a|',
        '|...........2|', '|       test.|',
        '+------------+', '+------------+',
    ], 'bottom', 'right', 'This is a test.')

def test_fill_box_too_small():
    assert_cmd(fill_box, ' ', ' ', [
        '+-----+', '+-----+', 
        '|1    |', '|not  |', 
        '|    2|', '|enoug|',
        '+-----+', '+-----+', 
    ], 'top', 'left', 'not enough space')

    assert_cmd(fill_box, ' ', ' ', [
        '+-+', '+-+',
        '|1|', '|n|',
        '|.|', '|e|',
        '|2|', '|s|',
        '+-+', '+-+',
    ], 'top', 'left', 'not enough space')

def test_draw_box_with_label():
    assert_cmd(draw_box_with_label, '.', '.', [
        '.........', '.........',
        '.1.......', '.+-----+.',
        '.........', '.| foo |.',
        '.........', '.| bar |.',
        '.......2.', '.+-----+.',
        '.........', '.........',
    ], 'top', 'left', 'foo bar')

# -------- Line drawing --------

def test_arrow_reverse():
    assert arrow_reverse('---') == '---'
    assert arrow_reverse('<->') == '<->'
    assert arrow_reverse('-->') == '<--'
    assert arrow_reverse('<--') == '-->'

def test_draw_ling_hv():
    assert_cmd(draw_line_hv, ' ', ' ', [
        ' 1    2 ', ' o----> ',
    ], 'o->')

    assert_cmd(draw_line_hv, ' ', ' ', [
        ' 2    1 ', ' <----o ',
    ], 'o->')

    assert_cmd(draw_line_hv, ' ', ' ', [
        ' ', ' ',
        '1', 'o',
        ' ', '|',
        ' ', '|',
        '2', 'v',
    ], 'o->')

    assert_cmd(draw_line_hv, ' ', ' ', [
        ' ', ' ',
        '2', '^',
        ' ', '|',
        ' ', '|',
        '1', 'o',
    ], 'o->')

    assert_cmd(draw_line_hv, ' ', ' ', [
        '        ', '        ',
        ' 1      ', ' o----+ ',
        '        ', '      | ',
        '      2 ', '      v ',
        '        ', '        ',
    ], 'o->')

    assert_cmd(draw_line_hv, ' ', ' ', [
        '        ', '        ',
        ' 2      ', ' ^      ',
        '        ', ' |      ',
        '      1 ', ' +----o ',
        '        ', '        ',
    ], 'o->')

    assert_cmd(draw_line_hv, ' ', ' ', [
        '        ', '        ',
        '      1 ', ' +----o ',
        '        ', ' |      ',
        ' 2      ', ' v      ',
        '        ', '        ',
    ], 'o->')

    assert_cmd(draw_line_hv, ' ', ' ', [
        '        ', '        ',
        '      2 ', '      ^ ',
        '        ', '      | ',
        ' 1      ', ' o----+ ',
        '        ', '        ',
    ], 'o->')

def test_draw_ling_vh():
    assert_cmd(draw_line_vh, ' ', ' ', [
        ' 1    2 ', ' o----> ',
    ], 'o->')

    assert_cmd(draw_line_vh, ' ', ' ', [
        ' 2    1 ', ' <----o ',
    ], 'o->')

    assert_cmd(draw_line_vh, ' ', ' ', [
        ' ', ' ',
        '1', 'o',
        ' ', '|',
        ' ', '|',
        '2', 'v',
    ], 'o->')

    assert_cmd(draw_line_vh, ' ', ' ', [
        ' ', ' ',
        '2', '^',
        ' ', '|',
        ' ', '|',
        '1', 'o',
    ], 'o->')

    assert_cmd(draw_line_vh, ' ', ' ', [
        '        ', '        ',
        ' 1      ', ' o      ',
        '        ', ' |      ',
        '      2 ', ' +----> ',
        '        ', '        ',
    ], 'o->')

    assert_cmd(draw_line_vh, ' ', ' ', [
        '        ', '        ',
        ' 2      ', ' <----+ ',
        '        ', '      | ',
        '      1 ', '      o ',
        '        ', '        ',
    ], 'o->')

    assert_cmd(draw_line_vh, ' ', ' ', [
        '        ', '        ',
        '      1 ', '      o ',
        '        ', '      | ',
        ' 2      ', ' <----+ ',
        '        ', '        ',
    ], 'o->')

    assert_cmd(draw_line_vh, ' ', ' ', [
        '        ', '        ',
        '      2 ', ' +----> ',
        '        ', ' |      ',
        ' 1      ', ' o      ',
        '        ', '        ',
    ], 'o->')

def test_draw_line_auto():
    assert_cmd(draw_line_auto, ' ', ' ', [
        '       |', '       |',
        '      2|', ' +---->|',
        '       |', ' |     |',
        ' 1      ', ' o      ',
        '        ', '        ',
    ], 'o->')

    assert_cmd(draw_line_auto, ' ', ' ', [
        '     ---', '     ---',
        '      2 ', '      ^ ',
        '        ', '      | ',
        ' 1      ', ' o----+ ',
        '        ', '        ',
    ], 'o->')

def test_line_start_plus():
    assert_cmd(draw_line_auto, '-', ' ', [
        '       |', '       |',
        '      2|', ' +---->|',
        '       |', ' |     |',
        '-1-     ', '-+-     ',
        '        ', '        ',
    ], '-->')

    assert_cmd(draw_line_auto, '+', ' ', [
        '       |', '       |',
        '      2|', ' +---->|',
        '       |', ' |     |',
        '-1-     ', '-+-     ',
        ' |      ', ' |      ',
    ], '-->')

    assert_cmd(draw_line_auto, '|', ' ', [
        '     ---', '     ---',
        '      2 ', '      ^ ',
        ' |      ', ' |    | ',
        ' 1      ', ' +----+ ',
        ' |      ', ' |      ',
    ], '-->')

