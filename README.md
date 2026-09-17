# Network Security MITM Analysis

A controlled network security testing project that demonstrates ARP-based
Man-in-the-Middle (MITM) positioning and DNS traffic analysis using Python
and Scapy.

This project was developed for educational and security research purposes
in an authorized local network test environment.

## Features

- ARP-based MITM positioning for controlled local network testing
- DNS query observation using Scapy packet capture
- Source IP and queried domain extraction
- Duplicate DNS query suppression within a configurable time window
- Periodic ARP poisoning to maintain test positioning
- ARP table restoration after the test is stopped
- Externalized network-specific configuration
- Git-safe configuration management using a local ignored file
- Graceful handling of missing or invalid configuration files

## Technologies

- **Python 3**
- **Scapy 2.6.1**
- **ARP (Address Resolution Protocol)**
- **Ethernet and IPv4 networking**
- **DNS (Domain Name System)**
- **Packet sniffing and traffic analysis**
- **Python threading and asynchronous packet capture**
- **Windows networking tools**

## Project Structure

```text
Network-Security-MITM-Analysis/
|-- .gitignore
|-- README.md
|-- requirements.txt
|
|-- config/
|   |-- config.example.json
|   `-- config.local.json
|
`-- src/
    `-- mitm_dns.py
```

### Configuration files

- `config.example.json` — safe template showing the required configuration fields.
- `config.local.json` — local environment configuration containing network-specific values. This file is excluded from version control through `.gitignore`.

## Configuration

Before running the project, create a local configuration file from the provided example:

```text
config/config.example.json → config/config.local.json
```

Update `config.local.json` with the values for your authorized test environment:

- `interface_index` — Scapy network interface index used for the test.
- `target_ip` — IP address of the authorized test target.
- `gateway_ip` — IP address of the network gateway.
- `target_mac` — MAC address of the authorized test target.
- `gateway_mac` — MAC address of the network gateway.
- `excluded_ip` — source IP excluded from DNS query logging.

The local configuration file is intentionally excluded from Git version control. Do not commit real IP addresses, MAC addresses, credentials, or other environment-specific information to the repository.

## Requirements

- Python 3.9 or later
- Scapy 2.6.1
- Windows operating system
- A network interface accessible to Scapy
- Administrator privileges may be required for packet capture and packet transmission

Install the Python dependency with:
```powershell
pip install -r requirements.txt
```

Verify the installation with:
```
python -c "import scapy; print(scapy.__version__)"
```

The expected version for this project is:
```
2.6.1
```

## Network Prerequisites

This project requires a controlled local network environment in which the
tester has explicit authorization to perform security testing.

Before starting the script:

1. Identify the correct network interface used for the authorized test.
2. Enable IPv4 forwarding on the appropriate Windows network interface.
3. Confirm that the interface identifier configured in `config.local.json`
   matches the interface currently used by the system.
4. Verify that the configured target and gateway addresses belong to the
   authorized test environment.

Network interface identifiers can change between systems or network
connections, so the value should not be hardcoded in the source code.

> **Safety:** Run this project only on systems and networks you own or have
> explicit permission to test.

## Execution

From the repository root, run:

```powershell
python src/mitm_dns.py
```

When started, the program:

1. Loads the local network configuration.
2. Resolves the configured Scapy network interface.
3. Starts the ARP-based MITM positioning loop.
4. Starts asynchronous DNS packet observation on port 53.
5. Displays observed DNS queries in the terminal.
6. Restores the ARP mappings when the process is stopped.

To stop the program safely, press:
```text
Ctrl+C
```

The program then stops the packet sniffer and attempts to restore the
original ARP mappings.

## How It Works

The project combines two components during a controlled network security test:

### 1. ARP-Based MITM Positioning

The script sends crafted ARP replies to the authorized target and gateway,
causing each device to associate the tester's machine with the other's IP
address.

This places the tester logically between the target and gateway at the
local network layer.

The ARP positioning loop periodically retransmits the forged mappings to
maintain the test state. When the program is stopped, legitimate ARP
mappings are sent back to the target and gateway to restore the network state.

### 2. DNS Traffic Analysis

While the ARP-based test is active, Scapy captures packets matching port 53.

The DNS analysis component:

- Identifies DNS query packets.
- Extracts the source IP address.
- Extracts the requested domain name.
- Ignores the configured excluded source IP.
- Suppresses repeated identical queries for a short time window.
- Displays the observed query in the terminal.

Example output:

```text
[DNS] 192.168.31.100 queried example.com
```

This project focuses on observing DNS query metadata in a controlled
environment. It does not decrypt HTTPS/TLS traffic.

## Security and Authorization

This project is intended strictly for:

- Personal cybersecurity learning
- Authorized penetration-testing labs
- Isolated virtual or physical test networks
- Academic and security research

Do not run the script against networks, devices, or traffic without explicit
authorization.

The repository intentionally separates environment-specific network
configuration from the source code to reduce the risk of exposing real
network information.

The author is not responsible for unauthorized use, network disruption, or
damage resulting from misuse of this software.

## Limitations

- The project is designed for controlled IPv4 local-network testing.
- DNS analysis is limited to traffic visible to the configured network
  interface and matching the capture filter.
- Encrypted DNS protocols such as DoH and DoT may prevent the queried domain
  from being visible through traditional DNS packet inspection.
- The project does not decrypt HTTPS/TLS traffic.
- Network interface identifiers may change between systems or connections.
- Successful packet capture and transmission depend on the operating system,
  network adapter, permissions, and Scapy configuration.
- The implementation is intended as an educational security-testing
  demonstration rather than a production-grade network monitoring system.

## Future Improvements

Potential improvements for future versions include:

- Add structured logging instead of terminal-only output.
- Improve configuration validation and error handling.
- Make the DNS deduplication interval configurable through the configuration
  file.
- Add support for additional DNS transport and analysis scenarios where
  technically feasible.
- Introduce automated tests for configuration loading and DNS packet parsing.
- Improve cross-platform network interface handling.
- Add packet-analysis statistics for controlled security experiments.
- Provide a dedicated test mode using simulated or replayed packet data.

## Disclaimer

This project is provided for educational, academic, and authorized security
research purposes only.

The techniques demonstrated by this project can affect network connectivity
when used improperly. Always obtain explicit authorization before performing
security testing on any network or device.

Use the project responsibly and only within environments where you have
permission to conduct testing.
