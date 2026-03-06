#!/usr/bin/env python3
'''
Client component of AppNetComms

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
import socket
from applogging.logging import get_logger, init_console_logger

# Local app modules
from appnetcomms.data_packet import DataPacket
from appnetcomms.common import put_socket, get_socket_tcp, get_socket_udp
from appnetcomms.constants import DEFAULT_LISTEN_PORT
from appnetcomms.typing import ProtocolType, IPFamily

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
DEFAULT_LOGGER_NAME = "AppNetComms"

#
# Global Variables
#


###########################################################################
#
# NetCommClient Class Definition
#
###########################################################################
class NetCommClient():
    '''
    Class to manage a network communications client sessions

    Attributes:
        address (str) [ReadOnly]: The Address the client connects to
        protocol (ProtocolType) [ReadOnly]: The protocol the client uses
        port (int) [ReadOnly]: The port the client uses
        family (IPFamily) [ReadOnly]: The IP family (IPv6, IPv4, or both)
            supported by this connection
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
            logger_name: str = "",
            logger_level: str = "CRITICAL"
    ):
        '''
        Initialises the instance.

        Args:
            address (str): The address the client should connect to
            protocol (ProtocolType): The protocol the client should use
            port (int): The port the client should connect to
            family (IPFamily): The IP family (IPv6, IPv4, or both) supported by
                this connection
            logger_name (str): The name of the logger to use.  If empty (or
                not a string) then a logger will be created to log to the
                console
            logger_level (str): If no logger name is provided, the created
                logger will be set to log events at or above this level (default
                = "CRITICAL")

        Returns:
            None

        Raises:
            AssertionError:
                When address is not a string, or is empty
        '''
        assert isinstance(address, str), "address must be a string"
        assert address, "Address cannot be empty"

        if not isinstance(protocol, ProtocolType): protocol = ProtocolType.TCP
        if not isinstance(port, int): port = DEFAULT_LISTEN_PORT
        if not isinstance(family, IPFamily): family = IPFamily.BOTH

        # Private Attributes
        self._address = address
        self._protocol = protocol
        self._port = port
        self._family = family
        self._socket = None

        if isinstance(logger_name, str) and logger_name:
            self._logger = get_logger(name=logger_name)

        else:
            self._logger = init_console_logger(name=DEFAULT_LOGGER_NAME)
            self._logger.setLevel(level=logger_level)

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
        ''' The address the client connects to '''
        return self._address


    @property
    def protocol(self) -> ProtocolType:
        ''' The protocol the client uses '''
        return self._protocol


    @property
    def port(self) -> int:
        ''' The port the client connects to '''
        return self._port


    @property
    def family(self) -> IPFamily:
        ''' The IP family supported by this connection '''
        return self._family


    ###########################################################################
    #
    # Class Methods
    #
    ###########################################################################
    #
    # connect
    #
    def connect(self):
        '''
        Connect to the server

        Args:
            None

        Returns:
            None

        Raises:
            None
        '''
        self._logger.debug("Client -> Connect")

        if not isinstance(self._socket, socket.socket):
            if self._protocol == ProtocolType.TCP:
                if self._family == IPFamily.IPV4:
                    self._socket = socket.socket(
                        socket.AF_INET,
                        socket.SOCK_STREAM
                    )
                    self._socket.connect((self._address, self._port))

                if self._family == IPFamily.IPV6:
                    self._socket = socket.socket(
                        socket.AF_INET6,
                        socket.SOCK_STREAM
                    )
                    self._socket.connect((self._address, self._port))

                else:
                    self._socket = socket.create_connection(
                        (self._address, self._port)
                    )

            else:   # self._protocol == ProtocolType.UDP
                if self._family == IPFamily.IPV4:
                    self._socket = socket.socket(
                        socket.AF_INET,
                        socket.SOCK_DGRAM
                    )

                if self._family == IPFamily.IPV6:
                    self._socket = socket.socket(
                        socket.AF_INET6,
                        socket.SOCK_DGRAM
                    )

                else:
                    _addr_info = socket.getaddrinfo(
                        self._address,
                        self._port,
                        family=socket.AF_UNSPEC,
                        type=socket.SOCK_DGRAM,
                        proto=0,
                        flags=socket.AI_ADDRCONFIG
                    )

                    _socket_exception = None
                    for family, socktype, proto, _, sa in _addr_info:
                        try:
                            # Create a socket using the gathered information
                            self._socket = socket.socket(
                                family,
                                socktype,
                                proto
                            )

                            # Socket created OK
                            break
            
                        except socket.error as _err:
                            if not _socket_exception: _socket_exception = _err
                            continue

                    # Don't hide the exception raised by the socket attempt
                    if _socket_exception: raise _socket_exception

        else:   # isinstance(self._socket, socket.socket):
            self._logger.warning("Client socket already created")


    #
    # disconnect
    #
    def disconnect(self):
        '''
        Disconnect from the server

        Args:
            None

        Returns:
            None

        Raises:
            None
        '''
        self._logger.debug("Client -> Disconnect")

        if isinstance(self._socket, socket.socket):
            # If TCP send a shutdown
            if self._protocol == ProtocolType.TCP:
                self._socket.shutdown(socket.SHUT_RDWR)
        
            # Close the socket
            self._socket.close()


    #
    # send
    #
    def send(self, buffer: bytes = b""):
        '''
        Send to the socket

        Args:
            buffer (bytes): The data to send

        Returns:
            None

        Raises:
            AssertionError:
                When buffer is not of type bytes
            FileNotFoundError:
                When the socket has not been created
            MemoryError:
                When the buffer to be sent exceeds the maximum size
        '''
        assert isinstance(buffer, bytes), "buffer must be of type bytes"
        if not isinstance(self._socket, socket.socket) or not self._socket:
            raise FileNotFoundError("socket has not been created")

        self._logger.debug("Client -> Send")

        _packet = DataPacket(
            data=buffer,
            address=self.address,
            protocol=self.protocol,
            port=self.port
        )

        put_socket(send_socket=self._socket, packet=_packet)


    #
    # receive
    #
    def receive(self) -> bytes:
        '''
        Receive from the socket

        Args:
            None

        Returns:
            bytes - The received data buffer

        Raises:
            FileNotFoundError:
                When the socket has not been created
        '''
        if not isinstance(self._socket, socket.socket) or not self._socket:
            raise FileNotFoundError("socket has not been created")

        self._logger.debug("Client -> Receive")

        _data = b""

        if self._protocol == ProtocolType.TCP:
            _packet = get_socket_tcp(self._socket)
        else:
            _packet = get_socket_udp(self._socket)

        if isinstance(_packet, DataPacket):
            _data = _packet.data

        return _data


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
