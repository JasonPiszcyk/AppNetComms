#!/usr/bin/env python3
'''
Server component of AppNetComms

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
from appnetcomms.constants import DEFAULT_LISTEN_PORT
from appnetcomms.typing import ProtocolType, IPFamily
import appnetcomms.socket_server_factory as socket_server_factory
import appnetcomms.request_handler_factory as request_handler_factory

# Imports for python variable type hints
from typing import Callable


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
# NetCommServer Class Definition
#
###########################################################################
class NetCommServer():
    '''
    Class to manage a network communications server

    Attributes:
        address (str) [ReadOnly]: The Address the server is listening on
        protocol (ProtocolType) [ReadOnly]: The protocol the server is listening
            on
        port (int) [ReadOnly]: The port the server is listening on
        family (IPFamily) [ReadOnly]: The IP family (IPv6, IPv4, or both)
            supported by this server
        threaded (bool) [ReadOnly]: Return True if the server running a thread
            for each connection, False otherwise
    '''
    #
    # __init__
    #
    def __init__(
            self,
            address: str = "",
            protocol: ProtocolType = ProtocolType.TCP,
            port: int = DEFAULT_LISTEN_PORT,
            family: IPFamily = IPFamily.BOTH,
            threaded: bool = False,
            request_handler: Callable | None = None
    ):
        '''
        Initialises the instance.

        Args:
            address (str): The address the server should listen on
            protocol (ProtocolType): The protocol the server is listening on
            port (int): The port the server should listen on
            family (IPFamily): The IP family (IPv6, IPv4, or both) supported by
                this server
            threaded (bool): If True, start a new thread for each connection.
                If False, process incoming connections in the same thread
            request_handler (Callable): Function to process received data.
                Returns a DataPacket instance or None.  If return value is a
                DataPacket, return DataPacket.data via the socket

        Returns:
            None

        Raises:
            None
        '''
        if not isinstance(address, str): address = ""
        if not isinstance(protocol, ProtocolType): protocol = ProtocolType.TCP
        if not isinstance(port, int): port = DEFAULT_LISTEN_PORT
        if not isinstance(family, IPFamily): family = IPFamily.BOTH
        if not isinstance(threaded, bool): threaded = False
        if not callable(request_handler): request_handler = None

        # Private Attributes
        if address:
            self._address = address
        else:
            if family == IPFamily.IPV4:
                self._address = "0.0.0.0"
            else:
                self._address = "::"

        self._address = address
        self._protocol = protocol
        self._port = port
        self._family = family
        self._threaded = threaded
        self._request_handler = request_handler
        self._server = None

        # Attributes


    ###########################################################################
    #
    # Properties
    #
    ###########################################################################
    #
    # address
    #
    @property
    def address(self) -> str:
        ''' The Address the server is listening on '''
        return self._address


    @property
    def protocol(self) -> ProtocolType:
        ''' The Protocol the server is listening on '''
        return self._protocol


    @property
    def port(self) -> int:
        ''' The Port the server is listening on '''
        return self._port


    @property
    def family(self) -> IPFamily:
        ''' The IP family supported by this server '''
        return self._family

    @property
    def threaded(self) -> bool:
        ''' Is the server running a thread for each connection '''
        return self._threaded


    ###########################################################################
    #
    # Class Methods
    #
    ###########################################################################
    #
    # start
    #
    def start(self):
        '''
        Start the server

        Args:
            None

        Returns:
            None

        Raises:
            None
        '''
        # Generate a socketserver class via the factory
        _socketserver = socket_server_factory.SocketServerFactory(
            protocol=self._protocol,
            family=self._family,
            threaded=self._threaded
        )

        # Generate a handler class via the factory
        _handler = request_handler_factory.RequestHandlerFactory(
            protocol=self._protocol,
            request_handler=self._request_handler
        )

        # Create the server using the generated classes
        self._server = _socketserver((self._address, self._port), _handler)

        # Start the server
        with self._server:
            self._server.serve_forever()


    #
    # stop
    #
    def stop(self):
        '''
        Stop the server

        Args:
            None

        Returns:
            None

        Raises:
            None
        '''
        if isinstance(self._server, socketserver.BaseServer):
            # Shutdown the server
            self._server.shutdown()


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
