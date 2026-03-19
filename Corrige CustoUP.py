'''
Esse código concerta a planilha de CustoUP, 
insere os valores de custo que não tinhamos
presentes na primeira parte.
'''
import pandas as pd
#Funções que iremos utilizar para concertar a planilha de Custo
def insere_SKU(custoUP):
    '''
    Correção da coluna de SKU Armazem
    a lógica é que para valores que o SKU
    não existe mas exisyte o SKU normal
    significa que ambos os valores são
    iguais sendo necessário apenas uma
    substituição do valor,
    '''
    elementos_skuarmazem_nulo = list(custoUP[custoUP['SKU (Armazém)'].isnull()].index)
    for i in range(len(elementos_skuarmazem_nulo)):
        custoUP.loc[elementos_skuarmazem_nulo[i],"SKU (Armazém)"] = custoUP.loc[elementos_skuarmazem_nulo[i],"SKU"]
    return custoUP

def insere_custo(custoUP, dataSKU):
    elementos_custo_nulo = list(custoUP[custoUP['Custo Médio'].isnull()].index) #faz uma lista de todos os indices que contem custo nulo
    for i in range(len(elementos_custo_nulo)):
        SKU_armazem = custoUP.loc[elementos_custo_nulo[i],"SKU (Armazém)"] #VALOR DO SKU DO ARMAZEM.
        indice = dataSKU.loc[dataSKU['SKU'] == SKU_armazem].index #retorna o index do valor do sku encontrado  na planilha de sku2skuarmazem)
        if not indice.empty:
            valor = int(indice[0])
            custoUP.loc[elementos_custo_nulo[i],"Custo Médio"] = dados_SKUArmazem.loc[valor,'Custo Médio']
        else:
            custoUP.loc[elementos_custo_nulo[i],"Custo Médio"] = 0
    return custoUP


def main():
    #Exportamos os bancos de dados que queremos trabalhar 
    dados_income = pd.read_csv("income.csv").drop("Unnamed: 0", axis =1)
    dados_custoUP = pd.read_csv("custoUP.csv").drop("Unnamed: 0", axis =1)
    dados_todosPedidos = pd.read_csv("todosPedidos.csv").drop("Unnamed: 0", axis =1)
    dados_devolucoes = pd.read_csv("devolucoes.csv").drop("Unnamed: 0", axis =1)
    dados_SKUArmazem = pd.read_csv("SKU2SKUarmazem.csv")

    #primeira correção da planilha, inserimos os valores de SKU do Armazem que faltam.

    # Correção dos valores de SKU's do Armazém
    dados_custoUP_filtro = insere_SKU(dados_custoUP)
    # Correção dos valores de custo
    custoUP_data = insere_custo(dados_custoUP_filtro, dados_SKUArmazem)

    #Salvar a planilha:
    custoUP_data.to_excel("custoUP.xlsx")
    custoUP_data.to_csv("custoUP.csv")
    return


if __name__ == "__main__":
    main()