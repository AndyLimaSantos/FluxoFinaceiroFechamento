'''
Esse código tem como funçõa principal filtras as colunas importantes
que utilizaremos para fechar o balanço principal final, ele recolhe
três arquivos e retorna 3 planilhas de saida com as informações que 
utilizamos parea construção dos calculos principais.

OBS: A informaçõa de entradas do número de pedidos deve ser forneci-
da como uma planilha com extenção .csv por alguma razão ele não
reconhece uma planilha dessa em extrensão excel.
'''
# Bibliotecas utilizadas
import pandas as pd

# Funções criadas que usaremos no script

def modifica_corrige(coluna):
    coluna_filtro1 = coluna.str.replace('BRL ', '', regex=False)
    coluna_filtro2 = coluna_filtro1.str.replace(',','.', regex=False)
    coluna_filtro3 = coluna_filtro2.astype(float)
    return coluna_filtro3

def modifica_corrige_package(coluna):
    #filtra o package ID
    coluna_filtro1 = coluna.str.replace('\t', '', regex=False)
    coluna_filtro2 = coluna_filtro1.astype(str)
    coluna_filtro3 = coluna_filtro2.replace('', 'Cancelado', regex=False)
    return coluna_filtro3
# Importação dos dados brutos que utilizares e iremos limpar.
nome_pedidos = str(input())
nome_income = str(input())
nome_exportOrder = str(input())

todosPedidosBase = pd.read_csv(nome_pedidos)
incomeBase = pd.read_excel(nome_income)
exportOrderBase = pd.read_excel(nome_exportOrder)

#Corrige os valores e informações das colunas
todosPedidosBase['SKU Subtotal After Discount'] = modifica_corrige(todosPedidosBase['SKU Subtotal After Discount'])
todosPedidosBase['SKU Unit Original Price'] = modifica_corrige(todosPedidosBase['SKU Unit Original Price'])
todosPedidosBase['SKU Subtotal Before Discount'] = modifica_corrige(todosPedidosBase['SKU Subtotal Before Discount'])
todosPedidosBase['Package ID'] = modifica_corrige_package(todosPedidosBase['Package ID'])

#Eliminamos as colunas que não queremos escrevendo novos bancos de dados para os pedidos
#Eliminamos as colunas que não queremos escrevendo novos bancos de dados para os pedidos
todosPedidosBase_filtro = pd.DataFrame(data = {'Package ID':todosPedidosBase['Package ID'],\
                                               'Quantity':todosPedidosBase['Quantity'].astype(int),\
                                               'SKU Subtotal After Discount':todosPedidosBase['SKU Subtotal After Discount'],\
                                               'SKU Unit Original Price':todosPedidosBase['SKU Unit Original Price'],\
                                               'SKU Subtotal Before Discount':todosPedidosBase['SKU Subtotal Before Discount'],\
                                               'Sku Quantity of return':todosPedidosBase['Sku Quantity of return'].astype(int),\
                                               'Seller SKU':todosPedidosBase['Seller SKU'].astype(str)})
#Escrevemos um novo banco de dados para o Income
incomeBase_filtro = pd.DataFrame(data = {'ID do pedido/ajuste':incomeBase['ID do pedido/ajuste'].astype(str),\
                                         'Valor total a ser liquidado':incomeBase['Valor total a ser liquidado'].astype(float),\
                                         'Data do demonstrativo':incomeBase['Data do demonstrativo']})
#Escrevemos um novo banco de dados para o Export Order
exportOrder_filtro = pd.DataFrame(data = {'Nº de Pedido da Plataforma':exportOrderBase['Nº de Pedido da Plataforma'].astype(str),\
                                          'Custo Médio':exportOrderBase['Custo Médio'].astype(float),\
                                          'SKU':exportOrderBase['SKU'],\
                                          'SKU (Armazém)':exportOrderBase['SKU (Armazém)']})
#Escrevemos a planilha de devoluções
devolucoes = incomeBase_filtro[incomeBase_filtro ['Valor total a ser liquidado']<0]

#todosPedidosBase_filtro.to_csv('todosPedidos.csv')
#incomeBase_filtro.to_csv('income.csv')
#exportOrder_filtro.to_csv('custoUP.csv')
#devolucoes.to_csv("devolucoes.csv")


#todosPedidosBase_filtro.to_excel('todosPedidos.xlsx')
#incomeBase_filtro.to_excel('income.xlsx')
#exportOrder_filtro.to_excel('custoUP.xlsx')
#devolucoes.to_excel("devolucoes.xlsx")