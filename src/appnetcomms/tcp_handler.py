#!/usr/bin/env python3
'''
Class to handle an incoming TCP connection

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
import socketserver

# Local app modules
from appnetcomms.constants import MAX_SOCKET_SIZE

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
# TCPHandler Class Definition
#
###########################################################################
class TCPHandler(socketserver.BaseRequestHandler):
    '''
    TCPHandler is instantiated once per TCP connection to process the
    network traffic.

    Attributes:
        None
    '''
    #
    # __init__
    #
    def __init__(
            self,
            *args,
            **kwargs
    ):
        '''
        Initialises the instance.

        Args:
            *args (Undef): Unnamed arguments to be passed to the constructor
                of the inherited process
            **kwargs (Undef): Keyword arguments to be passed to the constructor
                of the inherited process

        Returns:
            None

        Raises:
            None
        '''
        super().__init__(*args, **kwargs)

        # Private Attributes

        # Attributes


    ###########################################################################
    #
    # Class Methods
    #
    ###########################################################################
    def handle(self):
        '''
        Handle a TCP connection

        Args:
            None

        Returns:
            None

        Raises:
            None
        '''
        # self.request is the TCP socket connected to the client
        # print(f"Connected: {self.client_address[0]}:{self.client_address[1]}")
        try:
            while True:
                data = self.request.recv(MAX_SOCKET_SIZE)
                if not data:
                    break
                # Echo the received data back to the client
                self.request.sendall(data)

        except Exception as e:
            print(f"Error with client {self.client_address}: {e}")

        finally:
            print(f"Disconnected: {self.client_address[0]}:{self.client_address[1]}")
            self.request.close()


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
