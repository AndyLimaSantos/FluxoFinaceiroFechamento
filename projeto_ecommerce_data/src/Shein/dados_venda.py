import pandas as pd
from datetime import datetime

###################################### Funcoes quwe utilizam das planilhas apenas ######################################
def estimativa_taxa(dataPedidos):
    return pd.DataFrame(data = {"Estimativa de Taxa": (dataPedidos["Comissão"]+\
                                                       dataPedidos["Taxa de intermediação de frete"]+\
                                                       dataPedidos["Taxa de operação de estocagem"])})
def statusPedidos(dataPedidos,income): # verificar isso aqui, necessário pois parece incoerente
    linha = dataPedidos.shape[0]
    status = []
    for i in range(0,linha):
        pedido = dataPedidos.loc[i,'Número do pedido']
        situ = dataPedidos.loc[i,"Status do pedido"]
        presenca = len(list(income[income['Número do pedido_i']==pedido].index))
        if situ == "Cancelado":
            status.append("Cancelado")
        elif dataPedidos.loc[i,"Preço do produto"] == 0 and situ != "Cancelado":
            status.append("Amostra")
        elif presenca == 0:
            status.append("A Depositar")
        elif presenca > 0:
            status.append("Depositado")
    return pd.DataFrame(data = {"Status":status})

def custoUnitario(dataPedidos):    #Ja tem na planilha de todos os pedidos como Custo Médio
    return pd.DataFrame(data = {"Custo unitário":dataPedidos["Custo Médio"]})

def valor_real_depositado(dataPedidos):    #Ja tem na planilha de todos os pedidos como Receita estimada de mercadorias
    return pd.DataFrame(data = {"Valor real depositado":dataPedidos["Receita estimada de mercadorias"]})

def data_deposito(dataPedidos):            #Já tem ná planilha de todos os pedidos como data de pagamento
    return pd.DataFrame(data = {"Data de deposito":dataPedidos["Data de pagamento"]})

def estimativaRecebimento(dataPedidos):
    return  pd.DataFrame(data = {"Estimativa de Recebimento": dataPedidos["Preço do produto"]-\
                                                             (dataPedidos["Comissão"]+\
                                                              dataPedidos["Valor do cupom"]+\
                                                              dataPedidos["Desconto de campanha da loja"]+\
                                                              dataPedidos["Taxa de intermediação de frete"]+\
                                                              dataPedidos["Taxa de operação de estocagem"])})
def receita(dataPedidos):
    return  pd.DataFrame(data = {"Receita": dataPedidos["Preço do produto"]-\
                                                              (dataPedidos["Valor do cupom"]+\
                                                              dataPedidos["Desconto de campanha da loja"])})

#########################################Funcoes que usan de dados anterirores#########################################

def diferenca(valor_real, estima_recebe):
    return pd.DataFrame(data = {"Diferença":(valor_real["Valor real depositado"]\
                                             - estima_recebe["Estimativa de Recebimento"])})

def lucro_bruto_real(valor_real, custo_tot):
    lucro = pd.DataFrame(data = {"Lucro Bruto Real":(valor_real["Valor real depositado"]-custo_tot["Custo Total"])})
    return lucro

def lucro_estimado(estima_recebe, custo_tot):
    return pd.DataFrame(data = {"Lucro Estimado":(estima_recebe["Estimativa de Recebimento"]\
                                                  - custo_tot["Custo Total"])})

def margemDeLucro(lucro, dataPedidos):
    return pd.DataFrame(data = {"Margem de Lucro":(lucro["Lucro Estimado"]/ dataPedidos["Preço do produto"])})

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

def data_devolucao(todos_pedidos):  ## aqui é uma gambiarra feita para suportar os 3 meses de contas. Corrigir depois
    return pd.DataFrame(data = {"Data de Devolução":todos_pedidos["Data de devolução"]})

def frete_pago(dataPedidos):
    return pd.DataFrame(data = {"Frete":dataPedidos["Taxa de intermediação de frete"]})

def custo_total(dataPedidos):         #Não temos colunas de quantidades para calculo de custo total.
    return pd.DataFrame(data = {"Custo Total":dataPedidos["Custo Médio"]})

def main():
    #importacao das planilhas.
    custoUp = pd.read_csv("custoUP.csv").drop("Unnamed: 0", axis =1)
    income = pd.read_csv("income.csv").drop("Unnamed: 0", axis =1)
    todosPedidos = pd.read_csv("todospedidos.csv").drop("Unnamed: 0", axis =1)
    devolucoes = pd.read_csv("devolucoes.csv").drop("Unnamed: 0", axis =1)

    #Calculo das colunas que desejamos
    Vreceita = receita(todosPedidos)
    estima_taxa = estimativa_taxa(todosPedidos)
    custo_uni = custoUnitario(todosPedidos)
    status = statusPedidos(todosPedidos, income) 
    valor_real = valor_real_depositado(todosPedidos)
    dataDeposito = data_deposito(todosPedidos)
    estima_recebe = estimativaRecebimento(todosPedidos)
    difere = diferenca(valor_real, estima_recebe) 
    custo_tot = custo_total(todosPedidos)
    lucro_bruto = lucro_bruto_real(valor_real, custo_tot)
    lucro_estima = lucro_estimado(estima_recebe, custo_tot)
    margem = margemDeLucro(lucro_estima,todosPedidos)
    mes = mes_recebimento(dataDeposito)
    Vdevolucoes = data_devolucao(todosPedidos)
    frete = frete_pago(todosPedidos)

    Dados_vendas_final = pd.DataFrame(data = {  "Order ID":todosPedidos["Número do pedido"].astype(str),\
                                                "Receita":Vreceita["Receita"],\
                                                "Estimativa de Recebimento":estima_recebe["Estimativa de Recebimento"].astype(float).round(2),\
                                                "Custo Unitário":custo_uni["Custo unitário"].astype(float).round(2),\
                                                "Frete":frete["Frete"].astype(float).round(2),\
                                                "Lucro Estimado":lucro_estima["Lucro Estimado"].astype(float).round(2),\
                                                "Status":status["Status"],\
                                                "Valor Real Depositado":valor_real["Valor real depositado"].astype(float).round(2),\
                                                "Custo Total":custo_tot["Custo Total"].astype(float).round(2),\
                                                "Lucro Bruto Real":lucro_bruto["Lucro Bruto Real"].astype(float).round(2),\
                                                "Margem de Lucro":margem["Margem de Lucro"].astype(float).round(2),\
                                                "Diferênça":difere["Diferença"].astype(float).round(2),\
                                                "Data De Deposito":dataDeposito["Data de deposito"],\
                                                "Mês de Recebimento":mes["Mês de recebimento"],\
                                                "Data de Devolução":Vdevolucoes["Data de Devolução"],\
                                                'Taxa de comissão bruta':todosPedidos['Comissão'].astype(float).round(2),\
                                                'Taxa de intermediação de frete':todosPedidos['Taxa de intermediação de frete'].astype(float).round(2),\
                                                'Taxa de operação de estocagem':todosPedidos['Taxa de operação de estocagem'].astype(float).round(2),\
                                                'Valor do cupom':todosPedidos['Valor do cupom'].astype(float).round(2),\
                                                'Desconto de campanha da loja':todosPedidos['Desconto de campanha da loja'].astype(float).round(2),\
                                                "Estimativa de Taxa":estima_taxa["Estimativa de Taxa"].astype(float).round(2)
                                                })
    Dados_vendas_final.to_excel("Dados_venda_final.xlsx")
    Dados_vendas_final.to_csv("Dados_venda_final.csv")

    return
if __name__ == "__main__":
    main()