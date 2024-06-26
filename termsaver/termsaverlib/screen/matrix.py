# -*- coding: utf-8 -*-
###############################################################################
#
# file:     matrix.py
#
# Purpose:  refer to python doc for documentation details.
#
# Note:     This file is part of Termsaver application, and should not be used
#           or executed separately.
#
###############################################################################
#
# Copyright 2012 Termsaver
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
###############################################################################
"""
This module contains a fancy screen that displays falling text with Japanese
characters similar to the Matrix movie. See additional information in the
class itself.

See more details of the movie in here:
http://en.wikipedia.org/wiki/The_Matrix

The screen class available here is:

    * `MatrixScreen`
"""

import argparse
#
# Python mobdules
#
import random
import time

from termsaver.termsaverlib import constants, exception
from termsaver.termsaverlib.i18n import _
#
# Internal modules
#
from termsaver.termsaverlib.screen.base import ScreenBase
from termsaver.termsaverlib.screen.helper.position import PositionHelperBase


class MatrixScreen(ScreenBase, PositionHelperBase):
    """
    Fancy screen that displays falling Japanese and alpha - numeric characters
    simulating the Matrix movie.

    The Japanese characters are based on the Japanese Katakana phonetic
    letters. See more info in Wikipedia: http://en.wikipedia.org/wiki/Katakana

    From its base classes, the functionality provided here bases on the
    settings defined below:

        * clean up each cycle: False
          to give a sense of continuity, there will be no screen cleaning up
    """

    line_delay = None
    """
    Defines the line printing delay, to give a cool visual of a
    moving screen. This value is measured in seconds, and default marks are
    defined as 30 x `constants.Settings.LINE_DELAY_SECONDS`.
    """

    granularity = 10
    """
    Defines an integer value that represents the granularity in which the
    characters will be displayed on screen, moving from very sparse (1) to
    very dirty (100).

    Default value should be 10, which gives a nice look with the algorithm
    executed in `get_char_list`.
    """

    space_zenkaku = '　'  # WARNING: This is NOT a simple space char
    """
    Represent a full-width space character, used to fill in the blanks on the
    screen and guarantee good positioning.
    See more information about full-width characters in:
    http://en.wikipedia.org/wiki/Halfwidth_and_Fullwidth_Forms
    """

    space_hangaku = ' '
    """
    Represent a half-width space character, used to fill in the blanks on the
    screen and guarantee good positioning.
    See more information about full-width characters in:
    http://en.wikipedia.org/wiki/Halfwidth_and_Fullwidth_Forms
    """

    digmap_alpha_num_zenkaku = [
        '０', '１', '２', '３', '４', '５', '６', '７', '８', '９',
        'Ａ', 'Ｂ', 'Ｃ', 'Ｄ', 'Ｅ', 'Ｆ', 'Ｇ', 'Ｈ', 'Ｉ', 'Ｊ',
        'Ｋ', 'Ｌ', 'Ｍ', 'Ｎ', 'Ｏ', 'Ｐ', 'Ｑ', 'Ｒ', 'Ｓ', 'Ｔ',
        'Ｕ', 'Ｖ', 'Ｗ', 'Ｘ', 'Ｙ', 'Ｚ',
    ]
    """
    Holds the list of alpha-numeric characters, formatted with full-width
    formatting, to ensure char positioning on the screen during display.
    See more information about this at:
    http://en.wikipedia.org/wiki/Halfwidth_and_Fullwidth_Forms
    """

    digmap_alpha_num_hangaku = [
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
        'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
        'U', 'V', 'X', 'W', 'Y', 'Z',
    ]
    """
    Holds the list of alpha-numeric characters, formatted with half-width
    formatting, to ensure char positioning on the screen during display.
    See more information about this at:
    http://en.wikipedia.org/wiki/Halfwidth_and_Fullwidth_Forms
    """

    digmap_kana_hangaku = [
        'ｱ', 'ｲ', 'ｳ', 'ｴ', 'ｵ', 'ｶ', 'ｷ', 'ｸ', 'ｹ', 'ｺ', 'ｻ', 'ｼ', 'ｽ', 'ｾ', 'ｿ', 
        'ﾀ', 'ﾁ', 'ﾂ', 'ﾃ', 'ﾄ', 'ﾅ', 'ﾆ', 'ﾇ', 'ﾈ', 'ﾉ', 'ﾊ', 'ﾋ', 'ﾌ', 'ﾍ', 'ﾎ', 'ﾏ', 
        'ﾐ', 'ﾑ', 'ﾒ', 'ﾓ', 'ﾔ', 'ﾕ', 'ﾖ', 'ﾗ', 'ﾘ', 'ﾙ', 'ﾚ', 'ﾛ', 'ﾜ', 'ﾝ', 'ｦ', 'ｰ', 
    ]
    """
    Holds the list of Japanese Katakana used to display the screensaver.
    Based on information available on Wikipedia:
    http://en.wikipedia.org/wiki/Katakana
    All characters here are formatted with half-width
    formatting, to ensure char positioning on the screen during display.
    See more information about this at:
    http://en.wikipedia.org/wiki/Halfwidth_and_Fullwidth_Forms
    """

    digmap_kana_zenkaku = [
        'ア', 'イ', 'ウ', 'エ', 'オ', 'カ', 'キ', 'ク', 'ケ', 'コ',
        'サ', 'シ', 'ス', 'セ', 'ソ', 'タ', 'チ', 'ツ', 'テ', 'ト',
        'ナ', 'ニ', 'ヌ', 'ネ', 'ノ',  'ハ', 'ヒ', 'フ', 'ヘ', 'ホ',
        'マ', 'ミ', 'ム', 'メ', 'モ', 'ヤ', 'ユ', 'ヨ',
        'ラ', 'リ', 'ル', 'レ', 'ロ', 'ワ', 'ヰ', 'ヱ', 'ヲ', 'ン', 'ー',
    ]
    """
    Holds the list of Japanese Katakana used to display the screensaver.
    Based on information available on Wikipedia:
    http://en.wikipedia.org/wiki/Katakana
    All characters here are formatted with full-width
    formatting, to ensure char positioning on the screen during display.
    See more information about this at:
    http://en.wikipedia.org/wiki/Halfwidth_and_Fullwidth_Forms
    """

    space = ""
    """
    The actual space property used for blank printing. This will be based on
    `space_hangaku`, unless specified otherwise.
    """

    digmap = []
    """
    The actual property used for character picking. This will be based on
    both `digmap_alpha_num_*` and `digmap_kana_*` value, unless specified
    otherwise.
    """

    screen_map = []
    """
    The mapping of xy position and length of each line. This will hold the
    randomized values that are show on screen line by line.
    """
    
    use_zenkaku = False
    """
    Defines if all characters and size calculations should be done for
    full-width or half-width.
    """
    
    proportion = 1
    """
    Defines the granulation proportion for displaying characters in full-width
    of half-width size.
    """
    
    use_kana_only = False
    
    def __init__(self, parser = None):
        """
        The constructor of this class.
        """
        ScreenBase.__init__(self,
            "matrix",
            _("displays a matrix movie alike screensaver"),
            parser
        )

        if self.parser:
            self.parser.add_argument("-g", "--granularity",
                help="An integer value to define how dirt should the screen be. 1 - clean, 100 total dirt.",
                action="store",
                default=self.granularity
            )
            self.parser.add_argument("-k", "--kana",
                help="Displays only Japanese characters (excludes alpha numeric)",
                action="store_true",
                default=self.use_kana_only
            )
            self.parser.add_argument("-d", "--delay",
                help="Defines the speed (in seconds) of the character movement",
                default=30 * constants.Settings.CHAR_DELAY_SECONDS
            )
            self.parser.add_argument("-z", "--zenkaku",
                help="Displays full-width (fattish) Japanese characters.",
                action="store_true",
                default=self.use_zenkaku
            )
        self.cleanup_per_cycle = False

        # set defaults
        if self.line_delay is None:
            self.line_delay = 30 * constants.Settings.CHAR_DELAY_SECONDS


    def _run_cycle(self):
        """
        Executes a cycle of this screen.
        """

        # Identify terminal geometry
        self.get_terminal_size()
        
        if len(self.screen_map) == 0 or self.changed_geometry:
            # build it for the first time or whenever the geometry changes
            self.__build_screen_map()

        print(self.print_line())
        time.sleep(self.line_delay)

    def _parse_args(self, launchScreenImmediately=True):
        """
        Handles the special command-line arguments available for this screen.
        Although this is a base screen, having these options prepared here
        can save coding for screens that will not change the default options.
        """
        
        args, unknown = self.parser.parse_known_args()
        if args.kana:
            self.use_kana_only = True
        if args.zenkaku:
            self.use_zenkaku = True
        if args.granularity:
            try:
                # make sure argument is a valid value (int)
                self.granularity = int(args.granularity)
            except:
                raise exception.InvalidOptionException("granularity")
            if self.granularity <= 0:
                raise exception.InvalidOptionException("granularity",
                    "Must be higher than zero")
        if args.delay:
            try:
                # make sure argument is a valid value (float)
                self.line_delay = float(args.delay)
            except:
                raise exception.InvalidOptionException("delay")
            if self.line_delay <= 0:
                raise exception.InvalidOptionException("delay",
                    "Must be higher than zero")

        # fill in other important properties
        if self.use_zenkaku:
            digmap_kana = self.digmap_kana_zenkaku
            digmap_alpha_num = self.digmap_alpha_num_zenkaku
            self.space = self.space_zenkaku
            self.proportion = 2
        else:
            digmap_kana = self.digmap_kana_hangaku
            digmap_alpha_num = self.digmap_alpha_num_hangaku
            self.space = self.space_hangaku
            self.proportion = 1

        self.digmap.extend(digmap_kana)
        if not self.use_kana_only:
            self.digmap.extend(digmap_alpha_num)
        
        if launchScreenImmediately:
            self.autorun()
        else:
            return self


    def __build_screen_map(self):
        """
        Defines the `screen_map` size and structure, considering the terminal
        geometry and the fact that full-width characters occupy the double of
        the space of a usual char. Additionally, it will start randomizing
        which x position should start with visible chars and which should be
        just empty space. 
        """
        # clean up previous
        self.screen_map = []

        for __ in range(0, self.geometry['x'] // self.proportion): 

            if random.random() > 0.5:
                char_list = self.get_char_list()
            else:
                char_list = [self.space for __ in \
                    range(0, random.randint(0, self.geometry['y']))]
            self.screen_map.append(char_list)

    def get_char_list(self):
        """
        creates a randomized list of characters to be used in the `screen_map`.
        """
        result = []
        while(len(result) == 0):
            bt = [self.space for __ in range(0, 
                    min((self.geometry['y'], random.randint(0, 
                        int(self.geometry['y'] * 20 / (self.granularity * \
                            self.proportion))))))]
            cl = [self.digmap[random.randint(0, len(self.digmap)) - 1] \
                  for __ in range(0, random.randint(0, 
                      self.geometry['y'] - len(bt)))]
            result = bt
            result.extend(cl)
        return result


    def print_line(self):
        """
        Prints the line picking up the first available char of each list within
        the `screen_map`, and creating (renewing) them if empty.
        """
        result = ""
        for i in range(0, len(self.screen_map)):
            if len(self.screen_map[i]) == 0:
                self.screen_map[i] = self.get_char_list()
            try:
                result += self.screen_map[i].pop(0)
            except:
                # ignore errors in here
                pass
        return result
