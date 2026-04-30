import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

def corrige_devolucao(pedido):
    lista = list(pedido[pedido["Status do pedido"] == 'Reembolsado por cliente'].index)
    for i in range(len(lista)):
        if pedido.loc[lista[i],"Data de devolução"] == "Não devolvido":
            pedido.loc[lista[i],"Data de devolução"] = "Devolução pendente"
    return pedido

def main():
    print("Insira o nome do arquivo de Pedidos")
    nome_pedidos = str(input())
    print("Insira o nome do arquivo de income")
    nome_income = str(input())
    print("Insira o nome do arquivo de custo")
    nome_custo = str(input())
    print("Insira o nome do arquivo de Reembolso")
    nome_reembolso = str(input())
    #-------------------------Custo e todos os pedidos-------------------------------
    todosPedidos = pd.read_excel(nome_pedidos, header=1)
    custo_base = pd.read_excel(nome_custo)
    reembolso = pd.read_excel("Reembolso.xlsx")
    custo = custo_base[custo_base["SKU"].duplicated() == False].reset_index()

    #-----------------------------------Income---------------------------------------
    income = pd.read_excel(nome_income, header=1)
    income['Data de pagamento'] = income['Data de pagamento'].str.split(" ")
    income['Data de pagamento'] = income['Data de pagamento'].str[0]
    income = income[income["Número do pedido"].duplicated() == False]

    #-----------------------------------Reembolso-------------------------------------
    reembolso = pd.read_excel(nome_reembolso)
    reembolso['Data de pagamento'] = reembolso['Tempo de aplicação pós-venda'].str.split(" ")
    reembolso['Data de pagamento'] = reembolso['Data de pagamento'].str[0]
    reembolso = reembolso[reembolso["Número do pedido"].duplicated() == False]


    #criacao da nova planilha de devolução é por ela que iremos colocar os valores de devolução e reembolso.
    data_reembolso = pd.DataFrame(data = {"Solução pós-venda":reembolso['Solução pós-venda'].fillna(value = "Não definido").astype(str),\
                                        "SKU do vendedor":reembolso['SKU do vendedor'].astype(str),\
                                        "Número do pedido_d":reembolso['Número do pedido'].astype(str),\
                                        "Data de devolução":reembolso['Data de pagamento'].astype(str),\
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

    #----------------------Mesclagem de algumas colunas de maneira a deixar melhor ---------------------
    data_analise_reembolso = data_reembolso.merge(data_custo, how = "left", left_on = "SKU do vendedor",\
                                                   right_on = "SKU" ).drop("SKU", axis =1) #feito a planilha de reembolso corretamente.
    
    data_analise_pedidos = data_todosPedidos.merge(data_custo, how = "left", left_on = "SKU do vendedor",\
                                                    right_on = "SKU" ).drop("SKU", axis =1) #feito a planilha de pedidos sem a data
    
    #Inserção da coluna de data de deposito
    data_analise_pedidos = data_analise_pedidos.merge(data_income[["Número do pedido_i", 'Data de pagamento']],\
                                                       how = "left", left_on = "Número do pedido",\
                                                       right_on = "Número do pedido_i").drop("Número do pedido_i", axis =1)
    
    #Inserção da coluna de data de devolução
    data_analise_pedidos = data_analise_pedidos.merge(data_reembolso[["Número do pedido_d", "Data de devolução"]],\
                                                       how = "left", left_on = "Número do pedido",\
                                                       right_on = "Número do pedido_d").drop("Número do pedido_d", axis =1)
    
    data_analise_pedidos["Data de pagamento"] = data_analise_pedidos["Data de pagamento"].fillna(value = "A depositar") # todos os pedidos com a data

    data_analise_pedidos["Data de devolução"] = data_analise_pedidos["Data de devolução"].fillna(value = "Não devolvido") # todos os pedidos com a data

    data_analise_pedidos = corrige_devolucao(data_analise_pedidos) #correção das devoluções
    #Exportação das planilhas par analise
    #------------------------------------ CSV -------------------------------
    data_analise_reembolso.to_csv("devolucoes.csv")
    data_analise_pedidos.to_csv("todospedidos.csv")
    data_income.to_csv("income.csv")
    data_custo.to_csv("custoUP.csv")

if __name__ == "__main__":
    main()
