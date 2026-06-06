"""
API Client for my_ipx800v3.

This module provides the API client for communicating with the GCE IPX800 V3.
It handles fetching state from globalstatus.xml and controlling outputs.
"""

from __future__ import annotations

import asyncio
import socket
from typing import Any
import xml.etree.ElementTree as ET

import aiohttp


class MyIPX800V3ApiClientError(Exception):
    """Base exception to indicate a general API error."""


class MyIPX800V3ApiClientCommunicationError(
    MyIPX800V3ApiClientError,
):
    """Exception to indicate a communication error with the API."""


class MyIPX800V3ApiClientAuthenticationError(
    MyIPX800V3ApiClientError,
):
    """Exception to indicate an authentication error with the API."""


def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """
    Verify that the API response is valid.

    Raises appropriate exceptions for authentication and HTTP errors.

    Args:
        response: The aiohttp ClientResponse to verify.

    Raises:
        MyIPX800V3ApiClientAuthenticationError: For 401/403 errors.
        aiohttp.ClientResponseError: For other HTTP errors.

    """
    if response.status in (401, 403):
        msg = "Invalid credentials"
        raise MyIPX800V3ApiClientAuthenticationError(
            msg,
        )
    response.raise_for_status()


class MyIPX800V3ApiClient:
    """
    API Client for GCE IPX800 V3.

    Handles communication with the local IPX800 V3 board via HTTP XML polling
    and HTTP preset endpoints.
    """

    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """
        Initialize the API Client.

        Args:
            host: The host/IP address of the IPX800 V3.
            port: The HTTP port of the IPX800 V3.
            username: The optional username for authentication from config flow.
            password: The optional password for authentication from config flow.
            session: The aiohttp ClientSession to use for requests.

        """
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._session = session
        self._base_url = f"http://{host}:{port}"

    @property
    def base_url(self) -> str:
        """Get the base URL for the API client."""
        return self._base_url

    async def async_get_data(self) -> dict[str, str]:
        """
        Get all data from the IPX800 V3 board.

        Fetches the complete status in a single request to globalstatus.xml
        to minimize load on the board.

        Returns:
            A flat dictionary of tag-value pairs.

        Raises:
            MyIPX800V3ApiClientAuthenticationError: If authentication fails.
            MyIPX800V3ApiClientCommunicationError: If communication fails.
            MyIPX800V3ApiClientError: For other API errors.

        """
        url = f"{self._base_url}/globalstatus.xml"

        auth = None
        if self._username and self._password:
            auth = aiohttp.BasicAuth(self._username, self._password)

        xml_text = await self._api_wrapper(
            method="get",
            url=url,
            auth=auth,
            is_xml=True,
        )

        try:
            root = ET.fromstring(xml_text)  # noqa: S314
        except ET.ParseError as exception:
            msg = f"Failed to parse XML response from IPX800 V3: {exception}"
            raise MyIPX800V3ApiClientError(msg) from exception

        data = {}
        for child in root:
            if child.tag:
                data[child.tag] = child.text or ""

        # Default version to Unknown if not in XML
        if "version" not in data:
            data["version"] = "3.05.xx"

        return data

    async def async_get_names(self) -> dict[str, str]:
        """
        Get all data from the IPX800 V3 board.

        Fetches the names from ionames.xml.

        Returns:
            A flat dictionary of tag-value pairs.

        Raises:
            MyIPX800V3ApiClientAuthenticationError: If authentication fails.
            MyIPX800V3ApiClientCommunicationError: If communication fails.
            MyIPX800V3ApiClientError: For other API errors.

        """
        url = f"{self._base_url}/ioname.xml"

        auth = None
        if self._username and self._password:
            auth = aiohttp.BasicAuth(self._username, self._password)

        xml_text = await self._api_wrapper(
            method="get",
            url=url,
            auth=auth,
            is_xml=True,
        )

        try:
            root = ET.fromstring(xml_text)  # noqa: S314
        except ET.ParseError as exception:
            msg = f"Failed to parse XML response from IPX800 V3: {exception}"
            raise MyIPX800V3ApiClientError(msg) from exception

        data = {}
        for child in root:
            if child.tag:
                data[child.tag] = child.text or ""

        return data

    async def async_set_relay(self, relay_index: int, state: bool) -> Any:
        """
        Set the state of a relay (0-indexed relay_index, e.g. 0 to 31).

        Uses /preset.htm?setX=1 or 0 where X = relay_index + 1.

        Args:
            relay_index: The 0-based index of the relay (0 maps to set1).
            state: True for ON (1), False for OFF (0).

        Returns:
            The API response text.

        Raises:
            MyIPX800V3ApiClientAuthenticationError: If authentication fails.
            MyIPX800V3ApiClientCommunicationError: If communication fails.
            MyIPX800V3ApiClientError: For other API errors.

        """
        param_num = relay_index + 1
        param_val = 1 if state else 0

        url = f"{self._base_url}/preset.htm"
        params = {f"set{param_num}": param_val}

        auth = None
        if self._username and self._password:
            auth = aiohttp.BasicAuth(self._username, self._password)

        return await self._api_wrapper(
            method="get",
            url=url,
            auth=auth,
            params=params,
            is_xml=True,
        )

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
        params: dict | None = None,
        auth: aiohttp.BasicAuth | None = None,
        is_xml: bool = False,
    ) -> Any:
        """
        Wrapper for API requests with error handling.

        Args:
            method: The HTTP method (get, post, etc.).
            url: The URL to request.
            data: Optional data to send in the request body.
            headers: Optional headers to include in the request.
            params: Optional query parameters.
            auth: Optional HTTP Basic Authentication.
            is_xml: If True, returns response as raw text instead of JSON.

        Returns:
            The JSON response, or raw text if is_xml is True.

        Raises:
            MyIPX800V3ApiClientAuthenticationError: If authentication fails.
            MyIPX800V3ApiClientCommunicationError: If communication fails.
            MyIPX800V3ApiClientError: For other API errors.

        """
        try:
            async with asyncio.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                    params=params,
                    auth=auth,
                )
                _verify_response_or_raise(response)
                if is_xml:
                    return await response.text()
                return await response.json()

        except TimeoutError as exception:
            msg = f"Timeout error fetching information - {exception}"
            raise MyIPX800V3ApiClientCommunicationError(
                msg,
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise MyIPX800V3ApiClientCommunicationError(
                msg,
            ) from exception
        except Exception as exception:
            msg = f"Something really wrong happened! - {exception}"
            raise MyIPX800V3ApiClientError(
                msg,
            ) from exception
