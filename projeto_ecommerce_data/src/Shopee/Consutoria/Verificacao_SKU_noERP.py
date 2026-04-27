import pandas as pd
#Funcoes utilizadas para o calculo
def verifica_in_armazem(dado_loja, dado_armazem):
    linhas = int(dado_loja.shape[0])
    colunas = list(dado_loja.columns)
    naoEncontrados = []
    valorCusto = []
    if 'Número de referência SKU' in colunas:
        for i in range(0, linhas):
            Sku_seller = dado_loja.loc[i, 'Número de referência SKU']
            existe = dado_armazem['SKU (Armazém)'].isin([Sku_seller]).any()
            if existe == False:
                naoEncontrados.append(Sku_seller)
                valorCusto.append(dado_loja.loc[i,"Custo unitário"])
    if 'SKU' in colunas:
        for i in range(0, linhas):
            Sku_seller = dado_loja.loc[i, 'SKU']
            existe = dado_armazem['SKU (Armazém)'].isin([Sku_seller]).any()
            if existe == False:
                naoEncontrados.append(Sku_seller)
                valorCusto.append(dado_loja.loc[i,"Custo Unitário"])
    return pd.DataFrame(data = {"SKU não encontrados": naoEncontrados,"Custo Unitário":valorCusto})

def main():
    print("Insira o numero de calculos que deverão ser feitos")
    n_calculos = int(input())
    cont = 0
    while cont < n_calculos:
        print("insira o nome do arquivo com os dados de todos os pedidos, com a extensao")
        nome_pedidos = str(input())