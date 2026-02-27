#!/usr/bin/env python3
'''
Wrappers of the socket servers to enable mods for dual stack, etc

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
from appnetcomms.typing import IPFamily

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
# Function to help set up the socket server
#
###########################################################################
#
# _get_address_family
#
def _get_address_family(
        family: IPFamily = IPFamily.BOTH
) -> socket.AddressFamily:
    '''
    Return the socket address family

    Args:
        family (IPFamily): The IP family (IPv6, IPv4, or both) supported by
            this server

    Returns:
        socket.AddressFamily: The address family to use

    Raises:
        None
    '''
    if not isinstance(family, IPFamily): family = IPFamily.BOTH

    if family == IPFamily.IPV4:
        return socket.AF_INET

    return socket.AF_INET6


#
# _get_dual_stack
#
def _get_dual_stack(family: IPFamily = IPFamily.BOTH) -> bool:
    '''
    Return if Dual stack is being used

    Args:
        family (IPFamily): The IP family (IPv6, IPv4, or both) supported by
            this server

    Returns:
        socket.AddressFamily: The address family to use

    Raises:
        None
    '''
    if not isinstance(family, IPFamily): family = IPFamily.BOTH

    if family == IPFamily.BOTH:
        return True

    return False


#
# _get_ip_proto
#
def _get_ip_proto(family: IPFamily = IPFamily.BOTH) -> int:
    '''
    Determine the IP Protocol for the socket

    Args:
        family (IPFamily): The IP family (IPv6, IPv4, or both) supported by
            this server

    Returns:
        int: The IP Protocol

    Raises:
        None
    '''
    if not isinstance(family, IPFamily): family = IPFamily.BOTH

    if family == IPFamily.IPV4:
        return socket.IPPROTO_IPV4

    return socket.IPPROTO_IPV6


#
# _set_dual_stack
#
def _set_dual_stack(
        server_socket: socket.socket | None = None,
        dual_stack: bool = True,
        ip_proto: int = socket.IPPROTO_IPV6
):
    '''
    Set the socket options to determine if dual stack required

    Args:
        dual_stack (bool): If True, enable dual stack, if False enable single
            IP protocol/family

    Returns:
        None

    Raises:
        None
    '''
    # If the socket isn't set, not much to do
    if not isinstance(server_socket, socket.socket): return
    if not server_socket: return

    # Set defaults for other args
    if not isinstance(dual_stack, bool): dual_stack = True
    if not isinstance(ip_proto, int): ip_proto = socket.IPPROTO_IPV6

    # Generally, if IPv6 enabled it is dual stack. Explicitly set IPV6_ONLY
    # to ensure it is correct
    if hasattr(server_socket, "IPV6_V6ONLY"):
        if dual_stack:
            server_socket.setsockopt(
                socket.IPPROTO_IPV6,
                socket.IPV6_V6ONLY,
                0
            )

        elif ip_proto == socket.IPPROTO_IPV6:
            server_socket.setsockopt(
                socket.IPPROTO_IPV6,
                socket.IPV6_V6ONLY,
                1
            )


###########################################################################
#
# _TCP Class Definition
#
###########################################################################
class _TCP(socketserver.TCPServer):
    '''
    Class to wrap TCP socket server and manage IP family/Dual stack
    '''
    # AF_INET6 supports IPv6 only, or dual stack.  AF_INET is IPv4 only
    address_family = socket.AF_INET6
    dual_stack = True


    #
    # __init__
    #
    def __init__(
            self,
            *args,
            family: IPFamily = IPFamily.BOTH,
            **kwargs
    ):
        '''
        Initialises the instance.

        Args:
            *args (Undef): Unnamed arguments to be passed to the constructor
                of the inherited process
            family (IPFamily): The IP family (IPv6, IPv4, or both) supported by
                this server
            **kwargs (Undef): Keyword arguments to be passed to the constructor
                of the inherited process

        Returns:
            None

        Raises:
            None
        '''
        if not isinstance(family, IPFamily): family = IPFamily.BOTH

        self.address_family = _get_address_family(family=family)
        self.dual_stack = _get_dual_stack(family=family)
        self.ip_proto = _get_ip_proto(family=family)

        super().__init__(*args, **kwargs)


    def server_bind(self):
        _set_dual_stack(
            server_socket=self.socket,
            dual_stack=self.dual_stack,
            ip_proto=self.ip_proto
        )

        super().server_bind()


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
