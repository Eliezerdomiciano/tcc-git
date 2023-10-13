from playwright.sync_api import sync_playwright, expect
from bs4 import BeautifulSoup
from time import sleep
import numpy as np
import pandas as pd
import re
import requests

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
    menorValor = float("inf")
    produto_mais_barato = {}

    for site, dados in dados_produtos.items():
        precos = dados["preco"]
        links = dados["link"]
        nomes = dados["nome"]

        menorValor = min(precos)
        produto_mais_barato = {
            "site": site,
            "preco": menorValor,
            "link": links,
            "nome": nomes,
        }
    return produto_mais_barato


def formatando(preco, site):
    if site == "Amazon":
        pegar_valor_am.append(
            int(preco.text_content()[2:-3].replace(".", "").replace(",", ""))
        )
    elif site == "Google Shopping":
        pegar_valor_gs.append(
            int(
                preco.text_content()[2:7]
                .replace(",", "")
                .replace(".", "")
                .replace("+", "")
                .replace("tax", "")
            )
        )

    elif site == "Zoom":
        pegar_valor_z.append(
            int(preco.text_content()[2:-3].replace(",", "").replace(".", ""))
        )

    elif site == "Mercado Livre":
        pegar_valor_ml.append(int(preco.text_content()[:4]))
    else:
        print("site não cadastrado")


def run(playwright):
    #   Inicializando os Sites
    browser = playwright.firefox.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    # page2 = context.new_page()
    # page3 = context.new_page()
    # page4 = context.new_page()

    #   Abrindo Paginas dos Fornecedores
    page.goto(amazon)
    # page2.goto(googleShopping)
    # page3.goto(zoom)
    # page4.goto(mercadolivre)
    sleep(3)
    # # ======= 1º Pagina Amazon ========
    site = "Amazon"

    page.locator("#twotabsearchtextbox").click()
    page.locator("#twotabsearchtextbox").fill(equipamento)
    page.locator("#nav-search-submit-button").click()
    # Pegando Base do site
    produtos = page.locator("div.sg-col-20-of-24").locator(
        f'div[class="a-section a-spacing-base"]:has-text("{equipamento}")'
    )

    index = 0

    print("\n", site)
    while True:
        # Separando itens necessarios do produto
        link_prod = produtos.locator(f"a.a-link-normal >> nth={index}").get_attribute(
            "href"
        )
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
        "nome": [nome_prod],
        "preco": [pegar_valor_am],
        "link": [link_prod],
    }

    produtos_mais_barato = pegandoMenorValor(dados_produtos)
    print(produtos_mais_barato)
    sleep(3)

    # ---------------------

    # ======= 2º Pagina Google Shopping ========
    # site = "Google Shopping"
    # page2.locator("#REsRA").click()
    # page2.locator("#REsRA").fill(equipamento)
    # page2.locator('div[class="kzJn9c jzWc1"]').click()

    # sleep(3)
    # produtos = page2.locator("div#rso")
    # nome = produtos.locator("h3.tAxDx", has_text=f"{equipamento}")
    # pg_preco = produtos.locator('span[class="a8Pemb OFFNJ"]')
    # index = 0

    # print(site)
    # while index < nome.count():
    #     if index < 20:
    #         nome_prod = nome.nth(index).text_content()
    #         preco = pg_preco.nth(index)
    #         formatando(preco, site)
    #         index += 1
    #     else:
    #         break

    # dados_produtos[site] = {
    #     "nome": [nome_prod],
    #     "preco": [pegar_valor_am],
    #     "link": [link_prod],
    # }

    # produtos_mais_barato = pegandoMenorValor(dados_produtos)
    # print(produtos_mais_barato)

    # ---------------------

    # ======= 3º Pagina Zoom ========
    # site = "Zoom"

    # page3.locator('input[type="search"]').click()
    # page3.locator('input[type="search"]').fill(equipamento)
    # page3.locator('button[class="AutoCompleteStyle_submitButton__GkxPO"]').click()

    # produtos = page3.locator("div.Paper_Paper__HIHv0", has_text=f"{equipamento}")
    # nome = produtos.locator('h2[data-testid="product-card::name"]')
    # pg_preco = produtos.locator('p[data-testid="product-card::price"]')
    # index = 0

    # print("\n", site)
    # while index < produtos.count():
    #     if index < 20:
    #         nome_prod = nome.nth(index).text_content()
    #         preco = pg_preco.nth(index)
    #         formatando(preco, site)
    #         index += 1
    #     else:
    #         break

    # dados_produtos[site] = {
    #     "nome": [nome_prod],
    #     "preco": [pegar_valor_am],
    #     "link": [link_prod],
    # }

    # produtos_mais_barato = pegandoMenorValor(dados_produtos)
    # print(produtos_mais_barato)
    # sleep(3)

    # ---------------------

    # ======= 4º Pagina Mercado Livre ========
    # site = "Mercado Livre"

    # page4.locator("#cb1-edit").click()
    # page4.locator("#cb1-edit").fill(equipamento)
    # page4.locator(".nav-search-btn").click()

    # # Pegando a Tag Base.
    # produtos = page4.locator("ol.ui-search-layout li.ui-search-layout__item").filter(
    #     has_text=equipamento
    # )
    # index = 0

    # print("\n", site)
    # while True:
    #     # Separando itens necessarios do produto
    #     nome_prod = produtos.locator("h2.ui-search-item__title").nth(index)
    #     nome_prod = nome_prod.text_content()
    #     if equipamento in nome_prod and index < 20:
    #         preco = produtos.locator(
    #             'span[class="andes-money-amount ui-search-price__part ui-search-price__part--medium andes-money-amount--cents-superscript"]'
    #         ).nth(index)
    #         formatando(preco, site)
    #     else:
    #         break
    #     index += 1

    # dados_produtos[site] = {
    #     "nome": [nome_prod],
    #     "preco": [pegar_valor_am],
    #     "link": [link_prod],
    # }

    # produtos_mais_barato = pegandoMenorValor(dados_produtos)
    # print(produtos_mais_barato)
    # sleep(3)

    # ---------------------

    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
