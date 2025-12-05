import re
from bs4 import BeautifulSoup

def parse_page_html(html):
    soup = BeautifulSoup(html, "html.parser")
    
    item_names = []
    total = 0.0
    
    price_re = re.compile(r"([\d\s]+)\s*₽")
    

    product_cards = soup.select(".catalog-item, .product-item, .item, [class*='product'], [class*='item']")
    
    for card in product_cards:
        name_element = card.select_one(".title, .name, h3, h4, a.title, [class*='title'], [class*='name']")
        
        if name_element:
            name = name_element.get_text(strip=True)
            name = re.sub(r'\s+', ' ', name).strip()
            
            if name and len(name) > 2:  
                item_names.append(name)
                
                price_element = card.select_one(".price, .cost, [class*='price'], [class*='cost']")
                if price_element:
                    price_text = price_element.get_text()
                    m = price_re.search(price_text)
                    if m:
                        try:
                            price = float(m.group(1).replace(" ", ""))
                            total += price
                        except:
                            pass
    
    if not item_names:
        all_elements = soup.find_all(['h3', 'h4', 'a', 'div', 'span'])
        for elem in all_elements:
            text = elem.get_text(strip=True)
            if len(text) > 10 and len(text) < 200: 
                parent = elem.parent
                if parent:
                    parent_text = parent.get_text()
                    if '₽' in parent_text or 'руб' in parent_text.lower():
                        item_names.append(text)
    
    unique_names = []
    for name in item_names:
        if name not in unique_names:
            unique_names.append(name)
    
    return unique_names, total