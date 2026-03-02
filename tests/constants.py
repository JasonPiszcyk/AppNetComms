#!/usr/bin/env python3
'''
The Constants used for Testing

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
# Shared variables, constants, etc

# System Modules

# Local app modules
from appnetcomms import ProtocolType, IPFamily

# Imports for python variable type hints


###########################################################################
#
# Module Specific Items
#
###########################################################################
#
# Types
#

#
# Constants
#
SERVER_PORT = 15151
SERVER_ADDRESS_IPv4 = "127.0.0.1"
SERVER_ADDRESS_IPv6 = "::1"

# Different Protocols to try out
SERVER_PROTOCOLS = {
    "TCP": ProtocolType.TCP,
    "UDP": ProtocolType.UDP
}


# Different families to try out
SERVER_FAMILIES = {
    "IPv4": IPFamily.IPV4,
    "IPv6": IPFamily.IPV6,
    "Both": IPFamily.BOTH
}

SIMPLE_DATA_BYTES = b"simple_data_byes"
RANDOM_BYTE_LEN = 5000
RANDOM_RESPONSE_PREFIX = b"__RANDOM_RESPONSE_PREFIX__"

#
# Global Variables
#
