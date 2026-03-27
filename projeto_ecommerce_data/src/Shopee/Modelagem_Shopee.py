'''
Aqui estaremos fazendo a modelagem dos dados da shopee
de maneira que no final tenhamos os indicativos necessarios
para execucao das analises mais simples
'''
#importacao das bibliotecas necessarias para analise das vendas
import pandas as pd
#Importacao dos bancos de dados
dadosDePedidos =  pd.read_excel("Order_all.xlsx")
dadosDeCusto = pd.read_excel("Export_Order_shopee.xlsx")
dadosSKU2SKUA = pd.read_excel("SKU2SKUArmazem.xlsx")
#dados de ids considerados anteriormente, mas que podem ter sofridos alguma alteracao
dadosIdConsiderados = pd.read_excel("ID_anterior_considerado.xlsx")
#funcoes que utilizaremos parea analise
def sku_armazem(dadosP, dadosS):
    linhas = dadosP.shape[0]
    sku_armazem = []
    for i in range(0,linhas):
        sku_venda = dadosP.loc[i,'Número de referência SKU']
        indices = list(dadosS[dadosS['SKU de Loja/Venda'] == sku_venda].index)
        if len(indices) == 0:
            sku_armazem.append("Não encontrado")
        if len(indices) > 0:
            sku_armazem.append(dadosS.loc[indices[0],'SKU Armazem'])
    return sku_armazem
def custo(dadosP, dadosCusto):
    linhas = dadosP.shape[0]
    custo = []
    for i in range(0,linhas):
        sku_armazem = dadosP.loc[i,'SKU Armazem']
        indices = list(dadosCusto[dadosCusto['SKU (Armazém)'] == sku_armazem].index)
        if len(indices) == 0:
            custo.append(0)
        if len(indices) > 0:
            custo.append(dadosCusto.loc[indices[0],'Custo Médio'])
    return custo
#Criamos um novo banco de dados
dadosFiltrados = pd.DataFrame(data = {'ID do pedido':dadosDePedidos['ID do pedido'].astype(str),\
                                      'Status do pedido':dadosDePedidos['Status do pedido'].astype(str),\
                                      'Número de referência SKU':dadosDePedidos['Número de referência SKU'].astype(str),\
                                      'Returned quantity':dadosDePedidos['Returned quantity'].astype(int),\
                                      'Subtotal do produto':dadosDePedidos['Subtotal do produto'].astype(float),\
                                      'Preço original':dadosDePedidos['Preço original'].astype(float),\
                                      'Desconto do vendedor':dadosDePedidos['Desconto do vendedor'].astype(float),\
                                      'Quantidade':dadosDePedidos['Quantidade'],\
                                      'Valor estimado do frete':dadosDePedidos['Valor estimado do frete'].astype(float),\
                                      'Taxa de envio pagas pelo comprador':dadosDePedidos['Taxa de envio pagas pelo comprador'].astype(float),\
                                      'Desconto de Frete Aproximado':dadosDePedidos['Desconto de Frete Aproximado'].astype(float),\
                                      'Taxa de transação':dadosDePedidos['Taxa de transação'].astype(float),\
                                      'Taxa de Envio Reversa':dadosDePedidos['Taxa de Envio Reversa'].astype(float),\
                                      'Taxa de comissão bruta':dadosDePedidos['Taxa de comissão bruta'].astype(float),\
                                      'Taxa de serviço bruta':dadosDePedidos['Taxa de serviço bruta'].astype(float)})
dadosFiltrados_custo = pd.DataFrame(data = {'SKU':dadosDeCusto['SKU'].astype(str),\
                                            'SKU (Armazém)':dadosDeCusto['SKU (Armazém)'].astype(str),\
                                            'Custo Médio':dadosDeCusto['Custo Médio'].astype(float)})
#Adicionamos o custo dos pedidos, antes de filtrar
skuArma = sku_armazem(dadosFiltrados, dadosSKU2SKUA)
dadosFiltrados["SKU Armazem"] = skuArma
custos = custo(dadosFiltrados, dadosFiltrados_custo)
dadosFiltrados["Custo Unitário"] = custos
dadosFiltrados["Custo total"] = dadosFiltrados['Quantidade'] * dadosFiltrados["Custo Unitário"]
#filtramos os pedidos que estao cancelados.
dadosFiltrados = dadosFiltrados[dadosFiltrados['Status do pedido'] != 'Cancelado']
#resetamos os indices para possiveis interacoes
dadosFiltrados_reset = dadosFiltrados.reset_index()
#retiramos a coluna com os indices anteriores
dadosFiltradosNovos  = dadosFiltrados_reset.drop("index", axis = 1)

#---------------------Calculos feitos com os id's que sofreram-----------------------------------

