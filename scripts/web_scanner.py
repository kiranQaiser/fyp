import sys

def simulate_web_scan(url):
    print(f"Scanning {url} for vulnerabilities...")
    print("Found vulnerabilities: SQL Injection, XSS")  # Dummy output

if __name__ == "__main__":
    url = sys.argv[1]
    simulate_web_scan(url)
