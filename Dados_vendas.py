'''
Esse script tem como funçõa a criação do banco de dados que iremos utilizar para executar os 
calculos do resumo, 
'''
#Importação das nossas bibliotecas utilizadas no processo
import pandas as pd
from datetime import datetime

#Funções que iremos utilizar para criação das novas colunas.
def estimativa_taxa(todos_pedidos):
    return pd.DataFrame(data = {"Estimativa de Taxa":(todos_pedidos['SKU Subtotal After Discount']\
                                                       *(0.22))*todos_pedidos['Quantity']})
def estimativa_recebimento(todos_pedidos, estima_taxa):
    return pd.DataFrame(data  = {"Estimativa de Recebimento":todos_pedidos['SKU Subtotal After Discount'] - \
                                        estima_taxa["Estimativa de Taxa"]})
def diferenca(valor_real, estima_recebe):
    return pd.DataFrame(data = {"Diferença":(valor_real["Valor Real Depositado"]\
                                             - estima_recebe["Estimativa de Recebimento"])})
def custo_total(todos_pedidos, custo_unit):
    return pd.DataFrame(data = {"Custo Total":(custo_unit["Custo Unitario"]*todos_pedidos['Quantity'])})
def lucro_bruto_real(valor_real, custo_total):
    lucro = pd.DataFrame(data = {"Lucro Bruto Real":(valor_real["Valor Real Depositado"]-custo_total["Custo Total"])})
    lucro[lucro["Lucro Bruto Real"]<0] = 0
    return lucro
def margem_de_lucro(todos_pedidos, lucro_bruto):
    return pd.DataFrame(data = {"Margem de Lucro":(lucro_bruto["Lucro Bruto Real"]/todos_pedidos['SKU Subtotal Before Discount'])})
def correção_estima_taxa(todos_pedidos): #Só para construção do resumo.
    numero_pedidos = data_todospedidos["Package ID"].nunique() - 1
    taxa_por_pedido =  numero_pedidos*4
    return taxa_por_pedido
def lucro_estimado(estima_recebe, custo_uni):
    return pd.DataFrame(data = {"Lucro Estimado":(estima_recebe["Estimativa de Recebimento"]\
                                                  - custo_uni["Custo Unitario"])})
def custo_unitario(todos_pedidos, custo_up):
    #ele não enontra alguns valores no custo UP, acredito que seja pq o custo UP não esta pegando todos os pedidos.
    #as datas de criação não esta no dentro do intervalo do sdadoa do upseller
    #Mas esta correto
    custo_unitario=[]
    n_linhas = todos_pedidos.shape[0]
    for i in range(0, n_linhas):
        pedido = todos_pedidos.loc[i,'Order ID']
        sku_venda = todos_pedidos.loc[i,"Seller SKU"]
        indice_local = list(custo_up[custo_up["Nº de Pedido da Plataforma"] == pedido].index)
        if len(indice_local) > 0:
            elementos = {}
            for k in range(len(indice_local)):
                produto = custo_up.loc[indice_local[k],"SKU"]
                elementos[produto] = custo_up.loc[indice_local[k],"Custo Médio"]
            custo_unitario.append(elementos[sku_venda])
        else:
            custo_unitario.append(0)
    return pd.DataFrame(data = {"Custo Unitario":custo_unitario}) 
def status_pedidos(todos_pedidos, income):
    linha = todos_pedidos.shape[0]
    status = []
    for i in range(0,linha):
        pedido = todos_pedidos.loc[i,"Order ID"]
        situ = todos_pedidos.loc[i,"Package ID"]
        presenca = len(list(income[income['ID do pedido/ajuste']==pedido].index))
        if situ == "Cancelado":
            status.append("Cancelado")
        elif todos_pedidos.loc[i,"SKU Unit Original Price"] == 0 and situ != "Cancelado":
            status.append("Amostra")
        elif presenca == 0:
            status.append("A Depositar")
        elif presenca > 0:
            status.append("Depositado")
    return pd.DataFrame(data = {"Status":status})
def valor_real_depositado(todos_pedidos, income):
    valor_real = []
    n_linhas =todos_pedidos.shape[0]
    for i in range(0, n_linhas):
        pedido = todos_pedidos.loc[i,"Order ID"]
        indices = list(income[income['ID do pedido/ajuste'] == pedido].index)
        if len(indices) > 0:
            valor = income.loc[indices[0],'Valor total a ser liquidado']
            valor_real.append(valor)
        else:
            valor_real.append(0)
    return pd.DataFrame(data = {"Valor Real Depositado":valor_real})
