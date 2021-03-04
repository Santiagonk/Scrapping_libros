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
import os
import datetime
import csv

#Constants 
HOME_URL = 'https://www.buscalibre.com.co/'

XPATH_LINK_TO_ARTICLE = '//div[@class="productos pais46"]//a/@href' #constant links
XPATH_AUTHOR = '//div[@id = "metadata-autor"]/a/text()' # constant de autor
XPATH_EDITORIAL = '//div[@id = "metadata-editorial"]/a/text()' #constant editorial
XPATH_CATEGORY = '//div[@id = "metadata-categoría"]/text()' # constant category
XPATH_NAME = '//div[@class = "info-libro"]//h1/text()' # constant name
XPATH_OPINIONS = '//div[@class = "info-libro"]//a[@id ="valoracion"]/text()' # constant opinions
XPATH_PRICE = '//p[@class = "precioAhora margin-0 font-weight-strong"]/span/text()'

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
            dato = 'libro, autor, precio, editorial, category, opinions'
            with open(f'{today}.csv','w') as csv_file:
                csv_file.write(dato) 

            # if not os.path.isdir(today):
            #     os.mkdir(today)
                
            #     f.close()
            #     print("Se crea carpeta: ",today)
            # else:
            #     print("Carpeta ya esta creada")
            print("Se inicia parseo de las noticias")
            books = []
            for link in links_to_books:
                if link[:5] == 'https':
                    books.append(parsed_book(link, today))
            print(f'finalizado el parseo de las noticias, se realizo sobre {len(links_to_books)} noticias')
            # with open(f'{today}.csv','w') as csv_file:
            #     writer = csv.writer(csv_file, delimiter = ',')
            #     writer.writerow(dato)  
            #     for book in books:
            #         writer.writerow(book) 
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parsed_book(link, date):
    try:
        #print(f'Se inicia parseo del link {link}')
        response = requests.get(link)
        if response.status_code == 200:
            #print("Se obtuvo status code correcto")
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            
            try:
                
                if parsed.xpath(XPATH_NAME) != []:
                    libro = parsed.xpath(XPATH_NAME)[0]
                    libro = libro.replace(',',' ')                
                    print(f'{link} el titulo es {libro}')
                else:
                    libro = '-1'
                if parsed.xpath(XPATH_AUTHOR) != []:
                    autor = parsed.xpath(XPATH_AUTHOR)[0]
                    autor = autor.replace(',',' ')
                    print('autor correcto')
                else:
                    autor = '-1'
                if parsed.xpath(XPATH_PRICE) != []:
                    precio = parsed.xpath(XPATH_PRICE)[0]
                    precio = str(precio)
                    print('Precio correcto')
                else:
                    precio = '-1'
                if parsed.xpath(XPATH_EDITORIAL) != []:
                    editorial = parsed.xpath(XPATH_EDITORIAL)[0]
                    editorial = editorial.replace(',',' ')
                    print('Editorial correcto')
                else:
                    editorial = '-1' 
                if parsed.xpath(XPATH_CATEGORY) !=[]:
                    category = parsed.xpath(XPATH_CATEGORY)[0]
                    category = category.strip()
                    print('Categoria correcto')
                else:
                    category = '-1'                
                if parsed.xpath(XPATH_OPINIONS) != []:
                    opinions = parsed.xpath(XPATH_OPINIONS)[0]                    
                    opinions = opinions.strip()
                else:
                    opinions = '-1'
                print(libro," parseado correctamente")
            except IndexError:
                return

            dato = "\n" + libro + ',' + autor + ',' + precio + ',' + editorial + ',' + category + ',' + opinions
            print(dato)
            with open(f'{date}.csv','a') as csv_file:    
                
                csv_file.write(dato)                     
            

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def main():
    parse_home()

if __name__ == "__main__":
    main()
