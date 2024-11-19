# IMPORTES

from desafio_DADOS import *
import requests
import json
import re

# Funções para realizar os passos do desafio
with requests.session() as s:

    # Faz uma requisição inicial e obtém valores de configuração e sessão
    def pegar_valores():    
        url = f'https://public.tableau.com/vizql/w/BoletimdeSeguranadeMercado-18_11_2024/v/NoAporteGarantiasFinanceiras/startSession/viewing?:embed=y&:showVizHome=no&:host_url=https://public.tableau.com/&:embed_code_version=3&:tabs=yes&:toolbar=yes&:animate_transition=yes&:display_static_image=no&:display_spinner=no&:display_overlay=yes&:display_count=yes&:language=pt-BR&:loadOrderID=0&:redirect=auth'

        pegar_valores_POST = s.post(url) 

        if pegar_valores_POST.status_code == 200:
            # X-Session-Id
            session_id = pegar_valores_POST.headers.get('X-Session-Id')

            # Converter para dicionário e pegar os valores
            json_data = json.loads(pegar_valores_POST.text)

            format_data_value_locally = json_data["formatDataValueLocally"]

            show_params = json_data["showParams"]

            sticky_session_key = json_data["stickySessionKey"]

            filter_tile_size = json_data["filterTileSize"]

            locale = json_data["locale"]

            language = json_data["language"]

            features_json = json_data["features_json"]

            keychain_version = json_data["keychain_version"]

            return session_id, format_data_value_locally, show_params, sticky_session_key, filter_tile_size, locale, language, features_json, keychain_version
        
    # Faz uma requisição para carregar as abas e pegar o valor do filtro
    def carregar_abas(session_id, format_data_value_locally, show_params, sticky_session_key, filter_tile_size, locale, language, features_json, keychain_version): 
        url = f'https://public.tableau.com/vizql/w/BoletimdeSeguranadeMercado-18_11_2024/v/NoAporteGarantiasFinanceiras/bootstrapSession/sessions/{session_id}' 

        carregar_abas_POST = s.post(
            url,
            data = payload_carregar_abas(format_data_value_locally, show_params, sticky_session_key, filter_tile_size, locale, language, features_json, keychain_version)
        )

        if carregar_abas_POST.status_code == 200:
            html = carregar_abas_POST.text

            # Valor do filtro
            valor_filtro = re.search(r'"name\\":\[\\\"(federated\.[^\\\"]+)', html).group(1) 

            return valor_filtro

    # Faz uma requisição para pesquisar o CNPJ e retorna seu ID correspondente
    def pesquisar_cnpj(session_id, valor_filtro, cnpj):
        url = f'https://public.tableau.com/vizql/w/BoletimdeSeguranadeMercado-18_11_2024/v/NoAporteGarantiasFinanceiras/searchwithindex/sessions/{session_id}/sheets/Desligamento%20por%20Descumprimento/filters/%5B{valor_filtro}%5D.%5Bnone%3ACNPJ%20do%20Agente%3Ank%5D?query={cnpj}&maxRows=100&domain=database' 

        pesquisar_cnpj_GET = s.get(url)

        if pesquisar_cnpj_GET.status_code == 200:
            # Converter para dicionário e pegar o valor do id_cnpj
            json_data = json.loads(pesquisar_cnpj_GET.text)

            id_cnpj = json_data['indices'][0]

            return id_cnpj

    # Retorna um dicionário com as informações extraídas e formatadas
    def valores_planilha(json_data):
        # Extrair os segmentos de dados
        data_columns = json_data['dataSegments']['0']['dataColumns']
        real_value = data_columns[0]['dataValues'][0]  # Valor real (rcad)
        cstring_values = data_columns[1]['dataValues']  # Valores de cstring

        # Trocar '%null%' por 'NULL'
        cstring_values = ['NULL' if value == '%null%' else value for value in cstring_values]

        # Identificar os valores principais
        valor_cnpj = cstring_values[0]
        periodo_monitoramento = next(value for value in cstring_values if '/' in value)
        status = next(value for value in cstring_values if "Suspenso" in value)

        # Determinar índices para identificação de classe, representante e sigla
        date_index = cstring_values.index(periodo_monitoramento)

        # Mapear corretamente os campos baseado na estrutura do JSON
        classe = cstring_values[date_index + 1]
        representante = "NULL" if "Caucionado" in cstring_values else cstring_values[date_index + 2]
        sigla = cstring_values[date_index + 3]

        # Separar os valores antes da data
        antes_da_data = " | ".join(cstring_values[1:date_index])

        # Valores após o status
        status_index = cstring_values.index(status)
        depois_do_status = " | ".join(cstring_values[status_index + 1:])

        # Montar o resultado
        return {
            "representante": representante,
            "sigla": sigla,
            "valor_cnpj": valor_cnpj,
            "classe": classe,
            "status": status,
            "periodo_monitoramento": periodo_monitoramento,
            "rcad": real_value,
            "caucionamento": antes_da_data,
            "tipos_descumprimentos": depois_do_status
        }

    # Faz uma requisição para buscar e retorna os dados de um CNPJ
    def dados_cnpj(session_id, valor_filtro, id_cnpj): 
        url = f'https://public.tableau.com/vizql/w/BoletimdeSeguranadeMercado-18_11_2024/v/NoAporteGarantiasFinanceiras/sessions/{session_id}/commands/tabdoc/categorical-filter-by-index' 

        dados_cnpj_POST = s.post(
            url,
            files = payload_dados_cnpj(valor_filtro, id_cnpj)
        )

        if dados_cnpj_POST.status_code == 200:
            # O que determina se o CNPJ possui desligamento é a presença de 'dataDictionary' na variável 'data'
            html = dados_cnpj_POST.text
            data = json.loads(html)
            json_data = data['vqlCmdResponse']['layoutStatus']['applicationPresModel']['dataDictionary']

            retorno = valores_planilha(json_data)

            return retorno 
