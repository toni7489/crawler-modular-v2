from urllib.parse import urljoin
from fuciones_red import (is_valid_url, get_status_code, get_title, get_h1, get_meta_description, get_file_type)
import requests
from lxml import html  # Asegúrate de importar html desde lxml

def extract_info_from_url(url, callback, processed_urls, depth, max_depth, request_timeout, excluded_domains):
    if depth > max_depth:
        return
    if any(domain in url for domain in excluded_domains):
        return
    
    try:
        response = requests.get(url, timeout=request_timeout)
        tree = html.fromstring(response.content)

        html_links = tree.xpath('//a/@href')
        image_links = tree.xpath('//img/@src')
        css_links = tree.xpath('//link[@rel="stylesheet"]/@href')
        js_links = tree.xpath('//script[@src]/@src')

        all_links = html_links + image_links + css_links + js_links
        absolute_links = [urljoin(url, link) for link in all_links]
        
        unique_links = list(set(absolute_links))

        for link in unique_links:
            if not is_valid_url(link):
                continue
            if link in processed_urls:
                continue
            
            processed_urls.add(link)

            status_code = get_status_code(link)
            title = get_title(link)
            h1 = get_h1(link)
            meta_description = get_meta_description(link)
            file_type = get_file_type(link)

            result = {
                'Código de Respuesta': status_code,
                'URL': link,
                'Tipo': file_type,
                'Título': title,
                'Etiqueta H1': h1,
                'Meta Descripción': meta_description,
                'Profundidad': depth
            }

            callback(result)

            extract_info_from_url(link, callback, processed_urls, depth + 1, max_depth, request_timeout, excluded_domains)

    except requests.RequestException:
        pass

    callback("FIN")