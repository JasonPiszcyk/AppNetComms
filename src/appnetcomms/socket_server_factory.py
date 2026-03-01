#!/usr/bin/env python3
'''
Factory to generate a class for the socket server

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
import socketserver

# Local app modules
from appnetcomms.typing import ProtocolType, IPFamily

# Imports for python variable type hints
from typing import Any


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
# SocketServerFactory
#
###########################################################################
def SocketServerFactory(
        protocol: ProtocolType = ProtocolType.TCP,
        family: IPFamily = IPFamily.BOTH,
        threaded: bool = False
) -> Any:
    '''
    Return a socketserver class instance base on the args

    Args:
        protocol (ProtocolType): The protocol to use for the server
        family (IPFamily): The IP family (IPv6, IPv4, or both) to be supported
            by this server
        threaded (bool): If True, start a new thread for each connection. If
            False, process incoming connections in the same thread

    Returns:
        socketserver.BaseServer - A socket server class instance

    Raises:
        None
    '''
    if not isinstance(family, IPFamily): family = IPFamily.BOTH
    if not isinstance(protocol, ProtocolType): protocol = ProtocolType.TCP
    if not isinstance(threaded, bool): threaded = False

    # Determine the type of server to select the base class
    if threaded:
        if protocol == ProtocolType.TCP:
            _base_class = socketserver.ThreadingTCPServer

        else:   # protocol == ProtocolType.UDP
            _base_class = socketserver.ThreadingUDPServer

    else:   # not threaded
        if protocol == ProtocolType.TCP:
            _base_class = socketserver.TCPServer

        else:   # protocol == ProtocolType.UDP
            _base_class = socketserver.UDPServer


    # Define the socket server class
    class _socket_server(_base_class): # type: ignore
        '''
        Class to wrap TCP socket server and manage IP family/Dual stack
        '''
        # Allow server to be restarted even if sockets in TIME_WAIT
        allow_reuse_address = True

        # default socket to both IPv4/IPv6
        address_family = socket.AF_INET6

        #
        # server_bind
        #
        def server_bind(self):
            '''
            Bind to the IP port 

            Args:
                None

            Returns:
                None

            Raises:
                None
            '''
            # If the socket isn't set, not much to do
            if not isinstance(self.socket, socket.socket): return
            if not self.socket: return

            # Set defaults for other args
            if not isinstance(_socket_server.ip_family, IPFamily):
                _socket_server.ip_family = IPFamily.BOTH

            # Generally, if IPv6 enabled it is dual stack. Explicitly set
            # IPV6_ONLY to ensure it is correct
            if hasattr(socket, "IPV6_V6ONLY"):
                if _socket_server.ip_family == IPFamily.BOTH:
                    # Set IPv6 Only to False
                    self.socket.setsockopt(
                        socket.IPPROTO_IPV6,
                        socket.IPV6_V6ONLY,
                        0
                    )

                elif _socket_server.ip_family == IPFamily.IPV6:
                    # Set IPv6 Only to True
                    self.socket.setsockopt(
                        socket.IPPROTO_IPV6,
                        socket.IPV6_V6ONLY,
                        1
                    )

            # Call the base class server_bind method
            super().server_bind()


    # AF_INET6 supports IPv6 only, or dual stack.  AF_INET is IPv4 only
    _socket_server.ip_family = family
    if family == IPFamily.IPV4:
        _socket_server.address_family = socket.AF_INET

    return _socket_server


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
