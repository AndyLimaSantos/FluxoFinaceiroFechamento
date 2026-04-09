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
nome_estoque_mapeado = str(input())
#temos aqui o chamado das planilhas
dataKitEstoque = pd.read_excel(nome_kit)
dataEstoque = pd.read_excel(nome_estoque)
dataEstoque_mapeado = pd.read_excel(nome_estoque_mapeado)
#pegando a parte importante da planilha de kit
dataKit = pd.DataFrame(data = {"SKU":dataKitEstoque["KIT SKU"].astype(str),\
                               "Custo Médio":dataKitEstoque["Custo Médio"].astype(float)})
#pegando a parte importante da planilha de Estoque
dataEstoque = pd.DataFrame(data = {"SKU":dataEstoque["SKU"].astype(str),\
                                   "Custo Médio":dataEstoque["Custo Médio"].astype(float)})
#Criação dos dos SKUS vendidos
data_uniao = pd.concat([dataKit,dataEstoque])
#filtro dos dados que não possuem informações de anuncio e dos que possuem
dataSKU_SKUanuncio = dataEstoque_mapeado.dropna()
dataSKU_comSKUanuncio = pd.DataFrame(data = {"SKU":dataSKU_SKUanuncio["SKU"],\
                                             "Mapeado SKU do Anúncio":dataSKU_SKUanuncio["Mapeado SKU do Anúncio"]})
#essa pode ser desconsiderada por um momento.
#dataSKU_semSKUanuncio = dataEstoque_mapeado[dataEstoque_mapeado["Mapeado SKU do Anúncio"].isnull()] #essa pode ser desconsiderada por um momento.

#criamos um novo banco de dados que é o relacional.
elementos = dataSKU_comSKUanuncio.shape[0]
sku_armazem_elementos = []
sku_venda_elementos = []
custo_venda_elementos = []
indices_presentes = list(dataSKU_comSKUanuncio.index)
for i in range(len(indices_presentes)):
    sku_armazem = dataSKU_comSKUanuncio.loc[indices_presentes[i],"SKU"]
    sku_anuncio = dataSKU_comSKUanuncio.loc[indices_presentes[i],"Mapeado SKU do Anúncio"]
    indice = data_uniao.index[data_uniao['SKU'] == sku_armazem].tolist() #Uma lista com os indices presentes com o sku
    if len(indice) > 0:
        valor = data_uniao.iloc[indice[0]]["Custo Médio"]
        sku_armazem_elementos.append(sku_armazem)
        sku_venda_elementos.append(sku_anuncio)
        custo_venda_elementos.append(float(valor))
SKU_mapeamento_atual = pd.DataFrame(data = {"SKU":sku_armazem_elementos,\
                                            "SKU Seller":sku_venda_elementos,\
                                            "Custo Médio":custo_venda_elementos})

#Exportação em .csv ou .xlsx
SKU_mapeamento_atual.to_csv("SKU2SKUarmazem.csv")
#SKU_mapeamento_atual.to_excel("SKU2SKUarmazem.xlsx")