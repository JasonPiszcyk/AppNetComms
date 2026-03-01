#!/usr/bin/env python3
'''
PyTest - Test of AppNetComm Server

Copyright (C) 2025 Jason Piszcyk
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
from tests.constants import *

# System Modules
import pytest
import time
import subprocess

# Local app modules
from appnetcomms import NetCommServer, NetCommClient, ProtocolType, IPFamily
from apptasking.tasking import Tasking, TaskTask

# Imports for python variable type hints
from typing import Any, Final


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
# Functions to run in the thread/process
#
###########################################################################
def get_netstat_listen_info() -> str:
    # Run the command and capture the output
    _netstat_output = subprocess.run(
        ["netstat", "-an"],
        capture_output=True,
        text=True,
        check=True
    )

    # Run it through grep
    _result = subprocess.run(
        ['grep', str(SERVER_PORT)],
        input=_netstat_output.stdout,
        capture_output=True,
        text=True,
        check=True
    )

    # return the protocol/family
    return _result.stdout.split()[0]


#
# Run the server in a separate thread
#
def create_comm_server_task(
        protocol: ProtocolType = ProtocolType.TCP,
        family: IPFamily = IPFamily.IPV6,
        threaded: bool = False
) -> TaskTask:
    # Create a task manager
    _task_mgr = Tasking(task_type="thread")

    # Create the Server
    _server = NetCommServer(
        address = "",
        protocol = protocol,
        port = SERVER_PORT,
        family = family,
        threaded = threaded
    )

    # Return the task
    return _task_mgr.create(
        name=f"AppNetComms - Server",
        start_func=_server.start,
        stop_func=_server.stop,
    )


###########################################################################
#
# The tests...
#
###########################################################################
#
# Server (tests both server and client)
#
class Test_Server():
    '''
    Test Class - Server -Test comms between the server and client

    Attributes:
        None
    '''
    #
    # _send_client
    #
    def _send_client(self, server_family, server_protocol, data):
        '''
        Basic tests

        Args:
            server_family: The family the server is using
            server_protocol: The protocol the server is using
            data: Data to be sent

        Returns:
            None

        Raises:
            AssertionError:
                when test fails
        '''
        assert server_family in IPFamily
        assert server_protocol in ProtocolType

        # Go through each protocol and test it
        for _proto in ProtocolType:
            # Go through each family and test it
            for _family in IPFamily:
                # Create the client
                if _family == IPFamily.IPV4:
                    _address = SERVER_ADDRESS_IPv4

                elif _family == IPFamily.IPV6:
                    _address = SERVER_ADDRESS_IPv6

                else:   # _family == IPFamily.BOTH
                    # Check what the server is running
                    if server_family == IPFamily.IPV4:
                        _address = SERVER_ADDRESS_IPv4
                    else:
                        _address = SERVER_ADDRESS_IPv6

                _client = NetCommClient(
                    address = _address,
                    protocol = _proto,
                    port = SERVER_PORT,
                    family = _family
                )

                # The ways connect might fail
                _expect_connect_fail = False
                if _proto != server_protocol:
                    _expect_connect_fail = True

                if server_family == IPFamily.IPV4:
                    if _family == IPFamily.IPV6:
                        _expect_connect_fail = True

                elif server_family == IPFamily.IPV6:
                    if _family == IPFamily.IPV4:
                        _expect_connect_fail = True

                if _expect_connect_fail:
                    # If trying to connect using UDP and server on TCP then
                    # skip test as UDP is just sent and test will hang waiting
                    # for a reply that will never come
                    if _proto == ProtocolType.UDP: continue

                    with pytest.raises(ConnectionRefusedError):
                        _client.connect()

                else:   # connection can be made
                    _client.connect()
                    _client.send(data)
                    _buffer = _client.receive()
                    _client.disconnect()
                    assert _buffer == data


    #
    # Basic Test - Start, check port being listened on, stop
    #
    @pytest.mark.parametrize("family", SERVER_FAMILIES)
    @pytest.mark.parametrize("protocol", SERVER_PROTOCOLS)
    def test_basic(self, family, protocol):
        '''
        Basic tests

        Args:
            family: The family being tested (eg IPv6, IPv4)
            protocol: The protocol being tested (eg TCP, UDP)

        Returns:
            None

        Raises:
            AssertionError:
                when test fails
        '''
        assert family in SERVER_FAMILIES
        assert protocol in SERVER_PROTOCOLS

        # Create a thread/non thread version of each
        for _threaded in [ False, True]:
            _task = create_comm_server_task(
                protocol=SERVER_PROTOCOLS[protocol],
                family=SERVER_FAMILIES[family],
                threaded=_threaded
            )

            # Start the server
            _task.start()

            # Wait a bit for it to start
            time.sleep(0.1)

            # Check the port
            _listen_port = get_netstat_listen_info()

            # On mac returns proto (tcp or udp) and family (4 or 46)
            assert _listen_port[:3] == SERVER_PROTOCOLS[protocol].value
            if SERVER_FAMILIES[family] == IPFamily.IPV4:
                assert _listen_port[3:] == "4"
            else:
                assert _listen_port[3:] == "46"

            # Stop the server
            _task.stop()


    #
    # internal echo - Send message, letting server respond with internal echo
    #
    @pytest.mark.parametrize("family", SERVER_FAMILIES)
    @pytest.mark.parametrize("protocol", SERVER_PROTOCOLS)
    def test_internal_echo(self, family, protocol):
        '''
        Send a simple message to server with the handler being the internal
        echo handler

        Args:
            family: The family being tested (eg IPv6, IPv4)
            protocol: The protocol being tested (eg TCP, UDP)

        Returns:
            None

        Raises:
            AssertionError:
                when test fails
        '''
        assert family in SERVER_FAMILIES
        assert protocol in SERVER_PROTOCOLS

        # Create a thread/non thread version of each
        for _threaded in [ False, True ]:
            _task = create_comm_server_task(
                protocol=SERVER_PROTOCOLS[protocol],
                family=SERVER_FAMILIES[family],
                threaded=_threaded
            )

            # Start the server
            _task.start()

            # Wait a bit for it to start
            time.sleep(0.1)

            # Try the client with various options
            self._send_client(
                SERVER_FAMILIES[family],
                SERVER_PROTOCOLS[protocol],
                SIMPLE_DATA_BYTES
            )

            # Stop the server
            _task.stop()


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

