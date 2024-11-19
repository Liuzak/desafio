# PAYLOADS

def payload_carregar_abas(format_data_value_locally, show_params, sticky_session_key, filter_tile_size, locale, language, features_json, keychain_version):
    payload_carregar_abas = {
        'worksheetPortSize': '{"w":1138,"h":800}',
        'dashboardPortSize': '{"w":1138,"h":800}',
        'clientDimension': '{"w":1138,"h":700}',
        'renderMapsClientSide': 'true',
        'isBrowserRendering': 'true',
        'browserRenderingThreshold': '100',
        'formatDataValueLocally': format_data_value_locally,
        'clientNum': '',
        'navType': 'Nav',
        'navSrc': 'Boot',
        'devicePixelRatio': '1.125',
        'clientRenderPixelLimit': '16000000',
        'allowAutogenWorksheetPhoneLayouts': 'false',
        'sheet_id': 'Desligamento por Descumprimento ',
        'showParams': show_params,
        'stickySessionKey': sticky_session_key,
        'filterTileSize': filter_tile_size,
        'locale': locale,
        'language': language,
        'verboseMode': 'false',
        '%3Asession_feature_flags': features_json,
        'keychain_version': keychain_version,
        'can_data_orientation_auto_open': 'false'
    }
    return payload_carregar_abas

def payload_dados_cnpj(valor_filtro, id_cnpj):
    payload_dados_cnpj = {
        "visualIdPresModel": (None, '{"worksheet":"Desligamento por Descumprimento","dashboard":"Desligamento por Descumprimento "}'),
        "globalFieldName": (None, f'[{valor_filtro}].[none:CNPJ do Agente:nk]'),
        "membershipTarget": (None, "filter"),
        "filterIndices": (None, f"[{id_cnpj}]"),
        "filterUpdateType": (None, "filter-replace")
    }
    return payload_dados_cnpj