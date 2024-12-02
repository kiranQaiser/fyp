import subprocess
import ipaddress


def nmap_scan(target, start_port=1, end_port=65535):
    """
    Scans the target IP address or range using Nmap to find open ports and their services.
    
    Parameters:
    - target (str): IP address or range to scan.
    - start_port (int): Start port for scanning.
    - end_port (int): End port for scanning.
    """
    try:
        print(f"Scanning {target} for open ports and services...")
        
        # Construct the Nmap command
        command = [
            "nmap",
            f"-p{start_port}-{end_port}",
            "-sV",  # Service version detection
            target
        ]
        
        # Run the Nmap command and capture the output
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        # Parse and print the results
        print("\nScan Results:")
        for line in result.stdout.splitlines():
            if "open" in line:  # Look for lines with open ports
                print(line)
        
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running Nmap: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def main():
    """
    Main function to take user input for scanning.
    """
    choice = input("Do you want to scan a single IP or a range of IPs? (s/r): ").strip().lower()
    
    if choice == "s":
        # Single IP address
        target_ip = input("Enter the IP address to scan: ").strip()
        try:
            ipaddress.ip_address(target_ip)  # Validate IP address
            nmap_scan(target_ip)
        except ValueError:
            print("Invalid IP address.")
    
    elif choice == "r":
        # Range of IPs
        start_ip = input("Enter the starting IP address of the range: ").strip()
        end_ip = input("Enter the ending IP address of the range: ").strip()
        try:
            # Validate IP addresses
            start_ip = ipaddress.ip_address(start_ip)
            end_ip = ipaddress.ip_address(end_ip)
            
            # Generate IPs in the range and scan each
            current_ip = start_ip
            while current_ip <= end_ip:
                nmap_scan(str(current_ip))
                current_ip += 1
        except ValueError:
            print("Invalid IP range.")
    
    else:
        print("Invalid choice. Please enter 's' for single IP or 'r' for IP range.")


if __name__ == "__main__":
    main()
