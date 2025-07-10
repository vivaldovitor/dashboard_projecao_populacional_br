import pandas as pd

def load_population_data():
    df = pd.read_csv("data/processed/projecoes_populacao_idade_2000_2070.csv")

    # Converte colunas de ano para int
    new_columns = []
    for col in df.columns:
        try:
            new_columns.append(int(col))
        except ValueError:
            new_columns.append(col)
    df.columns = new_columns
    return df

population_data = load_population_data()

macro_regions = {
    "Norte": ["Acre","Amazonas","Amapá","Pará","Rondônia","Roraima","Tocantins"],
    "Nordeste": ["Alagoas","Bahia","Ceará","Maranhão","Paraíba","Pernambuco","Piauí","Rio Grande do Norte","Sergipe"],
    "Centro-Oeste": ["Distrito Federal","Goiás","Mato Grosso","Mato Grosso do Sul"],
    "Sudeste": ["Espírito Santo","Minas Gerais","Rio de Janeiro","São Paulo"],
    "Sul": ["Paraná","Rio Grande do Sul","Santa Catarina"]
}