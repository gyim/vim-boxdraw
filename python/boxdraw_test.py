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
    assert replace_at('----', 3, 'xx\n') == '---xx\n'

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

