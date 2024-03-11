from urllib.parse import urlparse

def get_domain(url):
  parsed_url = urlparse(url)
  domain = parsed_url.netloc
  
  if isinstance(domain, bytes):
    domain = domain.decode("utf-8")

  domain = domain.replace("www.", "")

  return domain