# vamos verificar os id's que tem na nossa mas não tem na dela
bibi_verifica_ID ={separa_per_return: grupo for separa_per_return, grupo in dadosFiltradosNovos.groupby('Returned quantity')} #usaremos os dados filtrados.
verifica_ID = bibi_verifica_ID[0] #pegamos apenas aqueles pedidos que não devolvido.
# precisamos tambêm da tabela com os ids que ela considerou no calculo.
nao_existem = dadosIdConsiderados.loc[~dadosIdConsiderados["ID do pedido (anterior)"].isin(verifica_ID["ID do pedido"]),"ID do pedido (anterior)"]
#base de dadosque foi consideado no calculo anteriror como valor positivo.
baseAmais = dadosFiltrados[dadosFiltrados['ID do pedido'].isin(nao_existem)] ########################AQUIIIIIIIIIIIIIIIIIII###########################
#vamos separar os duplicados e os não duplicados
duplicaAmais = baseAmais[baseAmais.duplicated(subset=['ID do pedido'], keep=False)]
semduplicaAmais = baseAmais[baseAmais.duplicated(subset=['ID do pedido'], keep=False) == False]

#calculamos as taxas consideradas antes______
#calcular a taxa leva em consideração a primeira amostra apenas
first_aparicao = duplicaAmais[duplicaAmais.duplicated(subset=['ID do pedido'], keep='first') == False]
#receita anterior
receita_ant = baseAmais['Subtotal do produto'].sum()
#calculo da comissão da shopee dos duplicados e sem duplicar
comissaoShopee_ant_semDup = semduplicaAmais['Taxa de comissão bruta'].sum()
comissaoShopee_ant = first_aparicao['Taxa de comissão bruta'].sum()
comissaoAntFinal = comissaoShopee_ant_semDup + comissaoShopee_ant
#Taxa de Transação dos duplicados e sem duplicar
taxaTransacao_ant_semDup = semduplicaAmais['Taxa de transação'].sum()
taxaTransacao_ant = first_aparicao['Taxa de transação'].sum()
taxaTransacaoAntFinal = taxaTransacao_ant_semDup + taxaTransacao_ant
#Taxa de Serviço dos duplicados e sem duplicar
taxaServico_ant_semDup = semduplicaAmais['Taxa de serviço bruta'].sum()
taxaServico_ant = first_aparicao['Taxa de serviço bruta'].sum()
taxaDeServicoAntFinal = taxaServico_ant_semDup + taxaServico_ant
#custo anterior considerado
custoAntFinal = baseAmais['Custo total'].sum()
#Valor do Frete dos duplicados e sem duplicar
frete_ant_semDup = semduplicaAmais['Valor estimado do frete'].sum()\
- semduplicaAmais['Taxa de envio pagas pelo comprador'].sum()\
- semduplicaAmais['Desconto de Frete Aproximado'].sum()
frete_ant = first_aparicao['Valor estimado do frete'].sum()\
- first_aparicao['Taxa de envio pagas pelo comprador'].sum()\
- first_aparicao['Desconto de Frete Aproximado'].sum()
freteAntFinal =  frete_ant_semDup + frete_ant
#imposto anterior contabilizado
imposto_ant = receita_ant*0.1*0.0924
#---------------------------------------------------------------------------------------------------

#aqui ele filtra os dados que estão repetidos, podemos utilizar isso para zerar  todos eles
#Esse devemos ter um olhar um pouco mais critico.
duplicados = dadosFiltradosNovos[dadosFiltradosNovos.duplicated\
                                 (subset=['ID do pedido'], keep=False)] 
#Esse data frame contem os elementos não duplicados 
semDuplicatas = dadosFiltradosNovos[dadosFiltradosNovos.duplicated\
                                    (subset=['ID do pedido'], keep=False)  == False]

#-------------------------------Calculo dos elementos sem duplicacao --------------------------------
#Aqui separamos os dados entre aqueles que não possuem devoluções, ou seja return 
#e consideramos apenas aqueles que não estão repetidos. -----------------------------------------------------------------------------------------------------------------------
separaPerReturn_semDupli = {separa_per_return: grupo for separa_per_return, grupo in semDuplicatas.groupby('Returned quantity')}
#Pegamos a planilhja que possui os filtros e aplicamos os calculos desejados já.
dataAnalise = separaPerReturn_semDupli[0]
#calculo da receita
receita = dataAnalise['Subtotal do produto'].sum()
#Calculo dos Impostos
imposto = receita*0.1*0.0924
#calculo da comissão da shopee
comissaoShopee = dataAnalise['Taxa de comissão bruta'].sum()
#Taxa de Transação
taxaTransacao = dataAnalise['Taxa de transação'].sum()
#Taxa de Serviço
taxaServico = dataAnalise['Taxa de serviço bruta'].sum()
#Valor do Frete
frete = dataAnalise['Valor estimado do frete'].sum()\
- dataAnalise['Taxa de envio pagas pelo comprador'].sum()\
- dataAnalise['Desconto de Frete Aproximado'].sum()
#Custo
custo = dataAnalise['Custo total'].sum()
#Fechamento antes da correcao

