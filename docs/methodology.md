# Methodology

## 1. Problem Statement

Local IPv4 networks use ARP to associate IP addresses with MAC addresses. Because traditional ARP does not inherently authenticate these mappings, malicious or malformed ARP responses can potentially cause incorrect IP-to-MAC associations.

This project was created to study this behavior in a controlled environment.

## 2. Objective

The objective is to demonstrate:

- ARP packet construction.
- ARP cache manipulation concepts.
- Controlled MITM positioning.
- DNS packet observation.
- Packet-level network analysis using Python and Scapy.
- Basic restoration of modified ARP information.

## 3. Test Environment

The implementation assumes a controlled local IPv4 network containing:

- A testing machine running the Python program.
- An authorized test target.
- A local network gateway.
- A network interface through which the test traffic can be observed.

Actual IP addresses, MAC addresses, and interface identifiers used during development are intentionally excluded from the public repository.

## 4. High-Level Methodology

The application performs two related activities.

### ARP Testing

The program constructs Ethernet frames containing ARP responses.

During the controlled test, ARP responses are sent toward the authorized target and gateway at regular intervals.

This demonstrates how incorrect ARP associations can affect local network traffic paths.

### DNS Observation

The program starts an asynchronous packet sniffer and applies a port-53 filter.

When an IPv4 DNS query is observed, the application extracts the source IP address and queried domain name.

A short deduplication interval prevents the same source/domain combination from producing excessive repeated console output.

## 5. Traffic Observation

The DNS component is designed to demonstrate visibility into DNS queries that are available to the monitoring point.

A simplified representation of the observed information is:

```text
Source IP → DNS Query
```

For example:

```text
Test Client → example.test
```

The repository does not contain real private-network observations.

## 6. Restoration

When the test is interrupted, the program attempts to send corrective ARP information to the test devices.

The purpose is to restore the expected IP-to-MAC mappings used by the authorized laboratory network.

## 7. Security Implications

The experiment demonstrates the importance of protecting local network infrastructure against ARP-based traffic manipulation.

Defensive approaches can include:

- Dynamic ARP Inspection.
- Network segmentation.
- ARP monitoring.
- Static ARP entries where operationally appropriate.
- Detection of unexpected IP/MAC changes.
- Encrypted application protocols.
- Network-level anomaly monitoring.

## 8. Limitations

The current implementation is intentionally limited to a learning-oriented demonstration.

It does not provide:

- General-purpose traffic interception.
- TLS decryption.
- Automated vulnerability discovery.
- Automated attack detection.
- Enterprise network monitoring.
- Analysis of encrypted DNS protocols.

## 9. Ethical Considerations

The experiment should only be performed against systems and networks for which explicit authorization has been obtained.

The project is intended for cybersecurity education, networking research, and controlled laboratory testing.

Unauthorized interception or manipulation of network traffic can violate organizational policies and applicable laws.
