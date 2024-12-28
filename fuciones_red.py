import requests
from lxml import html
import mimetypes

def is_valid_url(link):
    return link and link.startswith(('http', 'https', 'www'))

def get_file_type(page_url):
    file_type, _ = mimetypes.guess_type(page_url)
    if file_type:
        if 'image' in file_type:
            return 'Imagen'
        elif 'html' in file_type:
            return 'HTML'
        elif 'css' in file_type:
            return 'CSS'
        elif 'javascript' in file_type or 'js' in file_type:
            return 'JavaScript'
    try:
        response = requests.head(page_url, timeout=10)
        content_type = response.headers.get('Content-Type', '')
        if 'image' in content_type:
            return 'Imagen'
        elif 'html' in content_type:
            return 'HTML'
        elif 'css' in content_type:
            return 'CSS'
        elif 'javascript' in content_type or 'js' in content_type:
            return 'JavaScript'
        return 'Desconocido'
    except requests.RequestException:
        return 'Error'

def get_status_code(page_url):
    try:
        response = requests.get(page_url, timeout=10)
        return response.status_code
    except requests.RequestException as e:
        return f'Error: {e}'

def get_title(page_url):
    try:
        response = requests.get(page_url, timeout=10)
        if 'text/html' in response.headers.get('Content-Type', ''):
            page_tree = html.fromstring(response.content)
            title = page_tree.xpath('//title/text()')
            return title[0].strip() if title else 'Sin título'
        return ''
    except requests.RequestException:
        return 'Error al obtener título'

def get_h1(page_url):
    try:
        response = requests.get(page_url, timeout=10)
        if 'text/html' in response.headers.get('Content-Type', ''):
            page_tree = html.fromstring(response.content)
            h1 = page_tree.xpath('//h1/text()')
            return h1[0].strip() if h1 else 'Sin etiqueta H1'
        return ''
    except requests.RequestException:
        return 'Error al obtener H1'

def get_meta_description(page_url):
    try:
        response = requests.get(page_url, timeout=10)
        if 'text/html' in response.headers.get('Content-Type', ''):
            page_tree = html.fromstring(response.content)
            meta_description = page_tree.xpath('//meta[@name="description"]/@content')
            return meta_description[0].strip() if meta_description else 'Sin meta descripción'
        return ''
    except requests.RequestException:
        return 'Error al obtener meta descripción'