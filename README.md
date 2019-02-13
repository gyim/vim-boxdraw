# vim-boxdraw - Draw ASCII diagrams in Vim

## Introduction

[![See vim-boxdraw in action](https://asciinema.org/a/qeig6TH6N4uteq7J6n4epUGaq.png)](https://asciinema.org/a/qeig6TH6N4uteq7J6n4epUGaq)

The vim-boxdraw plugin makes it easy to draw simple ASCII diagrams in
`blockwise-visual` mode. The basic idea is simple:

- Select a rectangle on the screen
- Invoke a draw command.

All commands are mapped to the `+` prefix. See the
[vim help file](doc/boxdraw.txt) for reference.

## Installation

| Method         | Instalation instructions                                                      |
| -------------- | ------------------------------------------------------------------------------|
| [NeoBundle][1] | Add `NeoBundle 'gyim/vim-boxdraw'` to `.vimrc`                                |
| [Pathogen][2]  | Run `git clone https://github.com/gyim/vim-boxdraw ~/.vim/bundle/vim-boxdraw` |
| [Plug][3]      | Add `Plug 'gyim/vim-boxdraw' ` to `.vimrc`                                    |
| [Vundle][4]    | Add `Plugin 'gyim/vim-boxdraw'` to `.vimrc`                                   |

[1]: https://github.com/Shougo/neobundle.vim
[2]: https://github.com/tpope/vim-pathogen
[3]: https://github.com/junegunn/vim-plug
[4]: https://github.com/gmarik/vundle

## Contributions
### Developer Setup
vim-boxdraw uses a Python script to do most of the work. To contribute to this plugin, you'll need

  - Python 2.7.x and 3.5.x (we want to support system Python on most platforms)
  - `pip install -U pytest`

#### Running the unit tests

From the `python` directory, 

    pytest

