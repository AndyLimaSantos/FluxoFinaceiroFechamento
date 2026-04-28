import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

todosPedidos = pd.read_excel("Exportar_pedidos.xlsx", header=1)
custo_base = pd.read_excel("Export_Order.xlsx")
reembolso = pd.read_excel("Reembolso.xlsx")
custo = custo_base[custo_base["SKU"].duplicated() == False].reset_index()

income = pd.read_excel("income.xlsx", header=1)
income['Data de pagamento'] = income['Data de pagamento'].str.split(" ")
income['Data de pagamento'] = income['Data de pagamento'].str[0]
income = income[income["Número do pedido"].duplicated() == False]

#criacao da nova planilha de devolução é por ela que iremos colocar os valores de devolução e reembolso.
data_reembolso = pd.DataFrame(data = {"Solução pós-venda":reembolso['Solução pós-venda'].fillna(value = "Não definido").astype(str),\
                                      "SKU do vendedor":reembolso['SKU do vendedor'].astype(str),\
                                      "Despesa prevista":reembolso['Despesa prevista'].astype(float)})
data_custo = pd.DataFrame(data = {"SKU":custo['SKU'].astype(str),\
                                  "Custo Médio":custo['Custo Médio'].astype(float).round(2)})

data_todosPedidos = pd.DataFrame(data = {'Número do pedido':todosPedidos['Número do pedido'].astype(str),\
                                         'SKU do vendedor':todosPedidos['SKU do vendedor'].astype(str),\
                                         'Status do pedido':todosPedidos['Status do pedido'].astype(str),\
                                         'Província':todosPedidos['Província'].astype(str),\
                                         'Preço do produto':todosPedidos['Preço do produto'].astype(float).round(2),\
                                         'Valor do cupom':todosPedidos['Valor do cupom'].astype(float).round(2),\
                                         'Desconto de campanha da loja':todosPedidos['Desconto de campanha da loja'].astype(float).round(2),\
                                         'Comissão':todosPedidos['Comissão'].astype(float).round(2),\
                                         'Taxa de intermediação de frete':todosPedidos['Taxa de intermediação de frete'].astype(float).round(2), \
                                         'Taxa de operação de estocagem':todosPedidos['Taxa de operação de estocagem'].astype(float).round(2),\
                                         'Receita estimada de mercadorias':todosPedidos['Receita estimada de mercadorias'].astype(float).round(2)})

data_income = pd.DataFrame(data = {'Número do pedido_i':income['Número do pedido'].astype(str),\
                                   'Data de pagamento':income['Data de pagamento'].astype(str),\
                                   'Valor a receber':income['Valor a receber'].astype(float).round(2)})

data_analise_reembolso = data_reembolso.merge(data_custo, how = "left", left_on = "SKU do vendedor", right_on = "SKU" ).drop("SKU", axis =1) #feito a planilha de reembolso corretamente.
data_analise_pedidos = data_todosPedidos.merge(data_custo, how = "left", left_on = "SKU do vendedor", right_on = "SKU" ).drop("SKU", axis =1) #feito a planilha de pedidos sem a data
data_analise_pedidos = data_analise_pedidos.merge(data_income[["Número do pedido_i", 'Data de pagamento']], how = "left", left_on = "Número do pedido",right_on = "Número do pedido_i").drop("Número do pedido_i", axis =1) #Inserção da coluna de data de deposito
data_analise_pedidos["Data de pagamento"] = data_analise_pedidos["Data de pagamento"].fillna(value = "A depositar") # todos os pedidos com a data

#Exportação das planilhas par analise
#------------------------------------ CSV -------------------------------
data_analise_reembolso.to_csv("devolucoes.csv")
data_analise_pedidos.to_csv("todospedidos.csv")
data_income.to_csv("income.csv")
data_custo.to_csv("custoUP.csv")

