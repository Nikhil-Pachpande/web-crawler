import os


# check if a dir already exists for target website, if it doesn't then create a new dir locally
def create_project_dir(location):
    if not os.path.exists(location):
        print('Creating a new Project ' + location)
        os.makedirs(location)


# create queue and files
def create_files(project_name, base_url):
    queue = project_name + '/queue.txt'
    crawled = project_name + '/crawled.txt'
    sqli = project_name + '/sql_injection_vulnerabilities.txt'
    xss = project_name + '/xss_vulnerabilities.txt'
    csrf = project_name + '/csrf_vulnerabilities.txt'
    ssrf = project_name + '/ssrf_vulnerabilities.txt'
    lfi = project_name + '/lfi_vulnerabilities.txt'
    rce = project_name + '/rce_vulnerabilities.txt'
    if not os.path.isfile(queue):
        create_file(queue, base_url)  # base_url since the crawler needs a reference point
    if not os.path.isfile(crawled):
        create_file(crawled, '')  # make the newly created file as empty
    if not os.path.isfile(sqli):
        create_file(sqli, '')
    if not os.path.isfile(xss):
        create_file(xss, '')
    if not os.path.isfile(csrf):
        create_file(csrf, '')
    if not os.path.isfile(ssrf):
        create_file(ssrf, '')
    if not os.path.isfile(lfi):
        create_file(lfi, '')
    if not os.path.isfile(rce):
        create_file(rce, '')


# create a new file
def create_file(path, data):
    f = open(path, 'w')
    f.write(data)
    f.close()


# append data to an already existing file
def add_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')


# delete the contents of a file
def clear_files(path):
    with open(path, 'w'):
        pass


# using sets to avoid duplicate entries
def convert_file_to_set(file_name):
    result = set()
    with open(file_name, 'rt') as f:
        for line in f:
            result.add(line.replace('\n', ''))
    return result


# iterate through the set, each item will be a new line in the file
def convert_set_to_file(links, file):
    clear_files(file)
    if links:
        for link in sorted(links):
            add_to_file(file, link)
    return file