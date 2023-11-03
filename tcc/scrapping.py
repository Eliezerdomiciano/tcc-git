from playwright.sync_api import sync_playwright
from time import sleep
import json
import re

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
    menor_preco = float("inf")
    site_menor_preco = ""

    for site, info in dados_produtos.items():
        preco = info["preco"]
        menor_site_preco = min(preco)
        if menor_site_preco < menor_preco:
            menor_preco = menor_site_preco
            site_menor_preco = site

    produto_mais_barato = {
        "site_menor_preco": {
            "fornecedor": site_menor_preco,  # Adiciona o nome do site
            "nome": dados_produtos[site_menor_preco]["nome"],
            "preco": menor_preco,
            "link": dados_produtos[site_menor_preco]["link"],
        }
    }

    nome_arquivo_json = "resultado.json"
    with open(nome_arquivo_json, "w") as arquivo:
        json.dump(produto_mais_barato, arquivo)
    print(f"Arquivo JSON '{nome_arquivo_json}' Criado com Sucesso!!")

    return produto_mais_barato


# def pegandoMenorValor(dados_produtos):
#     menor_preco = float("inf")
#     site_menor_preco = ""

#     for site, info in dados_produtos.items():
#         preco = info["preco"]
#         if preco:  # Verifique se a lista de preços não está vazia
#             menor_site_preco = min(preco)
#             if menor_site_preco < menor_preco:
#                 menor_preco = menor_site_preco
#                 site_menor_preco = site
#         else:
#             print(f"Nenhum preço válido encontrado para o site {site}.")

#     if site_menor_preco:
#         produto_mais_barato = {
#             "site_menor_preco": {
#                 "fornecedor": site_menor_preco,
#                 "nome": dados_produtos[site_menor_preco]["nome"],
#                 "preco": menor_preco,
#                 "link": dados_produtos[site_menor_preco]["link"],
#             }
#         }

#         nome_arquivo_json = "resultado.json"
#         with open(nome_arquivo_json, "w") as arquivo:
#             json.dump(produto_mais_barato, arquivo)
#         print(f"Arquivo JSON '{nome_arquivo_json}' Criado com Sucesso!!")

#         return produto_mais_barato
#     else:
#         print(
#             "Nenhum preço válido encontrado. Não foi possível determinar o produto mais barato."
#         )


# def format_price(price_text):
#     try:
#         # Remova o "R$" e substitua "," por "."
#         price_text = price_text.replace("R$", "").replace(",", ".")
#         # Converta para float
#         return float(price_text)
#     except ValueError:
#         return None  # Retorne None se não for possível converter


# def formatando(preco, site):
#     preco_text = preco.text_content()
#     preco_formatado = format_price(preco_text)

#     if preco_formatado is not None:
#         if site == "Amazon":
#             pegar_valor_am.append(preco_formatado)
#         elif site == "Google Shopping":
#             pegar_valor_gs.append(preco_formatado)
#         elif site == "Zoom":
#             pegar_valor_z.append(preco_formatado)
#         elif site == "Mercado Livre":
#             pegar_valor_ml.append(preco_formatado)
#     else:
#         print(
#             f"Não foi possível encontrar um valor numérico válido em '{preco_text}' para o site {site}."
#         )


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
                print(preco.text_content())
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
                print(preco.text_content())
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
                print(preco.text_content())
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
                print(preco.text_content())
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

    # ---------------------

    produtos_mais_barato = pegandoMenorValor(dados_produtos)
    print(produtos_mais_barato)

    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
