from playwright.sync_api import sync_playwright
import os

# Pasta de destino
pasta_download = os.path.abspath("downloads")
os.makedirs(pasta_download, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(accept_downloads=True)
    page = context.new_page()

    # 1. LOGIN
    print("Acessando Conta Azul")
    page.goto("https://app.contaazul.com")
    page.wait_for_timeout(5000)

    print("Fazendo login...")
    campos = page.query_selector_all("input")
    campos[0].fill("SEU EMAIL ") #login COLOCAR O EMAIL DE LOGIN CONTA AZUL
    campos[1].fill("SUA SENHA")  #senha

    page.click('button:has-text("Entrar")')
    page.wait_for_timeout(8000)
    print("✅ Login realizado")

    # 2. DRE GERENCIAL 2025
    print("Acessando DRE Gerencial...")
    page.goto("https://app.contaazul.com/#/ca/relatorios/dre?year=2025") #link dre
    page.wait_for_timeout(6000)

    print("Exportando DRE...")
    try:
        with page.expect_download() as dre_download:
            page.click('button:has-text("Exportar")')
        dre_file = dre_download.value
        dre_path = os.path.join(pasta_download, "dre_2025.csv")
        dre_file.save_as(dre_path)
        print(f"✅ DRE salvo em: {dre_path}")
    except Exception as e:
        print("Erro ao exportar DRE:", e)
        page.screenshot(path="erro_dre.png")

    # 3. FLUXO DE CAIXA
    print("Acessando Fluxo de Caixa Mensal...")
    page.goto("https://app.contaazul.com/#/relatorios/fluxo-de-caixa/mensal") #link fluxo de caixa
    page.wait_for_timeout(6000)

    print("Clicando em Filtrar Relatório...")
    page.click('button:has-text("Filtrar Relatório")')
    page.wait_for_timeout(5000)

    print("Exportando Fluxo de Caixa...")
    try:
        with page.expect_download() as fluxo_download:
            page.click('#conteudo > div > div.container.hidden-print > div:nth-child(2) > div > div > button')
        fluxo_file = fluxo_download.value
        fluxo_path = os.path.join(pasta_download, "fluxo_caixa.csv")
        fluxo_file.save_as(fluxo_path)
        print(f"Fluxo de Caixa salvo em: {fluxo_path}")
    except Exception as e:
        print("Erro ao exportar Fluxo de Caixa:", e)
        page.screenshot(path="erro_fluxo.png")

    page.wait_for_timeout(3000)
    browser.close()
