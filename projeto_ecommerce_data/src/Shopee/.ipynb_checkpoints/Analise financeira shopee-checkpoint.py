#Importacoes das blibliotecas que utilizaremos.
import pandas as pd
#Funcoes utilizadas
def banco_sem_duplas(dados):
    #cria um banco sem as duplicacoes
    return dados[dados.duplicated(subset=['ID do pedido'], keep=False) == False]
def banco_duplicado(dados):
    #cria um banco apenas de duplicacoes
    return dados[dados.duplicated(subset=['ID do pedido'], keep=False)]
def primeiros_duplicado(dados):
    #cria um banco com apenas os primeiros elementos das duplicacoes
    #utilizam o dataframe duplicado
    return dados[dados.duplicated(subset=['ID do pedido'], keep='first') == False]
def dados_para_analise(dados):
    #gera o banco que ira ser analisado return = 0
    bancos = {bancos: grupo for bancos, grupo in dados.groupby('Returned quantity')}
    return bancos[0]
def receita(dados):
    #gera a receita
    return dados['Subtotal do produto'].sum()
def frete(dados):
    #gera o frete
    valorEstimado = dados['Valor estimado do frete'].sum()
    taxaPagaCom = dados['Taxa de envio pagas pelo comprador'].sum()
    desconto = dados['Desconto de Frete Aproximado'].sum()
    return valorEstimado - taxaPagaCom - desconto
def taxa_servico(dados):
    #gera a taxa de servico
    return dados['Taxa de serviço bruta'].sum()
def taxa_transacao(dados):
    #gera a taxa de transacao
    return dados['Taxa de transação'].sum()   
def comissao_shopee(dados):
    return dados['Taxa de comissão bruta'].sum()
def custo(dados):
    #gera o valor do custo
    return dados['Custo total'].sum()
def insere_custo(dadosP, dadosCusto):
    '''utiliza dos dados dos pedidos e procura entre os valores do custo o custo
    daquele produto pedido'''
    '''(dados de pedidos, dados de custo) -> um Series com os valores de cada um dos 
    custos identificados através da relação de nome de anuncio'''
    linhas = dadosP.shape[0]
    custo = []
    for i in range(0,linhas):
        nome_produto = dadosP.loc[i,'Nome do Produto']
        indices = list(dadosCusto[dadosCusto['Nome do Anúncio'] == nome_produto].index)
        if len(indices) == 0:
            custo.append(0)
        if len(indices) > 0:
            custo.append(dadosCusto.loc[indices[0],'Custo Médio'])
    return custo
