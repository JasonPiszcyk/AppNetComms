#!/usr/bin/env python3
'''
Common functions shared betgween server and client

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

# Local app modules
from appnetcomms.constants import (
    MAX_SOCKET_SIZE,
    MAX_BUFFER_SIZE,
    BUFFER_PADDING
)
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
# Module
#
###########################################################################
#
# put_socket
#
def put_socket(
        send_socket: socket.socket,
        buffer: bytes = b"",
        protocol: ProtocolType = ProtocolType.TCP,
        address: str = "",
        port: int = 0
):
    '''
    Put a data buffer onto the socket

    Args:
        send_socket (socket.socket): The socket to put the data on
        buffer (bytes): The data to send
        protocol (ProtocolType): The protocol used to send
        address (str): The address the client should connect to (not used if
            protocol is TCP)
        port (int): The port the client should connect to (not used if protocol
            is TCP)

    Returns:
        None

    Raises:
        AssertionError:
            When buffer is not of type bytes
            When protocol type is not valid
            When protocol is UDP, and address is not a valid string
            When protocol is UDP, and port is not a positive integer <= 65535
        FileNotFoundError:
            When the socket has not been created
        MemoryError:
            When the buffer to be sent exceeds the maximum size
    '''
    assert isinstance(buffer, bytes), "buffer must be of type bytes"
    if not isinstance(send_socket, socket.socket) or not send_socket:
        raise FileNotFoundError("socket has not been created")

    assert isinstance(protocol, ProtocolType), (
        "protocol must be of type ProtocolType"
    )

    if protocol == ProtocolType.UDP:
        assert isinstance(address, str) and address, (
             "address must be a non-empty string"
        )
        assert isinstance(port, int) and port > 0 and port < 65536, (
            "port must be a positive integer between 1 and 65535"
        )

    # Ensure the buffer isn't too big
    if len(buffer) > MAX_BUFFER_SIZE:
        raise MemoryError(f"send buffer exceeded {MAX_BUFFER_SIZE} bytes")

    # Copy the buffer so the original is left intact
    _buffer_copy = bytes(buffer)

    # Send the message in parts
    while len(_buffer_copy) > 0:
        _send_buffer = _buffer_copy[:MAX_SOCKET_SIZE]
        _buffer_copy = _buffer_copy[MAX_SOCKET_SIZE:]

        # If we send MAX_SOCKET_SIZE bytes, receiver assumes there is more
        # data and will wait for it.  If there is nothiung else to send,
        # pad the buffer_copy to ensure the other end finishes constructing
        # the receive buffer.
        if (len(_buffer_copy) < 1 and len(_send_buffer) == MAX_SOCKET_SIZE):
            _buffer_copy = BUFFER_PADDING

        if protocol == ProtocolType.TCP:
            # TCP
            send_socket.sendall(_send_buffer)
        else:
            # UDP
            send_socket.sendto(_send_buffer, (address, port))


#
# get_socket
#
def get_socket(recv_socket: socket.socket) -> bytes:
    '''
    Build a data buffer from data read from the socket

    Args:
        recv_socket (socket.socket): The socket to read from

    Returns:
        bytes - The data buffer

    Raises:
        FileNotFoundError:
            When the socket has not been created
        MemoryError:
            When the receive buffer exceeds the maximum size
    '''
    if not isinstance(recv_socket, socket.socket) or not recv_socket:
        raise FileNotFoundError("socket has not been created")

    _buffer = b""
    while True:
        _buffer_part = recv_socket.recv(MAX_SOCKET_SIZE)
        if _buffer_part == BUFFER_PADDING:
            # We have all of the data, so ignore this
            # Padding sent as message size was right on boundary
            break

        # Check to make sure the buffer hasn't grown too large
        if len(_buffer) + len(_buffer_part) > MAX_BUFFER_SIZE:
            raise MemoryError(
                f"receive buffer exceeded {MAX_BUFFER_SIZE} bytes"
            )

        _buffer = _buffer + _buffer_part

        # Check to see if more data is expected
        if len(_buffer_part) < MAX_SOCKET_SIZE:
            break

    return _buffer


###########################################################################
#
# In case this is run directly rather than imported...
#
###########################################################################
'''
Handle case of being run directly rather than imported
'''
if __name__ == "__main__":
    pass
