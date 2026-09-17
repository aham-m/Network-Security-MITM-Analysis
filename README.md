# Network Security Analysis & Controlled MITM Simulation

A Python and Scapy-based cybersecurity project demonstrating controlled Man-in-the-Middle (MITM) positioning through ARP spoofing and observation of DNS queries in an authorized laboratory network environment.

## Overview

This project was developed as a practical exploration of computer networking and network security concepts.

The implementation uses **Python and Scapy** to demonstrate how ARP-based traffic redirection can position a testing machine between two devices on a local network. It then monitors DNS traffic and records observed DNS queries for analysis.

The project is intended for **educational use, controlled laboratory environments, and networks where explicit authorization has been obtained**.

## Objectives

The primary objectives of the project are to:

- Understand ARP communication and ARP cache behavior.
- Demonstrate the concept of ARP-based Man-in-the-Middle positioning.
- Capture and analyze DNS query packets.
- Understand the relationship between Ethernet, ARP, IP and DNS traffic.
- Explore packet-level network analysis using Scapy.
- Practice Python-based network automation and troubleshooting.
- Demonstrate the security implications of weak ARP trust mechanisms.

## Features

- Ethernet and ARP packet construction using Scapy.
- Controlled bidirectional ARP spoofing demonstration.
- Continuous ARP packet transmission during the test.
- DNS query packet monitoring.
- Extraction of source IP and queried domain.
- Duplicate-query suppression using a configurable time interval.
- Graceful interruption using `Ctrl+C`.
- ARP table restoration when the test terminates.
- Console-based security-testing output.

## Technologies Used

- **Python**
- **Scapy**
- **TCP/IP networking**
- **Ethernet**
- **ARP**
- **DNS**
- **Packet sniffing**
- **Python threading**

## Networking Concepts Demonstrated

### ARP

Address Resolution Protocol (ARP) is used on IPv4 local networks to associate IP addresses with MAC addresses.

The project demonstrates how manipulating ARP responses can affect the local network's IP-to-MAC mappings.

### Man-in-the-Middle Positioning

The project demonstrates the concept of positioning a testing machine between a target device and its gateway through manipulated ARP information.

This is performed only within an authorized test environment.

### DNS Traffic

The sniffer monitors DNS traffic on port 53 and identifies DNS query packets.

For observed queries, the program records:

```text
Source IP → Requested Domain
```

Example format:

```text
[DNS] <test-client-ip> queried example.test
```

Actual network addresses used during testing are intentionally not included in this repository.

## High-Level Workflow

```text
                 Controlled Test Network

             ┌──────────────────────┐
             │       Gateway        │
             └──────────┬───────────┘
                        │
                        │
                 ┌──────┴──────┐
                 │ Test Machine│
                 │ Python/Scapy│
                 └──────┬──────┘
                        │
                        │
                 ┌──────┴──────┐
                 │ Test Target │
                 │   Device    │
                 └─────────────┘
```

At a high level:

```text
1. Identify the authorized test devices.
            ↓
2. Send controlled ARP responses.
            ↓
3. Position the testing machine in the
   intended laboratory traffic path.
            ↓
4. Monitor DNS query traffic.
            ↓
5. Record relevant DNS observations.
            ↓
6. Stop the test.
            ↓
7. Restore ARP information.
```

## Requirements

- Python 3.x
- Scapy
- Network interface capable of accessing the authorized test network.
- Administrative/root privileges may be required depending on the operating system and packet-capture configuration.

## Installation

Clone the repository:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd network-security-mitm-analysis
```

Create a virtual environment:

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the required Python dependency:

```bash
pip install -r requirements.txt
```

## Configuration

The original development version used machine-specific network values.

These values should **not** be committed to the public repository.

Before running the project, configure the required laboratory network parameters locally.

The configuration should contain only information belonging to the authorized test environment, such as:

- testing interface
- target IP address
- gateway IP address
- target MAC address
- gateway MAC address
- optional local filtering/exclusion address

See:

```text
config/config.example
```

for the expected configuration format.

Do not commit private credentials, personal network information, or unrelated device information.

## Running the Project

After configuring the authorized laboratory environment, run the Python program according to the instructions in the source file.

The program starts the controlled ARP testing process and DNS monitoring process.

During execution, DNS observations are displayed in the console.

Example:

```text
[*] Starting ARP spoofing and DNS sniffing...
[DNS] <source-ip> queried <domain>
```

The exact output depends on the traffic generated by the test environment.

Press:

```text
Ctrl+C
```

to stop the test.

The program then attempts to restore the ARP information used during the demonstration.

## Methodology

The project combines two activities:

1. Controlled ARP manipulation for demonstrating MITM positioning.
2. DNS packet observation for studying application-layer name-resolution traffic.

The ARP component repeatedly sends crafted ARP responses to the authorized test devices.

The DNS component uses Scapy's asynchronous packet-sniffing functionality and examines IPv4 DNS query packets.

The implementation also applies a short deduplication interval to reduce repeated console output for the same source-IP/domain combination.

A detailed methodology is available in:

```text
docs/methodology.md
```

## Security Implications

The project demonstrates why relying solely on unauthenticated ARP communication can expose local IPv4 networks to traffic-redirection attacks.

Potential defensive considerations include:

- Static ARP entries where appropriate.
- Dynamic ARP Inspection on supported network infrastructure.
- Network segmentation.
- Monitoring for unexpected ARP changes.
- Detection of duplicate or conflicting IP/MAC mappings.
- Use of encrypted application-layer protocols.
- DNS security monitoring and appropriate network controls.

## Limitations

This project is a learning-oriented demonstration rather than a production penetration-testing framework.

Current limitations include:

- Designed around a controlled local IPv4 network.
- Requires appropriate network privileges.
- DNS visibility depends on the traffic available to the testing machine.
- Encrypted DNS protocols such as DoH/DoT are not analyzed by the current implementation.
- The implementation is not intended to provide general-purpose traffic interception.
- Configuration is environment-dependent.
- No automated attack detection or defensive monitoring component is currently included.

## Ethical and Legal Use

This project must only be used on:

- Networks you own.
- Laboratory environments.
- Devices you own.
- Systems for which you have explicit authorization to perform security testing.

Do not use the implementation to intercept, redirect, monitor, or manipulate traffic belonging to other users or networks without authorization.

The author does not encourage unauthorized network interception or disruption.

## Future Improvements

Potential educational improvements include:

- Cleaner configuration management.
- Better packet-analysis reporting.
- Structured logging.
- Additional defensive detection mechanisms.
- Visualization of DNS observations.
- Automated laboratory setup documentation.
- Comparison of normal and anomalous ARP behavior.

## Project Structure

```text
network-security-mitm-analysis/
│
├── README.md
├── requirements.txt
├── LICENSE
├── .gitignore
│
├── src/
│   └── mitm_dns_analysis.py
│
├── config/
│   └── config.example
│
├── docs/
│   └── methodology.md
│
└── screenshots/
```

## Author

**Aham Mondal**

B.Tech Information Technology Graduate

Interested in:

- Software Development
- Computer Networks
- Cybersecurity
- Network Security
- Python
- Java

---

## Disclaimer

This repository is provided for educational and authorized security-testing purposes only. Always obtain explicit permission before performing security testing or packet analysis on a network or device.