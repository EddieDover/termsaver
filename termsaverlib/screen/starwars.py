###############################################################################
#
# file:     starwars.py
#
# Purpose:  An attempt at the starwars asciimation
#
# Note:     This file is part of Termsaver application, and should not be used
#           or executed separately.
#
###############################################################################
#
# Copyright 2020 Termsaver
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
This module contains a simple screen that loads the sw1.txt file used by
the star wars asciimation.

The screen class available here is:

    * `StarWarsScreen`
"""

#
# Internal modules
#
from termsaverlib.screen.base import ScreenBase
from termsaverlib.screen.helper.position import PositionHelperBase
from termsaverlib import common
from termsaverlib.i18n import _

import itertools

import time
import io

class StarWarsScreen(ScreenBase, PositionHelperBase):
    """
    Screen that displays the star wars text from the
    star wars asciimation.
    (http://www.asciimation.co.nz/).

    From its base classes, the functionality provided here bases on the
    settings defined below:

        * clean up each cycle: True
          this will force the screen to be cleaned (cleared) before each new
          cycle is displayed
    """

    def __init__(self):
        """
        The constructor of this class.
        """
        ScreenBase.__init__(self,
            "starwars",
            _("displays the star wars asciimation on screen"),
            'http://asciimation.co.nz',
            ["description"],
            "%(description)s",
        )
        self.cleanup_per_cycle = True
        self.is_initalized = False

    def reshape(self,lst, n):
        return [lst[i*n:(i+1)*n] for i in range(len(lst)//n)]

    def _run_cycle(self):
        """
        Executes a cycle of this screen.
        """
        
        if self.is_initalized is False:
            with io.open("data/sw1.txt","rb") as swfile:
                lines = swfile.readlines()
                lines = [line.decode('utf-8') for line in lines]

                self.current_frame = 0
                self.star_wars = self.reshape(lines,14)
                self.time_per_frame = 15
                self.is_initalized = True

        frame_time = float(self.star_wars[self.current_frame][0]) / self.time_per_frame
        print ("\r\n" + "".join(self.star_wars[self.current_frame][1:14]))
        time.sleep(frame_time)
        self.current_frame += 1
