# IMPORTS
from desafio_PASSOS import *
import pandas as pd
import os

# Obter o diretório do script em execução
caminho = os.path.dirname(os.path.abspath(__file__))

# Ler planilha com os 10 exemplos
df = pd.read_excel(os.path.join(caminho, 'planilha_desafio.xlsx'))

# Tamanho da planilha
print(f"Número de linhas na planilha: {len(df)}")

# Processar cada linha do DataFrame
for index, row in df.iterrows():
    try:
        # Validação do CNPJ
        cnpj = str(row['CNPJ']).strip()
        if not cnpj or not cnpj.isdigit():
            df.at[index, 'Status Final'] = 'CNPJ inválido!'
            print(f"{index + 1}: CNPJ inválido ({cnpj}).")
            continue

        # Obter valores de sessão e configuração
        session_id, format_data_value_locally, show_params, sticky_session_key, filter_tile_size, locale, language, features_json, keychain_version = pegar_valores()

        # Carregar dados da aba e obter valor do filtro
        valor_filtro = carregar_abas(session_id, format_data_value_locally, show_params, sticky_session_key, filter_tile_size, locale, language, features_json, keychain_version)

        # Pesquisar CNPJ e obter o ID correspondente
        id_cnpj = pesquisar_cnpj(session_id, valor_filtro, cnpj)

        # Obter dados do CNPJ
        retorno = dados_cnpj(session_id, valor_filtro, id_cnpj)

        # Atualizar o DataFrame com os resultados
        df.at[index, 'Representante'] = retorno.get('representante', '')
        df.at[index, 'Sigla'] = retorno.get('sigla', '')
        df.at[index, 'CNPJ'] = int(cnpj)
        df.at[index, 'Classe'] = retorno.get('classe', '')
        df.at[index, 'Status'] = retorno.get('status', '')
        df.at[index, 'Período de Monitoramento | Data do Desligamento'] = retorno.get('periodo_monitoramento', '')
        df.at[index, 'RCAd'] = retorno.get('rcad', '')
        df.at[index, 'Suspensão do Fornecimento (REN 1.014/2022)'] = '-'
        df.at[index, 'Tipos Descumprimentos'] = retorno.get('tipos_descumprimentos', '')
        df.at[index, 'Caucionamento'] = retorno.get('caucionamento', '')
        df.at[index, 'Status Final'] = 'CNPJ com restrição'

        print(f"{index + 1}: CNPJ {cnpj} processado com sucesso!")
    except Exception as erro:
        # Tratar caso de erro específico
        if 'dataDictionary' in str(erro):
            df.at[index, 'Status Final'] = 'CNPJ sem restrição'
            print(f"{index + 1}: CNPJ {cnpj} está sem restrição")
        else:
            df.at[index, 'Status Final'] = 'Erro no processamento'
            print(f"{index + 1}: Erro ao processar CNPJ {cnpj}: {erro}")

# Salvar o resultado final
df.to_excel(os.path.join(caminho, 'logs_desafio.xlsx'), index=False)
print(f"Processamento finalizado!")