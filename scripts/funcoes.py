import pandas as pd

def carregar_dados(caminho_alertas_UAs):
    """Carrega os CSVs de alertas do corredor e do RS."""
    alertas_UAs = pd.read_csv(caminho_alertas_UAs)
    return alertas_UAs

def preparar_datas(alertas_UAs):
    """Converte a coluna de data e cria colunas auxiliares de mês/ano e trimestre."""
    alertas_UAs = alertas_UAs.copy()
    # %d = dia // %m = mes // %Y = ano 4 digitos e %y = ano 2 digitos
    alertas_UAs["DATADETEC"] = pd.to_datetime(alertas_UAs["DATADETEC"], format="%Y/%m/%d")
    alertas_UAs["MES_ANO"] = alertas_UAs["DATADETEC"].dt.to_period("M")
    alertas_UAs["TRIMESTRE"] = alertas_UAs["DATADETEC"].dt.to_period("Q")
    # Semestre: não existe código pronto no pandas, calculamos a partir do trimestre
    ano = alertas_UAs["TRIMESTRE"].dt.year
    trimestre_num = alertas_UAs["TRIMESTRE"].dt.quarter
    semestre_num = ((trimestre_num - 1) // 2) + 1
    alertas_UAs["SEMESTRE"] = ano.astype(str) + "S" + semestre_num.astype(str)
    return alertas_UAs


ESCALAS = {
    "mes": {"coluna": "MES_ANO", "label_eixo_x": "Mês/Ano", "titulo": "mês"},
    "trimestre": {"coluna": "TRIMESTRE", "label_eixo_x": "Trimestre", "titulo": "trimestre"},
    "ano": {"coluna": "ANODETEC", "label_eixo_x": "Ano", "titulo": "ano"},
    "semestre": {"coluna": "SEMESTRE", "label_eixo_x": "Semestre", "titulo": "semestre"}
}


def agrupar_por_UA(alertas_UAs, coluna_area="AREAHA", escala="semestre", coluna_id="id_min", operacao="sum"):
    """
    Agrupa a área (ou contagem de alertas) por escala escolhida (mes, trimestre, semestre ou ano) e por unidade amostral (id_min).
    Retorna uma tabela com o período nas linhas e cada id_min numa coluna.
    operacao pode ser "sum" (soma da área) ou "count" (contagem de alertas/linhas).
    Coloquei como default "AREAHA", "semestre", "id_min" e "sum" pq é o que a principio vamos usar, mas pode ser alterado na hora de chamar a função.
    """
    coluna_periodo = ESCALAS[escala]["coluna"]
    tabela = alertas_UAs.groupby([coluna_periodo, coluna_id])[coluna_area].agg(operacao)
    tabela = tabela.unstack(coluna_id, fill_value=0)

    return tabela