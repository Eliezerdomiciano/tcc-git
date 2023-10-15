from playwright.sync_api import sync_playwright
from time import sleep
import json

amazon = "https://www.amazon.com.br/"
googleShopping = "https://shopping.google.com/"
zoom = "https://www.zoom.com.br/"
kabum = "https://www.kabum.com.br/"
buscape = "https://www.buscape.com.br/"
mercadolivre = "https://www.mercadolivre.com.br/"

equipamento = "Poco F5"
equipamento = equipamento.title()

pegar_valor_am = []
pegar_valor_gs = []
pegar_valor_z = []
pegar_valor_ml = []

dados_produtos = {}


def pegandoMenorValor(dados_produtos):
    site_menor_preco = min(
        dados_produtos, key=lambda x: min(dados_produtos[x]["preco"])
    )
    menor_preco = min(dados_produtos[site_menor_preco]["preco"])
    nome_produto = dados_produtos[site_menor_preco]["nome"]
    link_produto = dados_produtos[site_menor_preco]["link"]

    produto_mais_barato = {
        "site": site_menor_preco,
        "nome": nome_produto,
        "preco": menor_preco,
        "link": link_produto,
    }

    objeto_json = json.dumps(produto_mais_barato, indent=2)
    nome_arquivo_json = "resultado.json"

    with open(nome_arquivo_json, "w") as file:
        file.write(objeto_json)
    print(f"Arquivo JSON '{nome_arquivo_json}' Criado com Sucesso!!")

    return nome_arquivo_json


def formatando(preco, site):
    if site == "Amazon":
        pegar_valor_am.append(
            float(preco.text_content()[2:-3].replace(".", "").replace(",", ""))
        )
    elif site == "Google Shopping":
        pegar_valor_gs.append(
            float(
                preco.text_content()[2:7]
                .replace(",", "")
                .replace(".", "")
                .replace("+", "")
                .replace("tax", "")
            )
        )
    elif site == "Zoom":
        pegar_valor_z.append(
            float(preco.text_content()[2:-3].replace(",", "").replace(".", ""))
        )
    elif site == "Mercado Livre":
        pegar_valor_ml.append(float(preco.text_content()[2:].replace(".", "")))
    else:
        print("site não cadastrado")


def rapando_dados(site, produtos):
    index = 0
    verificar = site
    if verificar == "Amazon":
        while True:
            # Separando itens necessarios do produto
            link_prod = produtos.locator(
                f"a.a-link-normal >> nth={index}"
            ).get_attribute("href")
            nome_prod = produtos.locator(f"h2.a-size-mini >> nth={index}")
            nome_prod = nome_prod.text_content()
            if equipamento in nome_prod and index < 20:
                # pegando preco do produto
                preco = produtos.locator("span.a-offscreen").nth(index)
                # formatando valores
                formatando(preco, site)
            else:
                break
            index += 1

            dados_produtos[site] = {
                "nome": nome_prod,
                "preco": pegar_valor_am,
                "link": link_prod,
            }
    elif verificar == "Google Shopping":
        while index < produtos.count():
            nome = produtos.locator("h3.tAxDx", has_text=f"{equipamento}")
            pg_preco = produtos.locator('span[class="a8Pemb OFFNJ"]')
            link = produtos.locator('a[class="shntl sh-np__click-target"]')
            if index < 20:
                nome_prod = nome.nth(index).text_content()
                link_prod = link.nth(index).get_attribute("href")
                preco = pg_preco.nth(index)
                formatando(preco, site)
                index += 1
            else:
                break

            dados_produtos[site] = {
                "nome": nome_prod,
                "preco": pegar_valor_gs,
                "link": link_prod,
            }
    elif verificar == "Zoom":
        while index < produtos.count():
            nome = produtos.locator('h2[data-testid="product-card::name"]')
            pg_preco = produtos.locator('p[data-testid="product-card::price"]')
            link = produtos.locator('a[class="ProductCard_ProductCard_Inner__tsD4M"]')
            if index < 20:
                nome_prod = nome.nth(index).text_content()
                link_prod = link.nth(index).get_attribute("href")
                preco = pg_preco.nth(index)
                formatando(preco, site)
                index += 1
            else:
                break

            dados_produtos[site] = {
                "nome": nome_prod,
                "preco": pegar_valor_z,
                "link": link_prod,
            }
    elif verificar == "Mercado Livre":
        while True:
            # Separando itens necessarios do produto
            nome_prod = produtos.locator("h2.ui-search-item__title").nth(index)
            nome_prod = nome_prod.text_content()
            link = produtos.locator(
                'a[class="ui-search-item__group__element ui-search-link"]'
            )
            link_prod = link.nth(index).get_attribute("href")
            if equipamento in nome_prod and index < 20:
                preco = produtos.locator(
                    'span[class="andes-money-amount ui-search-price__part ui-search-price__part--medium andes-money-amount--cents-superscript"]'
                ).nth(index)
                formatando(preco, site)
            else:
                break
            index += 1

            dados_produtos[site] = {
                "nome": nome_prod,
                "preco": pegar_valor_ml,
                "link": link_prod,
            }
    else:  # finalizando o If
        print(f"{site}==> Site não Cadastrado !!!!!")


