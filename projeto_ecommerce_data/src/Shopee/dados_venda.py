#importação das bibliotecas
import pandas as pd
from datetime import datetime

#Funaoes que iremos utilizar para criacao das novas colunas.

#####################################sao as funcoes que utiliza das planilhas de base apenas###############################
def estimativa_taxa(todos_pedidos): #############################Essa taxa não me parece estar correta###############################
    return pd.DataFrame(data = {"Estimativa de Taxa":(todos_pedidos['Desconto de Frete Aproximado']-\
                                                             todos_pedidos['Taxa de transação']-\
                                                             todos_pedidos['Taxa de comissão bruta']-\
                                                             todos_pedidos['Taxa de serviço bruta']-\
                                                             todos_pedidos['Valor estimado do frete']-\
                                                             todos_pedidos['Coin Cashback Voucher Amount Sponsored by Seller'])})
def custo_unitario(todos_pedidos, custo_up): ### usa as planilhas ##########################Feito###############################
    #ele não enontra alguns valores no custo UP, acredito que seja pq o custo UP não esta pegando todos os pedidos.
    #as datas de criação não esta no dentro do intervalo do sdadoa do upseller
    #Mas esta correto
    custo_unitario=[]
    n_linhas = todos_pedidos.shape[0]
    for i in range(0, n_linhas):
        pedido = todos_pedidos.loc[i,'ID do pedido']
        sku_venda = todos_pedidos.loc[i,"Número de referência SKU"]
        indice_local = list(custo_up[custo_up["Nº de Pedido da Plataforma"] == pedido].index)
        if len(indice_local) > 0:
            elementos = {}
            for k in range(len(indice_local)):
                produto = custo_up.loc[indice_local[k],"SKU"]
                elementos[produto] = custo_up.loc[indice_local[k],"Custo Médio"]
            custo_unitario.append(elementos[produto])
        else:
            custo_unitario.append(0)
    return pd.DataFrame(data = {"Custo Unitario":custo_unitario})  
def status_pedidos(todos_pedidos, income):  #usa as tabelas   ########Feito##########
    linha = todos_pedidos.shape[0]
    status = []
    for i in range(0,linha):
        pedido = todos_pedidos.loc[i,'ID do pedido']
        situ = todos_pedidos.loc[i,"Status do pedido"]
        presenca = len(list(income[income['Order ID']==pedido].index))
        if situ == "Cancelado":
            status.append("Cancelado")
        elif todos_pedidos.loc[i,"Preço original"] == 0 and situ != "Cancelado":
            status.append("Amostra")
        elif presenca == 0:
            status.append("A Depositar")
        elif presenca > 0:
            status.append("Depositado")
    return pd.DataFrame(data = {"Status":status})
def valor_real_depositado(todos_pedidos, income):  #usa as tabelas   ########Feito##########
    valor_real = []
    n_linhas =todos_pedidos.shape[0]
    for i in range(0, n_linhas):
        pedido = todos_pedidos.loc[i,"ID do pedido"]
        indices = list(income[income["Order ID"] == pedido].index)
        if len(indices) > 0:
            valor = income.loc[indices[0],'Total Released Amount (R$)']
            valor_real.append(valor)
        else:
            valor_real.append(0)
    return pd.DataFrame(data = {"Valor Real Depositado":valor_real})
def data_deposito(todos_pedidos, income):  #usa as tabelas  ########Feito##########
    linhas = todos_pedidos.shape[0]
    data_deposito = []
    for  i in range(0, linhas):
        pedidos = todos_pedidos.loc[i,"ID do pedido"]
        indices = list(income[income["Order ID"] == \
            pedidos].index)
        if len(indices) == 0:
            data_deposito.append("A depositar")
        elif len(indices) > 0:
            data  = income.loc[indices[0],'Payout Completed Date']
            data_deposito.append(data)
    return pd.DataFrame(data = {"Data de deposito": data_deposito})


################sao as funcoes que utiliza das planilhas de base e dos valores criados com outras funcoes#####################
def estimativa_recebimento(todos_pedidos):
    return pd.DataFrame(data  = {"Estimativa de Recebimento":todos_pedidos['Subtotal do produto']-\
                                                             todos_pedidos['Cupom do vendedor']+\
                                                             todos_pedidos['Taxa de envio pagas pelo comprador']+\
                                                             todos_pedidos['Desconto de Frete Aproximado']-\
                                                             todos_pedidos['Taxa de transação']-\
                                                             todos_pedidos['Taxa de comissão bruta']-\
                                                             todos_pedidos['Taxa de serviço bruta']-\
                                                             todos_pedidos['Valor estimado do frete']-\
                                                             todos_pedidos['Coin Cashback Voucher Amount Sponsored by Seller']})
def diferenca(valor_real, estima_recebe):
    return pd.DataFrame(data = {"Diferença":(valor_real["Valor Real Depositado"]\
                                             - estima_recebe["Estimativa de Recebimento"])})
def custo_total(todos_pedidos, custo_unit):
    return pd.DataFrame(data = {"Custo Total":(custo_unit["Custo Unitario"]*todos_pedidos['Quantidade'])})
