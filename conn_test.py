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
