# web-crawler
A spider that crawls through the target websites and stores the links from them to their respective report folders in a text file.

* Queue Set - to store all the links collected
* Crawled Set - to move the links from queue to this set, to avoid crawling in again
 
Multithreading implementation 
- to improve responsiveness and scalability (helps if there are large no. of underlying pages or links)
- for better resource sharing (the spiders will share the same resources i.e. the queue set and the crawled set
- to reduce the space consumption and utilization of system resources, improves concurrency