def lucro_bruto_real(valor_real, custo_total):
    lucro = pd.DataFrame(data = {"Lucro Bruto Real":(valor_real["Valor Real Depositado"]-custo_total["Custo Total"])})
    lucro[lucro["Lucro Bruto Real"]<0] = 0
    return lucro
def margem_de_lucro(todos_pedidos, lucro_bruto,estima_taxa):
    return pd.DataFrame(data = {"Margem de Lucro":(lucro_bruto["Lucro Bruto Real"]/\
                                                   (todos_pedidos['Preço original']-\
                                                   todos_pedidos['Desconto do vendedor']-\
                                                   estima_taxa["Estimativa de Taxa"]))})
def lucro_estimado(estima_recebe, custo_tot):
    return pd.DataFrame(data = {"Lucro Estimado":(estima_recebe["Estimativa de Recebimento"]\
                                                  - custo_tot["Custo Total"])})
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
        sku_return = todos_pedidos.loc[i, 'Returned quantity']
        order_id = todos_pedidos.loc[i, "ID do pedido"]
        indices = list(devolucao[devolucao['Order ID'] == order_id].index)
        if sku_return > 0:
            data_devolucao.append("Devolução no mesmo mês")
        elif len(indices) > 0 and sku_return == 0:
            data_devolve = devolucao.loc[indices[0], 'Payout Completed Date']
            data_devolucao.append(data_devolve)
        elif len(indices) == 0 and sku_return == 0:
            data_devolucao.append("Não devolvido")
    return pd.DataFrame(data = {"Data de Devolução":data_devolucao})
def frete_pago(todos_pedidos):
    return pd.DataFrame(data = {"Frete":(todos_pedidos["Valor estimado do frete"]-todos_pedidos["Taxa de envio pagas pelo comprador"]-todos_pedidos["Desconto de Frete Aproximado"])})

def main():
    income = pd.read_csv("income.csv")
    custoUP = pd.read_csv("custoUP.csv")
    totalPedidos = pd.read_csv("todosPedidos.csv")
    devolucao = pd.read_csv("devolucoes.csv")
    
    #todos aqui foram verificados.
    estima_taxa = estimativa_taxa(totalPedidos)
    custo_uni = custo_unitario(totalPedidos, custoUP) #---- Ainda devolve algumas celulas sem valor
    status = status_pedidos(totalPedidos, income) 
    valor_real = valor_real_depositado(totalPedidos, income)
    dataDeposito = data_deposito(totalPedidos, income)
    #todos aqui foram verificados.
    estima_recebe = estimativa_recebimento(totalPedidos) #
    difere = diferenca(valor_real, estima_recebe)
    custo_tot = custo_total(totalPedidos, custo_uni)
    #todos aqui foram verificados.
    lucro_bruto = lucro_bruto_real(valor_real, custo_tot)
    margem = margem_de_lucro(totalPedidos, lucro_bruto, estima_taxa)
    lucro_estima = lucro_estimado(estima_recebe, custo_tot)
    #todos aqui foram verificados.
    mes = mes_recebimento(dataDeposito)
    devolucoes = data_devolucao(totalPedidos, devolucao)
    frete = frete_pago(totalPedidos)

    Dados_vendas_final = pd.DataFrame(data = {"Order ID":totalPedidos["ID do pedido"].astype(str),\
                                            "SKU Subtotal After Discount":(totalPedidos["Subtotal do produto"]).astype(float),\
                                            "Estimativa de Recebimento":estima_recebe["Estimativa de Recebimento"].astype(float),\
                                            "Custo Unitário":custo_uni["Custo Unitario"].astype(float),\
                                            "Frete":frete["Frete"].astype(float),\
                                            "Lucro Estimado":lucro_estima["Lucro Estimado"].astype(float),\
                                            "Status":status["Status"],\
                                            "Valor Real Depositado":valor_real["Valor Real Depositado"].astype(float),\
                                            "Custo Total":custo_tot["Custo Total"].astype(float),\
                                            "Lucro Bruto Real":lucro_bruto["Lucro Bruto Real"].astype(float),\
                                            "Margem de Lucro":margem["Margem de Lucro"].astype(float),\
                                            "Diferênça":difere["Diferença"].astype(float),\
                                            "Data De Deposito":dataDeposito["Data de deposito"],\
                                            "Mês de Recebimento":mes["Mês de recebimento"],\
                                            "Data de Devolução":devolucoes["Data de Devolução"],\
                                            'Taxa de comissão bruta':totalPedidos['Taxa de comissão bruta'].astype(float),\
                                            'Taxa de serviço bruta':totalPedidos['Taxa de serviço bruta'].astype(float),\
                                            'Taxa de Envio Reversa':totalPedidos['Taxa de Envio Reversa'].astype(float),\
                                            'Taxa de transação':totalPedidos['Taxa de transação'].astype(float),\
                                            "Estimativa de Taxa":estima_taxa["Estimativa de Taxa"].astype(float)
                                            })
    Dados_vendas_final.to_excel("Dados_venda_final.xlsx")
    Dados_vendas_final.to_csv("Dados_venda_final.csv")
    return

if __name__ == "__main__":
    main()