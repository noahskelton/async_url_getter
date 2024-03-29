# Asynchronous URL request getter

This is a CLI program that makes requests to N URLs in parallel. A text file with
newline separated URLs is given along with a timeout value, and a live output of each request along with its status code
and time taken is printed to stdout. After all requests have completed or the timeout specified has been reached,
some metrics of all requests are printed.

Tested on Python 3.8.

## Usage

Install the project requirements:
```
pip install .
```
A path to a text file is passed as an argument.  An optional
timeout can be specified as an integer, the default is 15 seconds and the minimum value is 1. 
A sample `url_list.txt` file of 100 URLs is included.

Run the program with an url_list and timeout of 10:
```
async-url-getter url_list.txt -t 10
```
In this example, there is a malformed URL and a server that does not respond within the timeout.

Sample output:

```
Connection error resolving http://www.youtubecom
Request to http://www.google.co.in responded with 200 and took 85.508ms to complete
Request to http://www.qq.com responded with 200 and took 112.648ms to complete
Request to http://www.bing.com responded with 200 and took 112.218ms to complete
Request to http://www.live.com responded with 200 and took 139.203ms to complete
Request to https://www.facebook.com responded with 200 and took 214.877ms to complete
Request to http://www.wikipedia.org responded with 200 and took 218.625ms to complete
Request to http://www.instagram.com responded with 200 and took 273.725ms to complete
Request to http://www.yahoo.com responded with 200 and took 475.64ms to complete
Request to http://www.amazon.com responded with 200 and took 755.536ms to complete
Request to http://www.twitter.com responded with 200 and took 1008.309ms to complete
Request to http://www.taobao.com responded with 200 and took 1222.272ms to complete
Request to http://www.weibo.com responded with 200 and took 3237.769ms to complete
Request to http://www.microsoftonline.com timed out after 10 seconds
Request to http://www.rakuten.co.jp timed out after 10 seconds
-----
Mean response time = 654.694ms
Median response time = 246.175ms
90th percentile of response times = 2633.12ms

```

## How to run the tests:

Install test requirements:

```
pip install -r dev-requirements.txt
```

Run tests:

```
pytest
```

## Decisions made:

- A default value of 15 seconds for the timeout was specified. This can be specified with the `--timeout` option.

- Metrics are rounded to three decimal places for readability.

- I used the `click` library for CLI functionality as it is easily testable compared to argparse.

- URLs that are not prefixed with `http://` or `https://` are fixed and prepended with `http://`. For example, 
`test.com` would be parsed and modified in place to `http://test.com`. Requests made to a URL without this prefix
would otherwise raise an InvalidURL exception. Python's `urllib` is not used here, as the `netloc` attribute of an 
`urlparse` object is not properly assigned by urllib if it does not start with `//`. For simplicity's sake, simple
string checking was used instead.
[Reference](https://docs.python.org/3.7/library/urllib.parse.html?highlight=urlparse#url-parsing)

- The tests are comprehensive and have thorough coverage. Mock requests were used to avoid making real-world requests
and to ensure reproducibility.

- `aiohttp` was used as it is an actively maintained and popular library for making asynchronous HTTP requests.

- There is a default connection limit of 100 simultaneous requests using the `aiohttp` client. In the future,
custom connection limits could be implemented.
 
- The code has full test coverage, fully typed with `mypy` and linted with `flake8`:

```
pytest --cov-fail-under 100 --cov tests/  --cov src/
flake8 .
mypy tests src
```