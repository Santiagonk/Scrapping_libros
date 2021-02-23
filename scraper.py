# import libraries 
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from urllib import robotparser
from urllib.request import urlopen,urljoin
import requests
from urllib.parse import urlparse
import requests
import lxml.html as html

#Constants 
HOME_URL = 'https://www.buscalibre.com.co/'

XPATH_LINK_TO_ARTICLE = '//div[@class="productos pais46"]//a/@href' #constant links
XPATH_AUTHOR = '//p[@class = "precioAhora margin-0 font-weight-strong"]/span/text()' # constant de autor
XPATH_EDITORIAL = '//div[@id = "metadata-editorial"]/a/text()' #constant editorial
XPATH_CATEGORY = '//div[@id = "metadata-categoría"]/text()' # constant category
XPATH_NAME = '//div[@class = "info-libro"]//h1/text()' # constant name
XPATH_OPINIONS = '//div[@class = "info-libro"]//a[@id ="valoracion"]/text()' # constant opinions
XPATH_PRICE = '//div[@id = "metadata-editorial"]/a/text()'

def parse_home():
    try:
        print("Parseando pagina principal")
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            print("Se obtuvo status code correcto")
            home = response.content.decode('utf-8')  # decode para traer las Ñ
            parsed = html.fromstring(home)
            links_to_books = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            #print(links_to_notice)

            today = datetime.date.today().strftime('%d-%m-%Y') #guardar en texto la fecha de hoy
            print("Se obtienen los links de: ",today)
            if not os.path.isdir(today):
                os.mkdir(today)
                print("Se crea carpeta: ",today)
            else:
                print("Carpeta ya esta creada")
            print("Se inicia parseo de las noticias")
            for link in links_to_books:
                if link[:5] == 'https':
                    parsed_notice(link, today)
            print(f'finalizado el parseo de las noticias, se realizo sobre {len(links_to_notice)} noticias')
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parsed_notice(link, date):
    try:
        #print(f'Se inicia parseo del link {link}')
        response = requests.get(link)
        if response.status_code == 200:
            #print("Se obtuvo status code correcto")
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            
            try:
                libro = ''
                libro = parsed.xpath(XPATH_NAME)[0]                
                print(f'{link} el titulo es {libro}')
                autor = parsed.xpath(XPATH_AUTHOR)[0]
                print('autor correcto')
                precio = parsed.xpath(XPATH_PRICE)
                print('Precio correcto')
                editorial = parsed.xpath(XPATH_EDITORIAL)
                print('Editorial correcto')
                category = parsed.xpath(XPATH_CATEGORY)
                print('Categoria correcto')
                opinions = parsed.xpath(XPATH_OPINIONS)
                print(title," parseado correctamente")
            except IndexError:
                return

            with open(f'{date}/{title}.txt','w',encoding='utf-8') as f:
                
                f.write(libro)
                f.write('\n\n')
                f.write(autor)
                f.write('\n\n')
                f.write(precio)
                f.write('\n\n')
                f.write(editorial)
                f.write('\n\n')
                f.write(category)
                f.write('\n\n')
                f.write(opinions)
                f.write('\n\n')              
                

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def main():
    pass

if __name__ == "__main__":
    pass
