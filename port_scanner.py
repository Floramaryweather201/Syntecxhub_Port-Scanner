import socket
import ipaddress
from datetime import datetime

print("=== Syntecxhub Port Scanner ===")

try:
    target = input("Enter target IP address: ").strip()
    ipaddress.IPv4Address(target)

    start_port = int(input("Enter starting port: "))
    end_port = int(input("Enter ending port: "))

    if not (1 <= start_port <= end_port <= 65535):
        raise ValueError("Invalid port range")

    print(f"\nScanning {target}...\n")

    open_ports = []

    for port in range(start_port, end_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as scanner:
            scanner.settimeout(0.5)
            result = scanner.connect_ex((target, port))

            if result == 0:
                try:
                    service = socket.getservbyport(port, "tcp")
                except OSError:
                    service = "Unknown"

                print(f"[OPEN] Port {port} - {service}")
                open_ports.append((port, service))

    print("\n=== Scan Summary ===")
    print(f"Target: {target}")
    print(f"Ports scanned: {end_port - start_port + 1}")
    print(f"Open ports: {len(open_ports)}")

    filename = "scan_results.txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write("Syntecxhub Port Scanner Results\n")
        file.write(f"Scan date: {datetime.now()}\n")
        file.write(f"Target: {target}\n")
        file.write(f"Port range: {start_port}-{end_port}\n\n")

        for port, service in open_ports:
            file.write(f"Port {port}: OPEN - {service}\n")

        file.write(f"\nTotal open ports: {len(open_ports)}\n")

    print(f"\nResults saved to {filename}")
    print("Scan completed!")

except ValueError as error:
    print(f"Invalid input: {error}")
except OSError as error:
    print(f"Error: {error}")
