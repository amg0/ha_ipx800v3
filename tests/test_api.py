"""Tests for the MyIPX800V3 API client."""

import aiohttp
import pytest

from custom_components.my_ipx800v3.api.client import MyIPX800V3ApiClient


@pytest.mark.asyncio
async def test_api_counter_methods(aioclient_mock):
    """Test counter methods."""
    async with aiohttp.ClientSession() as session:
        client = MyIPX800V3ApiClient("1.2.3.4", 80, "user", "pass", session)

        # Test set counter
        aioclient_mock.get(
            "http://1.2.3.4:80/protect/assignio/counter1.htm?num=0&counter=100",
            text="OK",
            status=200,
        )
        await client.async_set_counter(0, 100)
        assert aioclient_mock.call_count == 1

        # Test increment counter
        aioclient_mock.get(
            "http://1.2.3.4:80/protect/assignio/counter1.htm?num=1&inc=50",
            text="OK",
            status=200,
        )
        await client.async_increment_counter(1, 50)
        assert aioclient_mock.call_count == 2

        # Test decrement counter
        aioclient_mock.get(
            "http://1.2.3.4:80/protect/assignio/counter1.htm?num=2&dec=10",
            text="OK",
            status=200,
        )
        await client.async_decrement_counter(2, 10)
        assert aioclient_mock.call_count == 3

        # Test validation
        with pytest.raises(ValueError, match="Counter index must be between 0 and 7"):
            await client.async_set_counter(8, 100)

        with pytest.raises(ValueError, match="Increment amount must be between 1 and 255"):
            await client.async_increment_counter(0, 256)

        with pytest.raises(ValueError, match="Decrement amount must be between 1 and 255"):
            await client.async_decrement_counter(0, 0)
