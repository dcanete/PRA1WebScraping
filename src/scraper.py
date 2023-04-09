from bs4 import BeautifulSoup
import requests
import sys
import time
import csv
import logging
logging.basicConfig(filename='scraper.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
#logging.basicConfig(stream=sys.stdout, encoding='utf-8', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

###########################
# Constantes
###########################
base = "https://www.ferreteriasindustriales.es/"
# Número máximo de páginas por categoría (para no saturar la página origen)
max_pages = 10
# Número máximo de productos que se mira el detalle (para no saturar la página origen)
max_products = 50000
# Nombre del fichero de datos
filename = "data.csv"
# Categorías de productos (tienen páginas distintas)
categorias = ["14-para-el-hogar", "22-jardin-y-piscinas", "16-ferreteria", "19-fontaneria", 
              "20-material-electrico", "25-maquinaria", "15-cerrajeria", "17-climatizacion", 
              "176-cantoneras"]
# Segundos de retraso que se pone entre llamada y llamada a pagina de detalle (para no saturar la página origen)
delay = 0.25
products_links = []



##################################################################
# Método que almacena en un diccionario los datos de un producto
##################################################################
def getProduct(str):
    page = requests.get(str)
    soup = BeautifulSoup(page.content, features="lxml")
    productData={}
    
    productData['url'] = str
    productData['title'] = soup.title.string
        
    # Precio
    productData['price'] = soup.find("span", {"itemprop": "price"}).get_text()

    # Referencia
    # Hay algunos casos donde no viene el fabricante
    try: 
        productData['fabricante'] = soup.find("div", {"class": "product-reference"}).find ("a").get_text()
    except Exception:
        productData['fabricante'] = ""
    
    productData['sku'] = soup.find("span", {"itemprop": "sku"}).get_text() 

    # Categorización
    productData["Categoria"] = soup.find_all("li", {"itemprop": "itemListElement"})[1].find("span").get_text()
    productData["Subcategoria"] = soup.find_all("li", {"itemprop": "itemListElement"})[2].find("span").get_text()

    # Ficha técnica. Hay que recorrer el HTML para encontrar todas las propiedades de la ficha técnica
    productData["Articulo"] = ""
    productData["Marca Comercial"] = ""
    productData["Presentacion"] = ""
    productData["Referencia Proveedor"] = ""
    productData["Diametro"] = ""
    props = soup.find("dl", {"class": "data-sheet"}).contents
    tam=int((len(props)-1)/4)
    for i in range(0,tam):
        productData[props[i*4+1].string] = props[i*4+3].string
    
    
    # Devuelve el diccionario relleno
    return productData


###########################################
# Inicio del proceso
###########################################

# TODO: Sacar código a main.py como se hace en el ejemplo 
#   complejo: https://github.com/tteguayco/Web-scraping


logging.info('-----Inicio del proceso-----')

#print (getProduct("https://www.ferreteriasindustriales.es/articulos-de-navidad/72135-arbol-de-navidad-con-nieve-con-base-en-paraguas-verde-75-cm-8719883661919.html"))

# Bucle de categorias
for cat in categorias:
    logging.info('--Buscando productos en ' + cat + '...')
   
    # Bucle de páginas. Se para cuando se alcance el máximo o no se encuentren más productos
    for i in range(1,max_pages+1):
        url = base + cat +  "?page=" + str(i)
       
        page = requests.get(url)
        soup = BeautifulSoup(page.content, features="lxml")
        tam = len (soup.find_all('h5', {"class": "product-title"}))
        logging.debug ("----" + str(tam) + " productos encontrados")

        if (tam)==0:
            logging.info('----No se encuentran más productos. Páginas revisadas: ' + str(i))
            break
        
        for link in soup.find_all('h5', {"class": "product-title"}):
              aLink = link.find("a",href=True).get('href')
              products_links.append(aLink)

        # Para no saturar la web origen
        time.sleep (delay) 

# Quita enlaces duplicados    
products_links = list(dict.fromkeys(products_links))

# Reduce la lista para no saturar web origen
products_links = products_links[0:max_products] 

# Inicializa la lista de productos
item=["url","title","price","fabricante","sku","Articulo", "Marca Comercial", "Presentacion" , "Referencia Proveedor", "Diametro", "Categoria", "Subcategoria"]
products = []
products.append(item)


# Recorremos todos los productos viendo el detalle
i=1
size = len (products_links)
logging.info("-----Procesando " + str(size) + " productos-----")
for url in products_links: 
    productData = getProduct(url)
    logging.debug ("--Procesado " + productData["title"] + "(" + str(i) + "/" + str(size) + ")")
    i=i+1
    item = [productData ["url"],productData ["title"], productData ["price"], 
            productData ["fabricante"], productData ["sku"], productData ["Articulo"], 
            productData ["Marca Comercial"], productData ["Presentacion"] , 
            productData ["Referencia Proveedor"], productData ["Diametro"], 
            productData ["Categoria"], productData ["Subcategoria"]]
    products.append(item)
   
    # Para no saturar el servidor origen
    time.sleep (delay) 

# Por último, almacenamos el contenido de la lista en CSV
logging.info('-----Almacenamiento-----')
with open(filename, 'w', newline='') as csvFile:
    writer = csv.writer(csvFile)
    for product in products:
        writer.writerow(product)

logging.info('-----Fin del proceso-----\n\n')
