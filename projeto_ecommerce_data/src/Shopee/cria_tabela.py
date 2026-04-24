# Importação das bibliotecas que queremos 
import pandas as pd
#Funcoes que precisamos utilizar para executar oque queremos 
#Importacao dos dados
print("Insira o nome do arquivo que contem todos os pedidos")
nome_pedidos = str(input())
todosPedidos_data = pd.read_excel(nome_pedidos)

print("Insira o nome do arquivo Income)
nome_income = str(input())
income_data = pd.read_excel(nome_income, header=2, sheet_name="Income") #Ele pega a aba Income e começa a pegar apenas os valores a partir da 3linha

print("Insira o nome do arquivo Export Order")
nome_ExportOrder = str(input())
exportOrder_data = pd.read_excel(nome_ExportOrder)
#criação do banco de dados para analisar
dadosFiltrados = pd.DataFrame(data = {'ID do pedido':todosPedidos_data['ID do pedido'].astype(str),\
                                      'Status do pedido':todosPedidos_data['Status do pedido'].astype(str),\
                                      'Nome do Produto':todosPedidos_data['Nome do Produto'].astype(str),\
                                      'Número de referência SKU':todosPedidos_data['Número de referência SKU'],\
                                      'Returned quantity':todosPedidos_data['Returned quantity'].astype(int),\
                                      'Subtotal do produto':todosPedidos_data['Subrtotal do produto'].astype(float),\
                                      'Preço original':todosPedidos_data['Preço original'].astype(float),\
                                      'Desconto do vendedor':todosPedidos_data['Desconto do vendedor'].astype(float),\
                                      'Cupom do vendedor':todosPedidos_data['Cupom do vendedor'].astype(float),\
                                      'Coin Cashback Voucher Amount Sponsored by Seller':todosPedidos_data['Coin Cashback Voucher Amount Sponsored by Seller'],\
                                      'Quantidade':todosPedidos_data['Quantidade'],\
                                      'Valor estimado do frete':todosPedidos_data['Valor estimado do frete'].astype(float),\
                                      'Taxa de envio pagas pelo comprador':todosPedidos_data['Taxa de envio pagas pelo comprador'].astype(float),\
                                      'Desconto de Frete Aproximado':todosPedidos_data['Desconto de Frete Aproximado'].astype(float),\
                                      'Taxa de transação':todosPedidos_data['Taxa de transação'].astype(float),\
                                      'Taxa de Envio Reversa':todosPedidos_data['Taxa de Envio Reversa'].astype(float),\
                                      'Taxa de comissão bruta':todosPedidos_data['Taxa de comissão bruta'].astype(float),\
                                      'Taxa de serviço bruta':todosPedidos_data['Taxa de serviço bruta'].astype(float)})
#Vamos verificar o income
dadosFiltroIncome = pd.DataFrame(data = {'Order ID':income_data['Order ID'],\
                                         'Total Released Amount (R$)':income_data['Total Released Amount (R$)'],\
                                         'Payout Completed Date':income_data['Payout Completed Date']} )
#Dados dos custo Up
dadosFiltroOrder = pd.DataFrame(data = {'Nº de Pedido da Plataforma':exportOrder_data['Nº de Pedido da Plataforma'],\
                                        'Estado do Pedido':exportOrder_data['Estado do Pedido'],\
                                        'Custo Médio':exportOrder_data['Custo Médio'],\
                                        'SKU':exportOrder_data['SKU'],\
                                        'SKU (Armazém)':exportOrder_data['SKU (Armazém)']})

devolucoes = dadosFiltroIncome[dadosFiltroIncome['Total Released Amount (R$)'] < 0]

#Exportacao de dados em arquivos csv
dadosFiltrados.to_csv("todosPedidos.csv")
dadosFiltroIncome.to_csv("income.csv")
dadosFiltroOrder.to_csv("custoUP.csv")
devolucoes.to_csv("devolucoes.csv")