#----------------------------------calculo dos elementos com duplicacao-----------------------------

#Trabalharemos aqui com os resultados duplicados.
#Para o calculo das taxas podemos pegar apenas as primeira linhas.
separaPerReturn_dupli = {separa_per_return: grupo for separa_per_return, grupo in duplicados.groupby('Returned quantity')} #separa os elementos duplicados entre os que retornaram e os que não retornaram
dataAnalise_Dupli = separaPerReturn_dupli[0] #pegamos apenbas os que não retornaram
calculo_taxa_repe = dataAnalise_Dupli[dataAnalise_Dupli.duplicated(subset=['ID do pedido'], keep='first') == False] #pegamos apenas a primeira linha dos elementos duplicados que retornaram para o calculo das taxas

#calculo da comissão da shopee
comissaoShopee_repe = calculo_taxa_repe['Taxa de comissão bruta'].sum()
#Taxa de Transação
taxaTransacao_repe = calculo_taxa_repe['Taxa de transação'].sum()
#Taxa de Serviço
taxaServico_repe = calculo_taxa_repe['Taxa de serviço bruta'].sum()
#Valor do Frete
frete_repe = calculo_taxa_repe['Valor estimado do frete'].sum()\
- calculo_taxa_repe['Taxa de envio pagas pelo comprador'].sum()\
- calculo_taxa_repe['Desconto de Frete Aproximado'].sum()
#calculo do custo
custo_repe = dataAnalise_Dupli['Custo total'].sum()
#Valores relacionados a receita são calculados utilizando 3 indicadore consideramos os duplicados TODOS
receita_dupli = dataAnalise_Dupli['Subtotal do produto'].sum()
#Imposto
imposto_repe = receita_dupli*0.1*0.0924

#------------------------Calculo Final-------------------------------------------------------------
#Calculo Final.
receita_final = receita + receita_dupli
imposto_final = receita_final*0.1*0.0924
frete_final = frete + frete_repe
comissao_final = comissaoShopee + comissaoShopee_repe
taxa_transacao_final = taxaTransacao + taxaTransacao_repe
taxa_servico_final = taxaServico + taxaServico_repe
custo_final = custo + custo_repe

print('Fechamento de pedidos considerados como return 0 no fechamento anterior')
print('--------------------------------------------')
print(f'Receita____________________________ {receita_ant:<15.2f}')
print(f'Impostsos__________________________ {imposto_ant:<15.2f}')
print(f'Frete______________________________ {freteAntFinal:<15.2f}')
print(f'Custo total________________________ {custoAntFinal:<15.2f}')
print(f'Comissão Shopee____________________ {comissaoAntFinal:<15.2f}')
print(f'Taxas de Transação_________________ {taxaTransacaoAntFinal:<15.2f}')
print(f'Taxa de Serviços da shopee_________ {taxaDeServicoAntFinal:<15.2f}')
print('--------------------------------------------')


print('Fechamento antes de verificar os itens repetidos')
print('--------------------------------------------')
print(f'Receita____________________________ {receita:<15.2f}')
print(f'Impostsos__________________________ {imposto:<15.2f}')
print(f'Frete______________________________ {frete:<15.2f}')
print(f'Custo total________________________ {custo:<15.2f}')
print(f'Comissão Shopee____________________ {comissaoShopee:<15.2f}')
print(f'Taxas de Transação_________________ {taxaTransacao:<15.2f}')
print(f'Taxa de Serviços da shopee_________ {taxaServico:<15.2f}')
print('--------------------------------------------')

print('Fechamento dos itens repetidos')
print('--------------------------------------------')
print(f'Receita____________________________ {receita_dupli:<15.2f}')
print(f'Impostsos__________________________ {imposto_repe:<15.2f}')
print(f'Frete______________________________ {frete_repe:<15.2f}')
print(f'Custo total________________________ {custo_repe:<15.2f}')
print(f'Comissão Shopee____________________ {comissaoShopee_repe:<15.2f}')
print(f'Taxas de Transação_________________ {taxaTransacao_repe:<15.2f}')
print(f'Taxa de Serviços da shopee_________ {taxaServico_repe:<15.2f}')

#Fechamento antes da correção
print('Fechamento após de verificar os itens repetidos')
print('--------------------------------------------')
print(f'Receita____________________________ {receita_final:<15.2f}')
print(f'Impostsos__________________________ {imposto_final:<15.2f}')
print(f'Frete______________________________ {frete_final:<15.2f}')
print(f'Custo total________________________ {custo_final:<15.2f}')
print(f'Comissão Shopee____________________ {comissao_final:<15.2f}')
print(f'Taxas de Transação_________________ {taxa_transacao_final:<15.2f}')
print(f'Taxa de Serviços da shopee_________ {taxa_servico_final:<15.2f}')
print('--------------------------------------------')