# Web Crawler with Vulnerability Detection
A spider that crawls through the target websites and stores the links from them to their respective report folders in a text file.

* Queue Set - to store all the links collected
* Crawled Set - to move the links from queue to this set, to avoid crawling in again
 
# Multithreading implementation 
- to improve responsiveness and scalability (helps if there are large no. of underlying pages or links)
- for better resource sharing (the spiders will share the same resources i.e. the queue set and the crawled set
- to reduce the space consumption and utilization of system resources, improves concurrency

# Vulnerability Detection
* Implemented vulnerability detection for the target and crawled websites to detect security vulnerabilities(if any) and prevent websites from:
- Cross-site scripting (XSS) attacks
- SQL Injection (SQLI) attacks
- Cross-site request forgery (CSRF) attacks
- Server-side request forgery (SSRF) attacks
- Local File Inclusion (LFI) attacks
- Remote Code Execution (RCE) attacks

# Usage
pip install -r requirements.txt

* Replace the Project name and Target Url in main.py (ln 8, 9) as per your need (UI implementation in progress)
- PROJECT_NAME = 'Your Project Name'
- HOMEPAGE = 'Your Target URL'

* Increase the number of threads as per the capacity of your system - main.py (ln 13)

# Future Scope
- Implement User Interface for the application
- Implement detection for other common attacks
- Implement ThreadPooling, Async and Concurrency for the vulnerability scanner