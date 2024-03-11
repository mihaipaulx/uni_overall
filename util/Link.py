class Link:
  def __init__(self):
    self.protocol = "https://"
    self.domain = "search.yahoo.com"
    self.search_path = "/search;_ylt=A0oG7l7PeB5P3G0AKASl87UF"
    self.query_key = "p"
  def build(self, query):
    search_url = f"{self.protocol}{self.domain}{self.search_path}?{self.query_key}="
    for keyword in query.split():
      search_url += f"{keyword}+"
    return search_url