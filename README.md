[![Python Lint](https://github.com/greyinghair/template_python/actions/workflows/python-lint.yaml/badge.svg?branch=main)](https://github.com/greyinghair/template_python/actions/workflows/python-lint.yaml)

# TCP Connectivity Tester

This Python script allows you to test TCP connectivity to multiple destinations and ports simultaneously. It is useful for network diagnostics, troubleshooting, and validating connectivity from servers to specified endpoints.

## Features

- Test TCP connectivity to multiple destinations and ports.
- Support for specifying single destinations, lists of destinations, single ports, and port ranges.
- Asynchronous execution to perform tests simultaneously.
- Output results to both the console and a CSV file.
- Detailed logging of test results.

## Dependencies

- **Python 3.7 or later**: Ensure Python is installed on your system. You can download Python from the [official website](https://www.python.org/downloads/).
- **asyncio**: Asynchronous I/O framework included in the Python standard library.
- **ipaddress**: Library for working with IP addresses and networks. It is included in the Python standard library.
- **Logging**: Built-in logging module for capturing detailed logs of the tests.

## Installation

1. **Clone the Repository**: Clone the GitHub repository containing the script to your local machine.

   ```bash
   git clone https://github.com/your_username/your_repository.git
   ```

2. **Navigate to the Repository Directory**:

   ```bash
   cd your_repository
   ```

3. **Install Dependencies**: Install the required dependencies using pip.

   ```bash
   pip install asyncio ipaddress
   ```

## Configuration

1. **Edit `destinations.json`**: Modify the `destinations.json` file to include the destinations and ports you want to test. Below is an example configuration:

    ```json
    [
        {"destination": ["example.com", "example2.com"], "port_range": {"start": 80, "end": 85}},
        {"destination_range": {"start": "10.0.0.1", "end": "10.0.0.3"}, "port": 443},
        {"destination": "www.pypi.org", "port": 443},
        {"destination": "192.168.1.1", "port_range": {"start": 8000, "end": 8010}}
    ]
    ```

    This JSON structure allows you to specify destinations as single strings or lists of strings and specify ports as single ports or port ranges.

## Usage

1. **Execute the Script**: Run the script `conn_test.py` from the command line.

   ```bash
   python conn_test.py
   ```

2. **View Results**: The script will generate a CSV file named `results.csv` containing the test results. Additionally, the results will be printed to the console.

### Example Output

**Console Output:**
```
Test Results:
example.com:80 - Success
example.com:81 - Success
example.com:82 - Success
example.com:83 - Success
example.com:84 - Success
example.com:85 - Success
example2.com:80 - Success
example2.com:81 - Success
example2.com:82 - Success
example2.com:83 - Success
example2.com:84 - Success
example2.com:85 - Success
10.0.0.1:443 - Failed
10.0.0.2:443 - Failed
10.0.0.3:443 - Failed
www.pypi.org:443 - Success
192.168.1.1:8000 - Failed
192.168.1.1:8001 - Failed
192.168.1.1:8002 - Failed
192.168.1.1:8003 - Failed
192.168.1.1:8004 - Failed
192.168.1.1:8005 - Failed
192.168.1.1:8006 - Failed
192.168.1.1:8007 - Failed
192.168.1.1:8008 - Failed
192.168.1.1:8009 - Failed
192.168.1.1:8010 - Failed
```

**CSV File (`results.csv`):**
```
Destination,Port,Result
example.com,80,Success
example.com,81,Success
example.com,82,Success
example.com,83,Success
example.com,84,Success
example.com,85,Success
example2.com,80,Success
example2.com,81,Success
example2.com,82,Success
example2.com,83,Success
example2.com,84,Success
example2.com,85,Success
10.0.0.1,443,Failed
10.0.0.2,443,Failed
10.0.0.3,443,Failed
www.pypi.org,443,Success
192.168.1.1,8000,Failed
192.168.1.1,8001,Failed
192.168.1.1,8002,Failed
192.168.1.1,8003,Failed
192.168.1.1,8004,Failed
192.168.1.1,8005,Failed
192.168.1.1,8006,Failed
192.168.1.1,8007,Failed
192.168.1.1,8008,Failed
192.168.1.1,8009,Failed
192.168.1.1,8010,Failed
```
