import os
from pathlib import Path
import pandas as pd
from pandas import DataFrame
import numpy as np
import wget
from datetime import datetime
from dateutil.relativedelta import relativedelta


class dataFormat:
    def __init__(self):
        self.url = "https://sidra.ibge.gov.br/geratabela?format=us.csv&name=tabela1737.csv&terr=N&rank=-&query=t/1737/n1/all/v/all/p/all/d/v63%202,v69%202,v2263%202,v2264%202,v2265%202,v2266%2013/l/,v,p%2Bt"
        self.ano_mes = datetime.today().date()
        self.ano_mes = self.ano_mes + relativedelta(months=-1)
        self.ano_mes_formatado = self.ano_mes.strftime("%b%y").lower()
        self.file_path = f"data/ipca_{self.ano_mes_formatado}.csv"

    def dataDownload(self):
        if os.path.exists(f"data/ipca_{self.ano_mes_formatado}.csv"):
            return True
        else:
            return wget.download(
                url=self.url, out=f"data/ipca_{self.ano_mes_formatado}.csv"
            )

    def dataTransform(self) -> DataFrame:

        ipca_df: DataFrame = pd.read_csv(
            self.file_path, sep=",", encoding="utf-8-sig", skiprows=2, low_memory=False
        )

        column_rename: dict[str, str] = {
            "Unnamed: 1": "Território",
            "IPCA - Número-índice (base: dezembro de 1993 = 100) (Número-índice)": "Número-índice",
            "IPCA - Variação mensal (%)": "Variação mensal (%)",
            "IPCA - Variação acumulada em 3 meses (%)": "Variação 3 meses (%)",
            "IPCA - Variação acumulada em 6 meses (%)": "Variação 6 meses (%)",
            "IPCA - Variação acumulada no ano (%)": "Variação anual (%)",
            "IPCA - Variação acumulada em 12 meses (%)": "Variação 12 meses (%)",
        }

        ipca_df.rename(columns=column_rename, inplace=True)

        # Substituindo as pontuações
        ipca_df: DataFrame = ipca_df.replace("...", 0)

        # Retirando as linhas de fonte e notas de rodapé
        ipca_df: DataFrame = ipca_df.iloc[:-12]

        meses: dict[str, int] = {
            "janeiro": 1,
            "fevereiro": 2,
            "março": 3,
            "abril": 4,
            "maio": 5,
            "junho": 6,
            "julho": 7,
            "agosto": 8,
            "setembro": 9,
            "outubro": 10,
            "novembro": 11,
            "dezembro": 12,
        }

        # Dividindo a coluna de Mês para obter informação do Ano
        ipca_df[["Mês", "Ano"]] = ipca_df["Mês"].str.split(" ", expand=True)

        # Preenchendo a coluna Número do Mês de acordo com as chaves da variavel mes
        ipca_df["Número do Mês"] = ""
        ipca_df["Número do Mês"] = ipca_df["Mês"].map(meses)

        # Escolhendo colunas a serem visualizadas
        ipca_df = ipca_df[
            [
                "Ano",
                "Número do Mês",
                "Mês",
                "Número-índice",
                "Variação mensal (%)",
                "Variação 3 meses (%)",
                "Variação 6 meses (%)",
                "Variação anual (%)",
                "Variação 12 meses (%)",
            ]
        ]

        ipca_df["Ano"] = ipca_df["Ano"].astype(int)

        ipca_df[
            [
                "Número-índice",
                "Variação mensal (%)",
                "Variação 3 meses (%)",
                "Variação 6 meses (%)",
                "Variação anual (%)",
                "Variação 12 meses (%)",
            ]
        ] = ipca_df[
            [
                "Número-índice",
                "Variação mensal (%)",
                "Variação 3 meses (%)",
                "Variação 6 meses (%)",
                "Variação anual (%)",
                "Variação 12 meses (%)",
            ]
        ].astype(
            float
        )

        ipca_df.to_csv(
            f"output/ipca_formatado_{self.ano_mes_formatado}.csv",
            index=False,
            decimal=",",
            encoding="utf-8-sig",
            sep=";",
        )

        return ipca_df
