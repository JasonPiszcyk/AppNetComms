#!/usr/bin/env python3
'''
Define a data structure for a data packet

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
from appnetcomms.typing import ProtocolType

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

#
# Global Variables
#


###########################################################################
#
# UDPData Class Definition
#
###########################################################################
class DataPacket():
    '''
    Class to describe a data Packet

    Data structure for UDP data

    Attributes:
        None
    '''
    #
    # __init__
    #
    def __init__(
            self,
            data: bytes = b"",
            address: str = "",
            protocol = ProtocolType.TCP,
            port: int = 0            
    ):
        '''
        Initialises the instance.

        Args:
            data (bytes): The data associated with the datagram
            address (str): The address associated with the datagram
            port (int): The port associated with the datagram

        Returns:
            None

        Raises:
            None
        '''
        # Private Attributes
        self._data = b""
        self._address = ""
        self._protocol = ProtocolType.TCP
        self._port = 0

        # Attributes
        self.data = data
        self.address = address
        self._protocol = protocol
        self.port = port



    ###########################################################################
    #
    # Properties
    #
    ###########################################################################
    #
    # data
    #
    @property
    def data(self) -> bytes:
        ''' The data associated with this datagram '''
        return self._data


    @data.setter
    def data(self, value: bytes = b""):
        ''' Set the data associated with this datagram '''
        if isinstance(value, bytes):
            self._data = value


    #
    # address
    #
    @property
    def address(self) -> str:
        ''' The address associated with this datagram '''
        return self._address


    @address.setter
    def address(self, value: str = ""):
        ''' Set the address associated with this datagram '''
        if isinstance(value, str):
            self._address = value


    #
    # protocol
    #
    @property
    def protocol(self) -> ProtocolType:
        ''' The protocol associated with this datagram '''
        return self._protocol


    @protocol.setter
    def protocol(self, value: ProtocolType | None = None):
        ''' Set the protocol associated with this datagram '''
        if isinstance(value, ProtocolType):
            self._protocol = value


    #
    # port
    #
    @property
    def port(self) -> int:
        ''' The port associated with this datagram '''
        return self._port


    @port.setter
    def port(self, value: int = 0):
        ''' Set the port associated with this datagram '''
        if isinstance(value, int) and value > 0 and value < 65535:
            self._port = value


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
