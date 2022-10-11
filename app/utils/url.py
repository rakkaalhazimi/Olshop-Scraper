from urllib.parse import urlparse, parse_qsl, urlencode

def get_url_query(url: str, key: str):
    parsed_url = urlparse(url)
    query_dict = dict(parse_qsl(parsed_url.query))
    return query_dict.get(key)

def set_url_query(url: str, key: str, value: str):
    parsed_url = urlparse(url)
    query_dict = dict(parse_qsl(parsed_url.query))
    query_dict[key] = value
    new_query = urlencode(query_dict, doseq=True)
    new_url = parsed_url._replace(query=new_query).geturl()
    return new_url