#_______________main____________________
def main():
    # Nome dos bancos de dados, precisamos de quatro bancos
    # 1° dados dos pedidos feitos no ultimo mês
    # 2° dados dos custos que tivemos no mês
    # 3° dados de SKU, a relação existentes
    # 4° dados de ID considerados anteriormente
    #nome_pedidos = str(input())
    #nome_custo = str(input())
    #nomeSKU = str(input())
    #nome_ID = str(input())
    #dados de pedidos
    dadosDePedidos =  pd.read_excel(f"Order_all.xlsx")
    #dados de custo
    dadosDeCusto = pd.read_excel(f"Export_Order_eletronico.xlsx")
    #dados de SKU2SKU Armazem
    dadosSKU2SKUA = pd.read_excel(f"SKU2SKUArmazem.xlsx")
    #dados de ID Considerados
    dadosIdConsiderados = pd.read_excel(f"ID_anterior_considerado.xlsx") 
    #filtro das colunas que desejamos
    dadosFiltrados = pd.DataFrame(data = {'ID do pedido':dadosDePedidos['ID do pedido'].astype(str),\
                                          'Status do pedido':dadosDePedidos['Status do pedido'].astype(str),\
                                          'Nome do Produto':dadosDePedidos['Nome do Produto'].astype(str),\
                                          'Número de referência SKU':dadosDePedidos['Número de referência SKU'],\
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
                                                'Nome do Anúncio':dadosDeCusto['Nome do Anúncio'].astype(str),\
                                                'SKU (Armazém)':dadosDeCusto['SKU (Armazém)'].astype(str),\
                                                'Custo Médio':dadosDeCusto['Custo Médio'].astype(float)})
    
    #inserção dos custos no conjunto de dados de pedidos
    custos = insere_custo(dadosFiltrados, dadosFiltrados_custo)
    dadosFiltrados["Custo Unitário"] = custos
    dadosFiltrados["Custo total"] = dadosFiltrados['Quantidade'] * dadosFiltrados["Custo Unitário"]
    #filtramos os pedidos que estão cancelados.
    dadosFiltrados = dadosFiltrados[dadosFiltrados['Status do pedido'] != 'Cancelado']
    #resetamos os indices para possiveis interações
    dadosFiltrados_reset = dadosFiltrados.reset_index()
    #retiramos a coluna com os indices anteriores
    dadosFiltradosNovos  = dadosFiltrados_reset.drop("index", axis = 1)
    
    #____________________________________Bloco calculo dos valores copnsiderados na ultima finalizacao______________________________________________
    verifica_ID = dados_para_analise(dadosFiltradosNovos)
    nao_existem = dadosIdConsiderados.loc[~dadosIdConsiderados["ID do pedido (anterior)"].isin(verifica_ID["ID do pedido"]),\
        "ID do pedido (anterior)"]
    #base com os dados a mais que desejamos.
    baseAmais = dadosFiltrados[dadosFiltrados['ID do pedido'].isin(nao_existem)]
    #criação dos bancos que precisamos
    duplicaAmais = banco_duplicado(baseAmais)
    semduplicaAmais = banco_sem_duplas(baseAmais)
    first_aparicao = primeiros_duplicado(baseAmais)
    #receita anterior
    receita_ant = receita(baseAmais)
    #imposto anterior contabilizado
    imposto_ant = receita_ant*0.1*0.0924
    #custo anterior considerado
    custoAntFinal = custo(baseAmais)
    #calculo da comissão da shopee dos duplicados e sem duplicar
    comissaoAntFinal = comissao_shopee(semduplicaAmais) + comissao_shopee(first_aparicao)
    #Taxa de Transação dos duplicados e sem duplicar
    taxaTransacaoAntFinal = taxa_transacao(semduplicaAmais) + taxa_transacao(first_aparicao)
    #Taxa de Serviço dos duplicados e sem duplicar
    taxaDeServicoAntFinal = taxa_servico(semduplicaAmais) + taxa_servico(first_aparicao)
    #Valor do Frete dos duplicados e sem duplicar
    freteAntFinal =  frete(semduplicaAmais) + frete(first_aparicao)

    #____________________________________Bloco para calculo dos valores que estão mais atuais_______________________________________________________
    duplicados = banco_duplicado(dadosFiltradosNovos) #Esse devemos ter um olhar um pouco mais critico.
    semDuplicatas = banco_sem_duplas(dadosFiltradosNovos) #Esse data frame contem os elementos não duplicados 
    dataAnalise = dados_para_analise(semDuplicatas)
    #analise dos duplicados
    dataAnalise_Dupli = dados_para_analise(duplicados)
    calculo_taxa_repe = primeiros_duplicado(dataAnalise_Dupli)
    #calculo da receita
    valor_receita = receita(dataAnalise) + receita(dataAnalise_Dupli)
    #Calculo dos Impostos
    imposto = valor_receita*0.1*0.0924
    #calculo da comissão da shopee
    comissaoShopee = comissao_shopee(dataAnalise) + comissao_shopee(calculo_taxa_repe)
    #Taxa de Transação
    taxaTransacao = taxa_transacao(dataAnalise) + taxa_transacao(calculo_taxa_repe)
    #Taxa de Serviço
    taxaServico = taxa_servico(dataAnalise) + taxa_servico(calculo_taxa_repe)
    #Valor do Frete
    valor_frete = frete(dataAnalise) + frete(calculo_taxa_repe)
    #Custo
    valor_custo = custo(dataAnalise) + custo(dataAnalise_Dupli)
    
    #____________________________________Escrita dos arquivos de verificação externa________________________________________________________________
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
    print('Os valores acima devem ser corrigidos')
    print('--------------------------------------------')
    print('Fechamento final atual')
    print('--------------------------------------------')
    print(f'Receita____________________________ {valor_receita:<15.2f}')
    print(f'Impostsos__________________________ {imposto:<15.2f}')
    print(f'Frete______________________________ {valor_frete:<15.2f}')
    print(f'Custo total________________________ {valor_custo:<15.2f}')
    print(f'Comissão Shopee____________________ {comissaoShopee:<15.2f}')
    print(f'Taxas de Transação_________________ {taxaTransacao:<15.2f}')
    print(f'Taxa de Serviços da shopee_________ {taxaServico:<15.2f}')
    print('--------------------------------------------')
    
if __name__ == "__main__":
    main()