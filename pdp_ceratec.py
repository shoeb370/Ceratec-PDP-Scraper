import requests
import constants
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
# https://www.upwork.com/jobs/Product-Color-Image-Scraper_~022011651331797801006/?referrer_url_path=find_work_home

def get_response():
    headers = constants.pdp_headers
    for _ in range(5):
        response = requests.get('https://www.ceratec.com/fr/RSS-2048-Alchemy-2', 
                            headers=headers)
        print(f"Response Status Code: {response.status_code} --{response.url}")
        if response.status_code == 200:
            return response

def get_product_title(soup):
    product_title = '-'
    try:
        product_title = soup.find('div',{'class':'product-name'}).text.strip()
    except Exception as e:
        line_no = e.__traceback__.tb_lineno
        print(f"Error extracting product title at line {line_no}: {e}")
    return product_title
def get_breadcrumbs(soup):
    breadcrumbs = []
    try:
        breadcrumb_tags = soup.find('div', {'class': 'breadcrumb breadcrumbDesktop'})
        li_tag = breadcrumb_tags.find_all('li')
        breadcrumb_list = [i.find('a')['title'] for i in li_tag]
        breadcrumbs = ' > '.join(breadcrumb_list)
    except Exception as e:
        line_no = e.__traceback__.tb_lineno
        print(f"Error extracting breadcrumbs at line {line_no}: {e}")
    return breadcrumbs
def get_description(soup):
    description = '-'
    try:
        desc_tag = soup.find('div',{'class':'short-description'})
        description = desc_tag.text.strip()
    except Exception as e:
        line_no = e.__traceback__.tb_lineno
        print(f"Error extracting description at line {line_no}: {e}")
    return description

def get_image_urls(soup):
    image_urls = []
    try:
        img_tags = soup.find('div', {'id': 'picture-thumbs-carousel'}).find_all('img')
        image_urls = '|'.join([img['data-defaultsize'] for img in img_tags if 'data-defaultsize' in img.attrs])
    except Exception as e:
        line_no = e.__traceback__.tb_lineno
        print(f"Error extracting image URLs at line {line_no}: {e}")
    return image_urls
def get_color_grouping(soup):
    color_grouping = '-'
    try:
        color_section = soup.find('div', {'class': 'product-colors'})
        if color_section:
            color_options = color_section.find_all('span', {'class': 'color-option'})
            colors = [option['title'] for option in color_options if 'title' in option.attrs]
            color_grouping = '|'.join(colors)
    except Exception as e:
        line_no = e.__traceback__.tb_lineno
        print(f"Error extracting color grouping at line {line_no}: {e}")
    return color_grouping

def get_color_grouping_by_tag(soup):
    colors = []
    try:
        tag_section = soup.find('div',{'class':'availability-attributes-wrapper'})
        dt_tags = tag_section.find_all('dt')
        for i in dt_tags:
            if 'Couleur'.lower() in i.text.lower():
                dd_tags = i.find_next_sibling('dd')
                for j in dd_tags.find_all('span', {'class':'attribute-square'}):
                    colors.append(j['title'])
    except Exception as e:
        print(f"Error extracting colors by tag: {e}")
    return '|'.join(colors) if colors else '-'

def get_size_grouping(soup):
    sizes = []
    try:
        tag_section = soup.find('div',{'class':'availability-attributes-wrapper'})
        dt_tags = tag_section.find_all('dt')
        for i in dt_tags:
            if 'DIMENSION'.lower() in i.text.lower():
                dd_tags = i.find_next_sibling('dd')
                for j in dd_tags.find_all('span', {'class':'attribute-square'}):
                    sizes.append(j['title'])
    except Exception as e:
        print(f"Error extracting sizes by tag: {e}")
    return '|'.join(sizes) if sizes else '-'

def get_material(soup):
    material = '-'
    try:
        tag_section = soup.find('div',{'class':'availability-attributes-wrapper'})
        dt_tags = tag_section.find_all('dt')
        for i in dt_tags:
            if 'FINI DE LA SURFACE'.lower() in i.text.lower():
                dd_tags = i.find_next_sibling('dd')
                label = dd_tags.find('label')
                if label:
                    material = label.get('title', '-')
    except Exception as e:
        print(f"Error extracting material by tag: {e}")
    return material

def get_technical_document(soup):
    technical_document = '-'
    try:
        doc_section = soup.find('div', {'id': 'Documents'})
        if doc_section:
            docs_class = doc_section.find_all('div',{'class': 'documentation-entry'})
            docs = [a.find('a')['href'] for a in docs_class]
            technical_document = '|'.join(docs)
    except Exception as e:
        line_no = e.__traceback__.tb_lineno
        print(f"Error extracting technical document at line {line_no}: {e}")
    return technical_document

def parse_product_page(response):
    soup = BeautifulSoup(response.content, 'html.parser')
    product_data = {}
    product_data['url'] = 'https://www.ceratec.com/fr/RSS-2048-Alchemy-2'
    product_data['brand'] = 'Ceratec'
    product_data['currency'] = 'EUR'
    product_data['price'] = '-'
    product_data['website'] = 'Ceratec'
    # Extract product name
    product_name = get_product_title(soup)
    product_data['title'] = product_name
    product_data['breadcrumbs'] = get_breadcrumbs(soup)
    product_data['description'] = get_description(soup)
    product_data['image_urls'] = get_image_urls(soup)
    product_data['color_of_variants'] = '-'
    product_data['size_of_variants'] = '-'
    product_data['color_grouping'] = get_color_grouping_by_tag(soup)
    if product_data['color_grouping'] != '-':
        product_data['color_of_variants'] = product_data['color_grouping'].split('|')[0]
    product_data['size_grouping'] = get_size_grouping(soup)
    product_data['material'] = get_material(soup)
    product_data['technical_document'] = get_technical_document(soup)
    return product_data

if __name__ == "__main__":
    response = get_response()
    if response:
        product_info = parse_product_page(response)
        
        # Store returned info in Excel/CSV using pandas
        df = pd.DataFrame([product_info])
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        excel_file = f"product_data_{timestamp}.xlsx"
        csv_file = f"product_data_{timestamp}.csv"
        
        df.to_excel(excel_file, index=False)
        df.to_csv(csv_file, index=False)
        
        print(f"✓ Data saved to {excel_file}")
        print(f"✓ Data saved to {csv_file}")
        print("\nProduct Info:")
        print(product_info)
    else:
        print("Failed to retrieve the product page.")