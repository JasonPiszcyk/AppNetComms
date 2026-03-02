#!/usr/bin/env python3
'''
Factory to generate a class for the request handler

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
import socket

# Local app modules
from appnetcomms.typing import ProtocolType
from appnetcomms.data_packet import DataPacket
from appnetcomms.common import put_socket, get_socket_tcp

# Imports for python variable type hints
from typing import Any, Callable

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
# RequestHandlerFactory
#
###########################################################################
def RequestHandlerFactory(
        protocol: ProtocolType = ProtocolType.TCP,
        request_handler: Callable | None = None
) -> Any:
    '''
    Return a request handler class instance base on the args

    Args:
        protocol (ProtocolType): The protocol to use for the request handler
        request_handler (Callable): Function to process received data.
            Returns a DataPacket instance or None.  If return value is a
            DataPacket, return DataPacket.data via the socket

    Returns:
        socketserver.BaseRequestHandler - A request handler class instance

    Raises:
        None
    '''
    if not isinstance(protocol, ProtocolType): protocol = ProtocolType.TCP


    # Define the request handler class
    class _request_handler(socketserver.BaseRequestHandler): # type: ignore
        '''
        _request_handler is instantiated once per connection to process the
        network traffic.

        Attributes:
            None
        '''
        custom_handler = request_handler

        # define the hander function
        if protocol == ProtocolType.TCP:
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
                while True:
                    try:
                        _packet = get_socket_tcp(recv_socket=self.request)

                    except Exception:
                        _packet = None

                    if not _packet:
                        # Client has disconnected, or error has occured
                        break

                    if callable(_request_handler.custom_handler):
                        try:
                            _result = _request_handler.custom_handler(
                                packet=_packet
                            )

                        except Exception:
                            _result = None

                    else:
                        # Default to echoing the received data back to the client
                        _result = _packet

                    # Send the result to the client if desired
                    if isinstance(_result, DataPacket):
                        put_socket(send_socket=self.request, packet=_result)

                # Close the socket
                self.request.close()

        else:   # protocol == ProtocolType.UDP
            def handle(self):
                '''
                Handle a UDP connection

                Args:
                    None

                Returns:
                    None

                Raises:
                    None
                '''
                # The datagram is in the request
                _packet = DataPacket(
                    data=self.request[0].strip(),
                    address=self.client_address[0],
                    protocol=ProtocolType.UDP,
                    port=self.client_address[1]
                )

                if callable(_request_handler.custom_handler):
                    try:
                        _result = _request_handler.custom_handler(
                            packet=_packet
                        )

                    except Exception:
                        _result = None

                else:
                    # Default to echoing the received data back to the client
                    _result = _packet

                # Send the result to the client if desired
                if (
                    isinstance(_result, DataPacket) and 
                    isinstance(self.request[1], socket.socket)
                ):
                    put_socket(send_socket=self.request[1], packet=_result)


    # Return the class
    return _request_handler


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