def obter_dados_produtos():
    dados = {dados_produtos}
    return dados


# def convertendo_para_json():
#     resultado = produtos_mais_barato
#     objeto_json = json.dumps(resultado, indent=2)
#     nome_arquivo_json = "resultado.json"

#     with open(nome_arquivo_json, "w") as file:
#         file.write(objeto_json)
#     print(f"Arquivo JSON '{nome_arquivo_json}' Criado com Sucesso!!")

#     return nome_arquivo_json


def run(playwright):
    # Inicializando os Sites
    browser = playwright.firefox.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page2 = context.new_page()
    page3 = context.new_page()
    page4 = context.new_page()

    # Abrindo Paginas dos Fornecedores
    page.goto(amazon)
    page2.goto(googleShopping)
    page3.goto(zoom)
    page4.goto(mercadolivre)
    sleep(3)
    # # ======= 1º Pagina Amazon ========
    site = "Amazon"

    page.locator(".nav-input >> nth=0").click()
    page.locator(".nav-input >> nth=0").fill(equipamento)
    page.locator(".nav-input >> nth=1").click()
    # Pegando Base do site
    produtos = page.locator("div.sg-col-20-of-24").locator(
        f'div[class="a-section a-spacing-base"]:has-text("{equipamento}")'
    )

    rapando_dados(site, produtos)
    # produtos_mais_barato = pegandoMenorValor(dados_produtos)
    # print(produtos_mais_barato)
    sleep(3)

    # ---------------------

    # ======= 2º Pagina Google Shopping ========
    site = "Google Shopping"
    page2.locator("#REsRA").click()
    page2.locator("#REsRA").fill(equipamento)
    page2.locator('div[class="kzJn9c jzWc1"]').click()

    produtos = page2.locator("div#rso")

    rapando_dados(site, produtos)
    # produtos_mais_barato = pegandoMenorValor(dados_produtos)
    # print(produtos_mais_barato)
    sleep(3)
    # ---------------------

    # ======= 3º Pagina Zoom ========
    site = "Zoom"

    page3.locator('input[type="search"]').click()
    page3.locator('input[type="search"]').fill(equipamento)
    page3.locator('button[class="AutoCompleteStyle_submitButton__GkxPO"]').click()

    produtos = page3.locator("div.Paper_Paper__HIHv0", has_text=f"{equipamento}")
    rapando_dados(site, produtos)
    # produtos_mais_barato = pegandoMenorValor(dados_produtos)
    # print(produtos_mais_barato)
    sleep(3)

    # ---------------------

    # ======= 4º Pagina Mercado Livre ========
    site = "Mercado Livre"

    page4.locator("#cb1-edit").click()
    page4.locator("#cb1-edit").fill(equipamento)
    page4.locator(".nav-search-btn").click()

    # Pegando a Tag Base.
    produtos = page4.locator("ol.ui-search-layout li.ui-search-layout__item").filter(
        has_text=equipamento
    )
    rapando_dados(site, produtos)

    sleep(3)

    # ---------------------

    produtos_mais_barato = pegandoMenorValor(dados_produtos)
    print(produtos_mais_barato)

    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
