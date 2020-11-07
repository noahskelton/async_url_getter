import pytest
from aiohttp import ClientConnectorError
import time
from main import get, main
import aiohttp
from aioresponses import aioresponses, CallbackResult
from socket import gaierror
from aiohttp.client_reqrep import ConnectionKey
import asyncio



class TestCLI:
    def test_file_input_valid(self) -> None:
        pass

    def test_file_input_invalid(self) -> None:
        pass

    def test_timeout_valid(self) -> None:
        pass

    def test_timeout_invalid(self) -> None:
        pass

@pytest.fixture
def mock_aioresponse():
    with aioresponses() as m:
        yield m

class TestGet:
    async def test_valid_url(self, mock_aioresponse) -> None:
        session = aiohttp.ClientSession()
        valid_url = 'https://google.com'
        status = 200
        mock_aioresponse.get(valid_url, status=status)
        timeout = 10
        result = await get(session=session, url=valid_url, timeout=timeout)
        assert result.url == valid_url
        assert result.total_time < timeout
        assert result.status_code == status

    async def test_invalid_url(self, mock_aioresponse) -> None:
        session = aiohttp.ClientSession()
        valid_url = 'https://google.com'
        connection_key = ConnectionKey(host=valid_url, port=80, is_ssl=False, ssl=None, proxy=None, proxy_auth=None, proxy_headers_hash=None)
        os_error = gaierror(8, 'nodename nor servname provided, or not known')

        exception = ClientConnectorError(connection_key=connection_key, os_error=os_error)
        mock_aioresponse.get(valid_url, exception=exception)
        timeout = 10
        with pytest.raises(ClientConnectorError):
            result = await get(session=session, url=valid_url, timeout=timeout)

    async def test_timeout(self, mock_aioresponse) -> None:

        session = aiohttp.ClientSession()
        url = 'https://google.com'
        mock_aioresponse.get(url, exception=TimeoutError)

        timeout = 2
        with pytest.raises(TimeoutError):
            result = await get(session=session, url=url, timeout=timeout)


class TestMain:
    async def test_start_time(self, mock_aioresponse) -> None:

        request_delay = 1
        async def delay_request(*args, **kwargs):
            await asyncio.sleep(request_delay)

        url_1 = 'foo.com'
        url_2 = 'bar.com'
        urls = [url_1, url_2]
        for url in urls:
            mock_aioresponse.get(url, callback=delay_request)
            mock_aioresponse.get(url, callback=delay_request)
        start = time.monotonic()
        await main(url_list=urls, timeout=4)
        end = time.monotonic()
        time_taken = round(end - start)
        assert time_taken == request_delay

    async def test_valid_url(self, mock_aioresponse) -> None:
        url_1 = 'foo.com'
        urls = [url_1]
        status = 200
        mock_aioresponse.get(url_1, status=status)
        result = await main(url_list=urls, timeout=1)
        assert len(result) == 1
        request_info = result[0]
        assert request_info.status_code == status
        assert request_info.url == url_1
        assert request_info.total_time < 1

    async def test_valid_urls(self, mock_aioresponse) -> None:
        url_1 = 'foo.com'
        url_2 = 'bar.com'
        status_url_1 = 200
        status_url_2 = 201
        urls = [url_1, url_2]
        mock_aioresponse.get(url_1, status=status_url_1)
        mock_aioresponse.get(url_2, status=status_url_2)
        result = await main(url_list=urls, timeout=1)

        [request_info_1] = [info for info in result if info.url == url_1]
        [request_info_2] = [info for info in result if info.url == url_2]

        assert request_info_1.total_time < 1
        assert request_info_2.total_time < 1

        assert request_info_1.status_code == status_url_1
        assert request_info_2.status_code == status_url_2


    def test_invalid_url(self) -> None:
        pass

    def test_timeout(self) -> None:
        pass



class TestMetrics:
    def test_statistics(self) -> None:
        pass

    def test_string_output(self) -> None:
        pass