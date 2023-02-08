###############################################################################
#
# file:     position.py
#
# Purpose:  refer to module documentation for details
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
A helper class that provides positioning functionality to screens, such as
defining a terminal size, and centering information (horizontally or
vertically).

See additional information in the class itself.

The helper class available here is:

    * `PositionHelperBase`

"""
import math
import platform
import random
#
# Python built-in modules
#
import sys
import textwrap
import time

#
# Internal modules
#
from termsaver.termsaverlib.screen.helper import ScreenHelperBase


class PositionHelperBase(ScreenHelperBase):
    """
    This helper class provides positioning functionality to the screens,
    by dealing with the current dimensions of the terminal.

    There are main methods available here:

        * `get_terminal_size`: retrieves the current terminal dimensions, width
           and height, to be stored in local propertiy `geometry`.

        * `center_text_vertically`: centers a specified text in vertical

        * `center_text_horizontally`: centers a specified text in horizontal

        * `randomize_text_vertically`: randomizes a specified text in vertical

        * `randomize_text_horizontally`: randomizes a specified text in 
           horizontal

    If the method `get_terminal_size` is never called, all other functionality,
    relying on terminal dimensions, will just based on a default size, set as
    80x25.

    The main properties available are:

        * `geometry`: defines the size of the terminal (populated by the
          `get_terminal_size` method, whenever called.

        * `position`: defines the current position of the text to be printed,
           based on usage of other methods that temper with text positioning
           (eg. `randomize_text_horizontally`)

        * `changed_geometry`: for every call to `get_terminal_size` method,
           holds the information if the terminal has changed size or not.
    """
    
    geometry = {
        'x' : 0,
        'y' : 0,
    }
    """
    Defines the current terminal width and height.
    Its default value is set as 80x25.
    """

    __old_geometry = {
        'x' : 0,
        'y' : 0,
    }
    """
    Private property to track changes in the geometry. Refer to
    `changed_geometry` to identify any terminal size changes.
    """
    
    changed_geometry = False
    """
    A simple boolean that identifies if the terminal has changed size since the
    last check with `get_terminal_size`. This is handy to decide what to do
    with a particular screen (eg: clear and redraw again?).
    """
    
    position = {
        'x' : 0,
        'y' : 0,
    }
    """
    Stores the latest position X-Y axis (width and height) position value after
    calling the randomizing methods of this class (useful to allow you to know
    the previous location of the text in the window) 
    """
    
    def fix_text_wrap(self, text):
        """
        Wraps the text to the geometry size, maintaining existing new lines.
        """

        # fail safe if the screen does not properly set geometry
        if self.geometry['x'] == 0:
            return text

        temp = text.split("\n")
        longest_line = max([len(x) for x in temp])
        new_text = []
        for l in temp:
            # if utf string thwn width must be bigger
            overlen = len(l)-len(l) #.decode('utf-8)'))
            t = "\n".join(textwrap.wrap(l, width=self.geometry['x']+overlen))
            
            # fill in trailing blanks
            t += " " * (min(longest_line, self.geometry['x']) - min(len(t), self.geometry['x']))
            new_text.append(t)
        return "\n".join(new_text)
    
    def center_text_vertically(self, text):
        """
        Returns the text argument with additional new lines, calculated to
        display the text in the vertical center of the screen.

        Arguments:

            * text: the text to be vertically centered
        """

        temp = self.fix_text_wrap(text).split("\n")
        self.position['y'] = int(math.floor(
                (self.geometry['y'] - len(temp)) / 2))
        return "\n" * self.position['y'] + text
        
    def center_text_horizontally(self, text):
        """
        Returns the text argument with additional blank spaces, calculated to
        display the text in the horizontal center of the screen.

        Arguments:

            * text: the text to be horizontally centered
        """

        temp = self.fix_text_wrap(text).split("\n")
        new_text = ""
        for t in temp:
            self.position['x'] = int(math.ceil(
                    (self.geometry['x'] - len(t)) / 2))
            new_text += " " * self.position['x'] + t
            if len(temp) > 1:
                new_text += "\n"

        return new_text

    def align_text_right(self, text):
        """
        Returns the text argument with additional blank spaces, calculated to
        display the text in the right.

        Arguments:

            * text: the text to be aligned
        """
        return " " * (self.geometry['x'] - len(text)) + text

    def randomize_text_horizontally(self, text):
        """
        Returns the text argument with additional blank spaces, calculated to
        display the text in a random position of the screen.

        Arguments:

            * text: the text to be horizontally randomized
        """

        # find longest line
        temp = self.fix_text_wrap(text).split("\n")
        longest_line = max([len(x) for x in temp])

        self.position['x'] = random.randint(0, 
                self.geometry['x'] - longest_line)
        
        new_text = ""
        for t in temp:
            new_text += " " * self.position['x'] + t
            if len(temp) > 0:
                new_text += "\n"

        return new_text

    def randomize_text_vertically(self, text):
        """
        Returns the text argument with additional new lines, calculated to
        display the text in a random position of the screen.

        Arguments:

            * text: the text to be vertically randomized
        """
        total_lines = len(self.fix_text_wrap(text).split("\n"))
        self.position['y'] = random.randint(0, 
                max(0, self.geometry['y'] - total_lines))
        
        return "\n" * self.position['y'] + text

    def get_terminal_size(self):
        """ 
        Retrieves the screen terminal dimensions, returning a tuple
        (width, height), and will also store them in internal property 
        `geometry`.
        
        """
        
        self.geometry['y'], self.geometry['x'] = self.window.getmaxyx()

        # store geometry changes
        if self.__old_geometry == {'x': 0, 'y': 0}:
            # first time checking geometry
            self.__old_geometry = self.geometry.copy()
            self.changed_geometry = False
        elif self.__old_geometry != self.geometry:
            self.__old_geometry = self.geometry.copy()
            self.changed_geometry = True
        else:
            self.changed_geometry = False
