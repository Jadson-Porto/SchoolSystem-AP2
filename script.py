from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
import time
import json
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime
import os

def extrair_endpoints_selenium():
    docs_urls = [
        'http://localhost:5000/docs',
        'http://localhost:5001/docs', 
        'http://localhost:5002/docs'
    ]
    

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    endpoints_encontrados = []
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        
        for url in docs_urls:
            try:
                print(f" Navegando para: {url}")
                driver.get(url)
                time.sleep(3)

                elements = driver.find_elements(By.CSS_SELECTOR, "[class*='opblock-tag'], [class*='operation'], [class*='path']")
                
                for element in elements:
                    text = element.text
                    if text and '/' in text and 'localhost' not in text:
                        lines = text.split('\n')
                        for line in lines:
                            if line.startswith('/'):
                                full_url = f"http://localhost:{url.split(':')[-1].split('/')[0]}{line}"
                                if full_url not in endpoints_encontrados:
                                    endpoints_encontrados.append(full_url)
                                    print(f"    Endpoint: {line}")
                
                print(f" Extração de {url} concluída")
                
            except Exception as e:
                print(f" Erro em {url}: {e}")
        
        driver.quit()
        
    except Exception as e:
        print(f" Erro com Selenium: {e}")
        print("📋 Tentando método alternativo...")
        endpoints_encontrados = extrair_endpoints_alternativo()
    
    return endpoints_encontrados

def extrair_endpoints_alternativo():
    endpoints_comuns = []
    
    bases = ['5000', '5001', '5002']
    paths = ['/users', '/items', '/products', '/orders', '/customers', 
             '/api/v1/users', '/api/v1/items', '/api/users', '/api/items']
    
    for base in bases:
        for path in paths:
            endpoints_comuns.append(f'http://localhost:{base}{path}')
    
    return endpoints_comuns

def testar_endpoints(endpoints):
    endpoints_validos = []
    
    for endpoint in endpoints:
        try:
            print(f"Testando: {endpoint}")
            response = requests.get(endpoint, timeout=5)
            
            if response.status_code == 200:
                dados = response.json()
                if isinstance(dados, list) and len(dados) > 0:
                    endpoints_validos.append((endpoint, dados))
                    print(f" DADOS ENCONTRADOS: {endpoint} - {len(dados)} registros")
                elif isinstance(dados, dict):
                    endpoints_validos.append((endpoint, [dados]))
                    print(f" Dados (dict): {endpoint}")
                else:
                    print(f" Sem dados válidos: {endpoint}")
            else:
                print(f" Status {response.status_code}: {endpoint}")
                
        except Exception as e:
            print(f" Erro: {endpoint} - {e}")
    
    return endpoints_validos

