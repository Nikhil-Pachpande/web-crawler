from urllib.parse import urlparse



# get the domain name (sample.com)
def get_domain_name(url):
    try:
        results = get_sub_domain_name(url).split('.')
        return results[-2] + '.' + results[-1]
    except:
        return ''


# get the sub domain name (xyz.sample.com)
def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc
    except:
        return ''
