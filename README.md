[![Python Lint](https://github.com/greyinghair/template_python/actions/workflows/python-lint.yaml/badge.svg?branch=main)](https://github.com/greyinghair/template_python/actions/workflows/python-lint.yaml)

Certainly! Below is the full documentation in Markdown format, suitable for a GitHub README.md file, explaining the purpose of the script, dependencies required, deployment instructions, and step-by-step usage.

```markdown
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

## Full Python Script

Here is the full `conn_test.py` script:

```python
import socket
import json
import ipaddress
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='conn_test.log')

async def expand_ranges(config):
    expanded = []
    for entry in config:
        if "destination" in entry:
            destinations = entry["destination"]
            if isinstance(destinations, str):
                destinations = [destinations]  # Convert single destination to a list
            for dest in destinations:
                if "port" in entry:
                    expanded.append((dest, entry["port"]))
                elif "port_range" in entry:
                    port_start = entry["port_range"]["start"]
                    port_end = entry["port_range"]["end"]
                    for port in range(port_start, port_end + 1):
                        expanded.append((dest, port))
        elif "destination_range" in entry and "port" in entry:
            dest_start = entry["destination_range"]["start"]
            dest_end = entry["destination_range"]["end"]
            dest_ips = await resolve_domain_range(dest_start, dest_end)
            for dest in dest_ips:
                expanded.append((dest, entry["port"]))
    return expanded

async def resolve_domain_range(start_domain, end_domain):
    dest_ips = []
    try:
        start_ip = socket.gethostbyname(start_domain)
        end_ip = socket.gethostbyname(end_domain)
        for ip in range(int(ipaddress.IPv4Address(start_ip)), int(ipaddress.IPv4Address(end_ip)) + 1):
            dest_ips.append(str(ipaddress.IPv4Address(ip)))
    except socket.error:
        logging.error(f"Failed to resolve domain range from {start_domain} to {end_domain}.")
    return dest_ips

async def test_tcp_connectivity(loop, dest, port):
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set a timeout for connection attempt
        s.settimeout(3)
        # Attempt to connect
        await asyncio.wait_for(loop.sock_connect(s, (dest, port)), timeout=3)
        s.close()
        return "Success"
    except (socket.error, asyncio.TimeoutError) as e:
        return "Failed"

async def main():
    # Read destinations from the JSON file
    with open('destinations.json', 'r') as file:
        destinations_config = json.load(file)

    # Expand ranges to individual destinations and ports
    destinations = await expand_ranges(destinations_config)

    # Create event loop
    loop = asyncio.get_running_loop()

    # Create tasks for each destination and port
    tasks = [test_tcp_connectivity(loop, dest, port) for dest, port in destinations]
    # Execute tasks asynchronously
    results = await asyncio.gather(*tasks)

    # Write results to CSV file
    with open("results.csv", "w") as f:
        f.write("Destination,Port,Result\n")
        for (dest, port), result in zip(destinations, results):
            f.write(f"{dest},{port},{result}\n")
            logging.info(f"Test result: {dest}:{port} - {result}")

    # Print results to screen
    print("Test Results:")
    for (dest, port), result in zip(destinations, results):
        print(f"{dest}:{port} - {result}")

if __name__ == "__main__":
    asyncio.run(main())
```
```