def criar_pdf(endpoints_com_dados, nome_arquivo=None):
    
    if not endpoints_com_dados:
        print(" Nenhum dado para gerar PDF")
        return None
    
    if nome_arquivo is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"relatorio_api_{timestamp}.pdf"
    
    doc = SimpleDocTemplate(nome_arquivo, pagesize=A4, topMargin=30)
    elements = []
    styles = getSampleStyleSheet()
    
    titulo = Paragraph("RELATÓRIO COMPLETO DA API", styles['Title'])
    elements.append(titulo)
    elements.append(Spacer(1, 12))
    
    data_geracao = Paragraph(f"Data de geração: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", styles['Normal'])
    elements.append(data_geracao)
    
    total_endpoints = len(endpoints_com_dados)
    total_registros = sum(len(dados) for _, dados in endpoints_com_dados)
    info_relatorio = Paragraph(f"Endpoints encontrados: {total_endpoints} | Total de registros: {total_registros}", styles['Normal'])
    elements.append(info_relatorio)
    elements.append(Spacer(1, 20))
    
    for i, (url, dados) in enumerate(endpoints_com_dados, 1):
        titulo_endpoint = Paragraph(f"ENDPOINT {i}: {url}", styles['Heading2'])
        elements.append(titulo_endpoint)
        elements.append(Spacer(1, 8))
        
        info_dados = Paragraph(f"Registros encontrados: {len(dados)}", styles['Normal'])
        elements.append(info_dados)
        elements.append(Spacer(1, 12))
        
        if dados and len(dados) > 0:

            cabecalho = list(dados[0].keys())
            dados_tabela = [cabecalho]
            
            for registro in dados[:100]:
                linha = []
                for campo in cabecalho:
                    valor = registro.get(campo, '')
                    if isinstance(valor, str) and len(valor) > 50:
                        valor = valor[:47] + "..."
                    linha.append(str(valor))
                dados_tabela.append(linha)
            
            tabela = Table(dados_tabela, repeatRows=1)
            
            estilo = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                

                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 7),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
            ])
            
            tabela.setStyle(estilo)
            elements.append(tabela)
            

            if len(dados) > 100:
                aviso = Paragraph(f"<i>Nota: Mostrando os primeiros 100 de {len(dados)} registros</i>", styles['Italic'])
                elements.append(aviso)
        
        elements.append(Spacer(1, 25))
    

    elements.append(Spacer(1, 10))
    resumo = Paragraph(f"<b>RELATÓRIO CONCLUÍDO:</b> {len(endpoints_com_dados)} endpoint(s) processados com sucesso", styles['Heading3'])
    elements.append(resumo)
    

    try:
        doc.build(elements)
        print(f" PDF gerado com sucesso: {nome_arquivo}")
        return nome_arquivo
    except Exception as e:
        print(f" Erro ao gerar PDF: {e}")
        return None

def criar_pdfs_individuais(endpoints_com_dados):
    """Cria PDFs individuais para cada endpoint"""
    if not endpoints_com_dados:
        return
    
    print("\n Gerando PDFs individuais...")
    for url, dados in endpoints_com_dados:

        nome_base = url.replace('http://localhost:', '').replace('/', '_').strip('_')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"{nome_base}_{timestamp}.pdf"
        

        criar_pdf([(url, dados)], nome_arquivo)

def menu_exportacao(endpoints_validos):
    """Menu para escolher o tipo de exportação"""
    if not endpoints_validos:
        print(" Nenhum dado válido para exportar")
        return
    
    print(f"\n {len(endpoints_validos)} endpoints com dados encontrados!")
    print("=" * 60)
    
    for i, (url, dados) in enumerate(endpoints_validos, 1):
        print(f"{i}. {url} - {len(dados)} registros")
    
    print("\n OPÇÕES DE EXPORTAÇÃO PDF:")
    print("1.  PDF único com todos os endpoints")
    print("2.  PDFs individuais para cada endpoint")
    print("3.  Ambos (PDF único + individuais)")
    
    try:
        opcao = input("\nEscolha uma opção (1-3): ").strip()
        
        if opcao == "1":
            print("\n Gerando PDF único...")
            criar_pdf(endpoints_validos)
            
        elif opcao == "2":
            print("\n Gerando PDFs individuais...")
            criar_pdfs_individuais(endpoints_validos)
            
        elif opcao == "3":
            print("\n Gerando ambos...")
            criar_pdf(endpoints_validos)
            criar_pdfs_individuais(endpoints_validos)
            
        else:
            print(" Opção inválida. Gerando PDF único...")
            criar_pdf(endpoints_validos)
            
    except KeyboardInterrupt:
        print("\n Operação cancelada pelo usuário.")
    except Exception as e:
        print(f" Erro: {e}")

if __name__ == "__main__":
    print(" INICIANDO EXPORTAÇÃO DE DADOS DA API")
    print("=" * 50)
    
    print(" Extraindo endpoints das páginas /docs/...")
    endpoints = extrair_endpoints_selenium()
    
    if endpoints:
        print(f"\n {len(endpoints)} endpoints encontrados!")
        

        print("\n Testando endpoints...")
        endpoints_validos = testar_endpoints(endpoints)
        
        if endpoints_validos:

            menu_exportacao(endpoints_validos)
        else:
            print("\n Nenhum endpoint retornou dados válidos.")
    else:
        print("\n Nenhum endpoint encontrado.")
    
    print("\n Processo concluído!")