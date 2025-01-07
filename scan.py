import requests
import re
import os
import hashlib
from bs4 import BeautifulSoup


class Scan:
    url = ''
    insecure_set = set()
    sqli_set = set()
    xss_set = set()
    csrf_set = set()
    ssrf_set = set()
    lfi_set = set()
    rce_set = set()

    def __init__(self, url, insecure_set, sqli_set, xss_set, csrf_set, ssrf_set, lfi_set, rce_set):
        Scan.url = url
        self.insecure_set = insecure_set
        self.sqli_set = sqli_set
        self.xss_set = xss_set
        self.csrf_set = csrf_set
        self.ssrf_set = ssrf_set
        self.lfi_set = lfi_set
        self.rce_set = rce_set

    @staticmethod
    def is_url_insecure(scan_this_url):
        if not scan_this_url.startswith("https"):
            Scan.insecure_set.add(scan_this_url)
            return True
        else:
            return False

    @staticmethod
    def is_url_vulnerable_to_sql_injection(scan_this_url):
        # List of common SQL injection payloads
        payloads = [
            "'OR'1'='1",
            "' OR 'a'='a",
            '" OR "a"="a',
            "' OR 1=1 --",
            '" OR 1=1 --"'
        ]

        for payload in payloads:
            try:
                # GET request with the SQL injection payload
                response = requests.get(scan_this_url + "?id=" + payload, timeout=10)

                # Check if the response contains any signs of SQL errors or unusual behavior
                if re.search(r"error|warning|syntax|mysql_fetch_assoc|sql|unclosed|unexpected", response.text,
                             re.IGNORECASE):
                    # Add the URL to the SQL injection set if it seems vulnerable
                    Scan.sqli_set.add(scan_this_url)
                    print(f"SQL Injection vulnerability detected in the URL: {scan_this_url}")
                    break   # no need to check further
                elif response.status_code == 500:
                    # Server error could indicate SQL injection attempt
                    print(f"500 error detected while testing SQL Injection on {scan_this_url}. Possible SQL Injection vulnerability.")
                    Scan.sqli_set.add(scan_this_url)
                    break
                else:
                    print(f"No SQL Injection vulnerability detected in the URL: {scan_this_url}")
            except requests.exceptions.RequestException as e:
                # Handle network errors or timeouts
                print(f"Error while testing SQL Injection for URL {scan_this_url}: {e}")

        return Scan.sqli_set

    @staticmethod
    def is_url_vulnerable_to_xss(scan_this_url):
        # List of common XSS payloads
        payloads = [
            "<script>alert('XSS')</script>",  # Basic XSS payload
            "<img src='x' onerror='alert(1)'>",  # XSS via image error handler
            "<svg onload=alert('XSS')>",  # XSS via SVG onload event
            "<a href='javascript:alert(1)'>Click me</a>",  # XSS via JavaScript in href
            "<body onload=alert('XSS')>"  # XSS via body onload event
        ]

        for payload in payloads:
            try:
                # GET request with the XSS payload
                response = requests.get(scan_this_url + "?input=" + payload, timeout=10)

                # Check if the payload or a similar form of XSS appears in the response
                if re.search(r"<script.*?alert\('XSS'\).*?>", response.text, re.IGNORECASE) or \
                        re.search(r"onerror\s*=\s*['\"]?alert\('XSS'\)", response.text, re.IGNORECASE) or \
                        re.search(r"onload\s*=\s*['\"]?alert\('XSS'\)", response.text, re.IGNORECASE):
                    # If XSS is reflected in any form, add the URL to the XSS vulnerable set
                    Scan.xss_set.add(scan_this_url)
                    print(f"XSS vulnerability detected in the URL: {scan_this_url}")
                    break  # No need to check further
                else:
                    print(f"No XSS vulnerability detected in the URL: {scan_this_url}")

            except requests.exceptions.RequestException as e:
                # Handle network errors or timeouts
                print(f"Error while testing XSS for URL {scan_this_url}: {e}")

        return Scan.xss_set

    @staticmethod
    def is_url_vulnerable_to_csrf(scan_this_url):
        try:
            # Generate CSRF token
            # csrf_token = Scan.generate_csrf_token()

            # GET request to get the page content
            response = requests.get(scan_this_url, timeout=10)

            # Check if the CSRF token pattern is present in the response
            if "csrf_token" in response.text:
                # Use BeautifulSoup to parse the HTML and extract the CSRF token safely
                soup = BeautifulSoup(response.text, 'html.parser')
                token_element = soup.find('input', {'name': 'csrf_token'})  # Adjust the selector as needed

                if token_element:
                    csrf_token = token_element.get('value', '')
                    if csrf_token:
                        payload = {"csrf_token": csrf_token}  # Create the payload with the CSRF token

                        # POST request with the token in the payload
                        post_response = requests.post(scan_this_url, data=payload, timeout=10)

                        # Check for specific signs of CSRF protection failure (e.g., missing token or failure message)
                        if post_response.status_code == 200 and "Invalid CSRF token" not in post_response.text:
                            Scan.csrf_set.add(scan_this_url)  # Add the URL to the set if no invalid token message
                            print(f"CSRF vulnerability detected in the URL: {scan_this_url}")
                        else:
                            print(f"NO CSRF vulnerability detected in the URL: {scan_this_url}")
                    else:
                        print(f"CSRF Token is empty in the response for {scan_this_url}")
                else:
                    print(f"CSRF token not found in the response for URL: {scan_this_url}")
            else:
                print(f"CSRF token not found in the response for URL: {scan_this_url}")

        except requests.exceptions.RequestException as e:
            # Handle network issues or timeouts
            print(f"Error while testing CSRF vulnerability for URL {scan_this_url}: {e}")

        return Scan.csrf_set

    @staticmethod
    def is_url_vulnerable_to_ssrf(scan_this_url):
        # SSRF payloads for internal addresses
        payloads = [
            "http://localhost",
            "http://127.0.0.1",
            "http://[::1]",
            "http://169.254.169.254"  # Example: AWS metadata endpoint
        ]

        for payload in payloads:
            try:
                # GET request with the SSRF payload as a parameter
                response = requests.get(scan_this_url, params={"input": payload}, timeout=10)

                # Check for signs of SSRF vulnerability based on error codes or failed connection
                if response.status_code == 500 or "Error connecting" in response.text:
                    # Add to SSRF vulnerable set
                    Scan.ssrf_set.add(scan_this_url)
                    print(f"SSRF vulnerability detected in the URL: {scan_this_url}")
                    break  # No need to check further
                else:
                    print(f"NO SSRF vulnerability detected in the URL: {scan_this_url}")
            except requests.exceptions.RequestException as e:
                # Handle connection errors or timeouts
                print(f"Error while testing SSRF for URL {scan_this_url}: {e}")

        return Scan.ssrf_set

    @staticmethod
    def is_url_vulnerable_to_lfi(scan_this_url):
        # list of common LFI payloads
        payloads = [
            "../../../etc/passwd",  # Unix/Linux
            "../../../../etc/passwd",  # Try different traversal depths
            "../../../windows/system32/drivers/etc/hosts",  # Windows LFI payload
            "../../../../windows/system32/drivers/etc/hosts"  # Alternative depth for Windows
        ]

        for payload in payloads:
            try:
                # GET request with the LFI payload
                response = requests.get(scan_this_url, params={"file": payload}, timeout=10)

                # Check if the response contains evidence of file inclusion (e.g., /etc/passwd content)
                if response.status_code == 200 and "root:" in response.text:
                    # Add the URL to the LFI vulnerable set if the file is included
                    Scan.lfi_set.add(scan_this_url)
                    print(f"LFI vulnerability detected in the URL: {scan_this_url}")
                    break  # No need to check further
                elif response.status_code == 500:
                    # Server error indicating potential LFI attempt
                    print(f"500 error while testing LFI on {scan_this_url}. Possible LFI vulnerability.")
                    Scan.lfi_set.add(scan_this_url)
                    break
                else:
                    print("NO LFI vulnerability detected in the url: " + scan_this_url)
            except requests.exceptions.RequestException as e:
                # Handle network issues or timeouts
                print(f"Error while testing LFI for URL {scan_this_url}: {e}")

        return Scan.lfi_set

    @staticmethod
    def is_url_vulnerable_to_rce(scan_this_url):
        # list of common RCE payloads
        payloads = [
            ";ls",  # Simple list command
            "| ls",  # Pipe approach
            "; cat /etc/passwd",  # Attempt to read system file
            "| cat /etc/passwd",  # Another variant for reading system files
            ";echo vulnerable",  # Check for command output injection
            "| echo vulnerable"  # Check for command output injection
        ]

        for payload in payloads:
            try:
                # GET request with the RCE payload
                response = requests.get(scan_this_url, params={"input": payload}, timeout=10)

                # Check if the response contains evidence of command execution
                if response.status_code == 200 and ("vulnerable" in response.text or "bin" in response.text):
                    # Add to RCE vulnerable set if command output is found
                    Scan.rce_set.add(scan_this_url)
                    print(f"RCE vulnerability detected in the URL: {scan_this_url}")
                    break  # No need to check further
                elif response.status_code == 500:
                    # Server error potentially due to command execution
                    print(f"500 error while testing RCE on {scan_this_url}. Possible RCE vulnerability.")
                    Scan.rce_set.add(scan_this_url)
                    break
                else:
                    print("NO RCE vulnerability detected in the url: " + scan_this_url)
            except requests.exceptions.RequestException as e:
                # Handle network issues or timeouts
                print(f"Error while testing RCE for URL {scan_this_url}: {e}")

        return Scan.rce_set

    # function to generate a random csrf token for testing
    # @staticmethod
    # def generate_csrf_token():
    #     # Generate a random token
    #     token = os.urandom(16)
    #     # Optionally, you can use the session ID or some other value
    #     token = hashlib.sha256(token).hexdigest()
    #     return token