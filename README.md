[![Python Lint](https://github.com/greyinghair/template_python/actions/workflows/python-lint.yaml/badge.svg?branch=main)](https://github.com/greyinghair/template_python/actions/workflows/python-lint.yaml)

markdown
Copy code
# TCP Connectivity Tester

This Python script allows you to test TCP connectivity to multiple destinations and ports simultaneously.

## Setup

1. **Clone the Repository**: Clone the GitHub repository containing the script to your local machine.

   ```bash
   git clone https://github.com/your_username/your_repository.git
Install Python: Ensure Python 3.7 or later is installed on your system. You can download Python from the official website.

Install Dependencies: Install the required dependencies using pip.

bash
Copy code
pip install asyncio ipaddress
Configuration
Edit destinations.json: Modify the destinations.json file to include the destinations and ports you want to test. You can follow the provided example:

json
Copy code
[
    {"destination": ["example.com", "example2.com"], "port_range": {"start": 80, "end": 85}},
    {"destination_range": {"start": "10.0.0.1", "end": "10.0.0.3"}, "port": 443},
    {"destination": "www.pypi.org", "port": 443},
    {"destination": "192.168.1.1", "port_range": {"start": 8000, "end": 8010}}
]
This JSON structure allows you to specify destinations as single strings or lists of strings and specify ports as single ports or port ranges.

Running the Script
Execute the Script: Run the script conn_test.py from the command line.

bash
Copy code
python conn_test.py
The script will perform TCP connectivity tests to the destinations and ports specified in destinations.json.

View Results: The script will generate a CSV file named results.csv containing the test results. Additionally, the results will be printed to the console.

Dependencies
asyncio: Asynchronous I/O framework included in Python standard library.
ipaddress: Library for working with IP addresses and networks.
Notes
Ensure that the script conn_test.py and the destinations.json file are in the same directory.
Customize the destinations.json file according to your specific testing needs.
You can integrate this script into automated testing pipelines or use it for network diagnostics and troubleshooting.
