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
from appnetcomms.data_packet import DataPacket
from appnetcomms.constants import (
    MAX_SOCKET_SIZE,
    MAX_BUFFER_SIZE,
    BUFFER_SIZE_BYTES
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
        packet: DataPacket | None = None
):
    '''
    Put a data buffer onto the socket

    Args:
        send_socket (socket.socket): The socket to put the data on
        packet (DataPacket): The data packet (data and meta info)

    Returns:
        None

    Raises:
        AssertionError:
            When packet is not of type DataPacket
        FileNotFoundError:
            When the socket has not been created
        MemoryError:
            When the buffer to be sent exceeds the maximum size
    '''
    assert isinstance(packet, DataPacket), "packet must be of type DataPacket"
    if not isinstance(send_socket, socket.socket) or not send_socket:
        raise FileNotFoundError("socket has not been created")

    # Copy the buffer so the original is left intact
    _buffer_copy = bytes(packet.data)

    if packet.protocol == ProtocolType.TCP:
        # Ensure the buffer isn't too big
        if len(packet.data) > MAX_BUFFER_SIZE:
            raise MemoryError(f"send buffer exceeded {MAX_BUFFER_SIZE} bytes")

        # Prepend to size of the buffer to the buffer data
        _buffer_size = len(_buffer_copy).to_bytes(
            BUFFER_SIZE_BYTES,
            byteorder="big",
            signed=False
        )
        _send_buffer = _buffer_size + _buffer_copy

        # Send the message
        send_socket.sendall(_send_buffer)

    else:   # packet.protocol == ProtocolType.UDP
        send_socket.sendto(_buffer_copy, (packet.address, packet.port))


#
# get_socket_tcp
#
def get_socket_tcp(recv_socket: socket.socket) -> DataPacket | None:
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

    # Get the size of the data and the first part of the data
    _buffer_part = recv_socket.recv(MAX_SOCKET_SIZE)
    if not _buffer_part:
        # Client has disconnected
        return None

    _buffer_size_bytes = _buffer_part[:BUFFER_SIZE_BYTES]
    _buffer = _buffer_part[BUFFER_SIZE_BYTES:]

    _buffer_size = int.from_bytes(
        _buffer_size_bytes,
        byteorder="big",
        signed=False
    )

    while _buffer_size > len(_buffer):
        _buffer_part = recv_socket.recv(MAX_SOCKET_SIZE)
        if not _buffer_part:
            # Client has disconnected
            break

        # Check to make sure the buffer hasn't grown too large
        if len(_buffer) + len(_buffer_part) > MAX_BUFFER_SIZE:
            raise MemoryError(
                f"receive buffer exceeded {MAX_BUFFER_SIZE} bytes"
            )

        _buffer = _buffer + _buffer_part

    if _buffer:
        return DataPacket(data=_buffer)
    else:
        return None


#
# get_socket_udp
#
def get_socket_udp(recv_socket: socket.socket) -> DataPacket:
    '''
    Get a UDP datagram from the socket

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

    _data, _address = recv_socket.recvfrom(MAX_SOCKET_SIZE) 

    return DataPacket(
        data=_data,
        address=_address[0],
        protocol=ProtocolType.UDP,
        port=_address[1])


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
