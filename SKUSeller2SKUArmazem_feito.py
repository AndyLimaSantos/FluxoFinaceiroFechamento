''''
O objetivo desse código é executar a junção das duas tabelas 
do estoque, isso é uma parte fundamental para melhoria do cál-
culo do estoque.

O código se divide em algumas partes 
- Importação do banco de dados 
- Tratamento do banco de tados 
- Criação de um novo banco de dados agora com as tabelas SKU e
Custo Médio do produto
- Exportação da tabela correta.
'''

import pandas as pd
nome_kit = str(input())
nome_estoque = str(input())
dataKitEstoque = pd.read_excel(nome_kit)
dataEstoque = pd.read_excel(nome_estoque)
#Talvez fazer uma verificação dos valores que estão insentos.

#Pegando a parte importante da planilha de kit que são os dados de Kit Sku e Custo Médio
dataKit = pd.DataFrame(data = {"SKU":dataKitEstoque["KIT SKU"].astype(str),\
                               "Custo Médio":dataKitEstoque["Custo Médio"].astype(float)})
#pegando a parte importante da planilha de Estoque que são os dados de Sku e Custo Médio
dataEstoque = pd.DataFrame(data = {"SKU":dataEstoque["SKU"].astype(str),\
                                   "Custo Médio":dataEstoque["Custo Médio"].astype(float)})
#Aqui Concatenamos as tabelas
data_final = pd.concat([dataKit,dataEstoque])
#Exportação dos dados
#data_final.to_excel("Data_Estoque.xlsx")
#data_final.to_csv("SKU2SKUarmazem.csv")