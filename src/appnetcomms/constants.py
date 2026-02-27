#!/usr/bin/env python3
'''
Constants for the module

Copyright (C) 2026 Jason Piszcyk
Email: Jason.Piszcyk@gmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program (See file: COPYING). If not, see
<https://www.gnu.org/licenses/>.
'''
###########################################################################
#
# Imports
#
###########################################################################
from __future__ import annotations

# Shared variables, constants, etc

# System Modules

# Local app modules

# Imports for python variable type hints


###########################################################################
#
# Module Specific Items
#
###########################################################################
#
# Constants
#
DEFAULT_LISTEN_PORT = 15151

MAX_SOCKET_SIZE = 1024
MAX_BUFFER_SIZE = 65536
BUFFER_PADDING = b'___BUFFER PADDING___'


###########################################################################
#
# I choose to start the main code...  Here
#
###########################################################################
'''
Handle case of being run directly rather than imported
'''
if __name__ == "__main__":
    pass