def data_deposito(todos_pedidos, income):
    linhas = todos_pedidos.shape[0]
    data_deposito = []
    for  i in range(0, linhas):
        pedidos = todos_pedidos.loc[i,"Order ID"]
        indices = list(income[income['ID do pedido/ajuste'] == \
            pedidos].index)
        if len(indices) == 0:
            data_deposito.append("A depositar")
        elif len(indices) > 0:
            data  = income.loc[indices[0],'Data do demonstrativo']
            data_deposito.append(data)
    return pd.DataFrame(data = {"Data de deposito": data_deposito})
def mes_recebimento(data_deposito):
    linhas = data_deposito.shape[0]
    meses = []
    for i in range(0, linhas):
        d = data_deposito.loc[i, "Data de deposito"]
        if d != "A depositar":
            data_convert = datetime.strptime(d.replace("/","-"), "%Y-%m-%d").date()
            mes_numero = int(data_convert.month)
            meses.append(mes_numero)
        if d == "A depositar":
            meses.append(0)
    return pd.DataFrame(data = {"Mês de recebimento":meses})
def data_devolucao(todos_pedidos, devolucao):
    linhas = todos_pedidos.shape[0]
    data_devolucao = []
    for i in range(0, linhas):
        sku_return = todos_pedidos.loc[i, 'Sku Quantity of return']
        order_id = todos_pedidos.loc[i, "Order ID"]
        indices = list(devolucao[devolucao['ID do pedido/ajuste'] == order_id].index)
        if sku_return > 0:
            data_devolucao.append("Devolução no mesmo mês")
        elif len(indices) > 0 and sku_return == 0:
            data_devolve = devolucao.loc[indices[0], 'Data do demonstrativo']
            data_devolucao.append(data_devolve)
        elif len(indices) == 0 and sku_return == 0:
            data_devolucao.append("Não devolvido")
    return pd.DataFrame(data = {"Data de Devolução":data_devolucao})

#Importação dos banco de dados criados para tratamento.
data_todospedidos = pd.read_csv("todosPedidos.csv").drop("Unnamed: 0", axis = 1)
data_CustoUP = pd.read_csv("CustoUP_final.csv").drop("Unnamed: 0", axis = 1)
data_income = pd.read_csv("income.csv").drop("Unnamed: 0", axis = 1)
data_devolucoes = pd.read_csv("devolucoes.csv").drop("Unnamed: 0", axis = 1)

#Aplicação do main, para execução das tarefas
def main():
    estimaTaxa = estimativa_taxa(data_todospedidos)
    estimaRecebe = estimativa_recebimento(data_todospedidos, estimaTaxa)
    custoUni=custo_unitario(data_todospedidos,data_CustoUP)
    lucro_estima = lucro_estimado(estimaRecebe, custoUni)
    status = status_pedidos(data_todospedidos, data_income)
    valorRealLiquidado = valor_real_depositado(data_todospedidos, data_income)
    custoTot = custo_total(data_todospedidos, custoUni)
    valorLucro = lucro_bruto_real(valorRealLiquidado,custoTot)
    lucroMargem = margem_de_lucro(data_todospedidos,valorLucro)
    diferença = diferenca(valorRealLiquidado , estimaRecebe)
    dataDeposito = data_deposito(data_todospedidos, data_income)
    mesRecebimento = mes_recebimento(dataDeposito)
    dataDevolucao = data_devolucao(data_todospedidos, data_devolucoes)
    #Produção do novo banco de dados com os indicadores que precisamos, 
    #para fazer o resumo que desejamos
    Dados_vendas_final = pd.DataFrame(data = {"Order ID":data_todospedidos["Order ID"].astype(str),\
                                            "Package ID":data_todospedidos["Package ID"].astype(str),\
                                            "SKU Subtotal After Discount":data_todospedidos["SKU Subtotal After Discount"],\
                                            "Estimativa de Taxa":estima_taxa["Estimativa de Taxa"],\
                                            "Estimativa de Recebimento":estima_recebe["Estimativa de Recebimento"],\
                                            "Custo Unitário":custo_uni["Custo Unitario"],\
                                            "Lucro Estimado":lucro_estima["Lucro Estimado"],\
                                            "Status":status["Status"],\
                                            "Valor Real Depositado":valor_real_liquidado["Valor Real Depositado"],\
                                            "Custo Total":custo_tot["Custo Total"],\
                                            "Lucro Bruto Real":valor_lucro["Lucro Bruto Real"],\
                                            "Margem de Lucro":lucro_margem["Margem de Lucro"],\
                                            "Diferênça":diferenca_valor["Diferença"],\
                                            "Data De Deposito":dataDeposito["Data de deposito"],\
                                            "Mês de Recebimento":mesRecebimento["Mês de recebimento"],\
                                            "Data de Devolução":dataDevolucao["Data de Devolução"]})
    #Dados_vendas_final.to_excel("Dados de venda Final.xlsx")
    Dados_vendas_final.to_csv("Dados de venda Final.csv")
if __name__ == "__main__":
    main()