import csv
from bs4 import BeautifulSoup
from msedge.selenium_tools import Edge, EdgeOptions


def get_url(palavra_busca):
    """Gera url a partir da palavra_busca"""

    template = 'https://www.amazon.com/s?k={}'
    palavra_busca = palavra_busca.replace(' ','+')
    url = template.format(palavra_busca)

    return url

def extrair_informacao(item):

    #descricao
    atag = item.h2.a
    descricao = atag.text.strip()

    #preco - necessario try/except porque pode aparecer produtos indisponiveis e o valor não é mostrado
    try:
        preco_principal = item.find('span','a-price')
        preco = 'R' + preco_principal.find('span','a-offscreen').text
    except AttributeError:
        return

    resultado = (descricao,preco)

    return resultado

def main(palavra_busca):

    #Iniciar navegador
    options = EdgeOptions()
    options.use_chromium = True
    driver = Edge(options=options)

    lista_produtos = []

    #monta url e coloca no navegador
    url = get_url(palavra_busca)
    driver.get(url)

    #carrega a pagina e seus resultados
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    resultados = soup.find_all('div', {'data-component-type': 's-search-result'})

    #coloca as informacoes na lista
    for item in resultados:
        lista = extrair_informacao(item)
        if lista:
            lista_produtos.append(lista)
    driver.quit()

    #salvar informação e criar arquivo .CSV
    with open('resultado.csv','w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Descrição', 'Preço'])
        writer.writerows(lista_produtos)

main('Iphone')
