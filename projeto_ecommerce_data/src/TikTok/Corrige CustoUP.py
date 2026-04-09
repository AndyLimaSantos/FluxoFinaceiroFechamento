'''
Esse código concerta a planilha de CustoUP, 
insere os valores de custo que não tinhamos
presentes na primeira parte.
'''
import pandas as pd
#Funções que iremos utilizar para concertar a planilha de Custo
def insere_SKU(custoUP, dados_SKUArmazem):
    elementos_skuarmazem_nulo = list(custoUP[custoUP['SKU (Armazém)'].isnull()].index)
    for i in range(len(elementos_skuarmazem_nulo)):
        sku_venda = custoUP.loc[elementos_skuarmazem_nulo[i],"SKU"]
        indices = list(dados_SKUArmazem[dados_SKUArmazem["SKU Seller"] == sku_venda].index)
        if len(indices) > 0:
            custoUP.loc[elementos_skuarmazem_nulo[i],"SKU (Armazém)"]= dados_SKUArmazem.loc[indices[0],"SKU"]
    #Modificação no custo
    elementos_custoarmazem_nulo = list(custoUP[custoUP['Custo Médio'].isnull()].index)
    for i in range(len(elementos_custoarmazem_nulo)):
        sku_Armazem = custoUP.loc[elementos_custoarmazem_nulo[i],"SKU (Armazém)"]
        sku_venda = custoUP.loc[elementos_custoarmazem_nulo[i],"SKU"]
        indices_armazem = list(dados_SKUArmazem[dados_SKUArmazem["SKU"] == sku_Armazem].index)
        indices_venda = list(dados_SKUArmazem[dados_SKUArmazem["SKU Seller"] == sku_venda].index)
        condicional = True
        if len(indices_armazem) > 0 and condicional == True:
            custoUP.loc[elementos_custoarmazem_nulo[i],"Custo Médio"]= dados_SKUArmazem.loc[indices_armazem[0],"Custo Médio"]
        if len(indices_venda) > 0 and condicional == True:
            custoUP.loc[elementos_custoarmazem_nulo[i],"Custo Médio"]= dados_SKUArmazem.loc[indices_venda[0],"Custo Médio"]
    return custoUP

def main():
    #Exportamos os bancos de dados que queremos trabalhar 
    dados_income = pd.read_csv("income.csv").drop("Unnamed: 0", axis =1)
    dados_custoUP = pd.read_csv("custoUP.csv").drop("Unnamed: 0", axis =1)
    dados_todosPedidos = pd.read_csv("todosPedidos.csv").drop("Unnamed: 0", axis =1)
    dados_devolucoes = pd.read_csv("devolucoes.csv").drop("Unnamed: 0", axis =1)
    dados_SKUArmazem = pd.read_csv("SKU2SKUarmazem.csv").drop("Unnamed: 0", axis =1)

    #Correção e inserção dos valores esperados
    dados = insere_SKU(dados_custoUP, dados_SKUArmazem)
    #Salvar a planilha:
    #custoUP_data.to_excel("custoUP.xlsx")
    custoUP_data.to_csv("custoUP_final.csv")
    return


if __name__ == "__main__":
    main()