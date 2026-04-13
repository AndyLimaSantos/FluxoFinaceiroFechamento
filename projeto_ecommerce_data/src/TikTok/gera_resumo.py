#importação das bibliotecas
import pandas as pd
#importação do banco de dados utilizado
data_vendas_final = pd.read_csv("Dados_venda_final.csv").drop("Unnamed: 0", axis = 1)
#data_vendas_anteriror = pd.read_csv("Dados_venda_final.csv").drop("Unnamed: 0", axis = 1)
#Funções que aplicaremos
#__________________________________________Receitas Obtidas____________________________________
def correção_estima_taxa(todos_pedidos): #Só para construção do resumo.
    numero_pedidos = data_todospedidos["Package ID"].nunique() - 1
    taxa_por_pedido =  numero_pedidos*4
    return taxa_por_pedido

def receita_vendas(data_vendas):
    separa_per_status = {separa_per_status: grupo for separa_per_status, grupo in data_vendas_final.groupby('Status')}
    depositado = separa_per_status["Depositado"]["SKU Subtotal After Discount"].sum()
    aDepositar = separa_per_status["A Depositar"]["SKU Subtotal After Discount"].sum()
    valor = float(depositado+aDepositar)
    return valor

def comissao_tk(data_vendas):
    separa_per_status = {separa_per_status: grupo for separa_per_status, grupo in data_vendas_final.groupby('Status')}
    depositado = separa_per_status["Depositado"]["Estimativa de Taxa"].sum()
    n_pedidos_depositados = separa_per_status["Depositado"]["Package ID"].nunique() -1
    aDepositar = separa_per_status["A Depositar"]["Estimativa de Taxa"].sum()
    n_pedidos_adepositar = separa_per_status["A Depositar"]["Package ID"].nunique() -1
    taxa = float(depositado) + float(aDepositar) + float(n_pedidos_depositados*4) + float(n_pedidos_adepositar*4)
    return taxa

def custo(data_vendas):
    separa_per_status = {separa_per_status: grupo for separa_per_status, grupo in data_vendas_final.groupby('Status')}
    depositado = separa_per_status["Depositado"]["Custo Total"].sum()
    aDepositar = separa_per_status["A Depositar"]["Custo Total"].sum()
    taxa = float(depositado) + float(aDepositar)
    return taxa
#__________________________________________Despesas Obtidas________________________________________
def despesas_vendas(data_vendas):
    despesa = 0
    separa_per_status = {separa_per_status: grupo for separa_per_status, grupo in data_vendas_final.groupby('Status')}
    aDepositar = separa_per_status["A Depositar"]
    Depositado = separa_per_status["Depositado"]
    devolução_aDepositar = {separa_per_status: grupo for separa_per_status, grupo in aDepositar.groupby('Data de Devolução')}
    devolucao_depositado = {separa_per_status: grupo for separa_per_status, grupo in Depositado.groupby('Data de Devolução')}
    chaves_adeposita = list(devolução_aDepositar.keys())
    chaves_adeposita.remove('Não devolvido')
    chaves_depositado = list(devolucao_depositado.keys())
    chaves_depositado.remove('Não devolvido')
    for i in range(len(chaves_adeposita)):
        valor = devolução_aDepositar[chaves_adeposita[i]]["SKU Subtotal After Discount"].sum()
        despesa += float(valor)
    for m in range(len(chaves_depositado)):
        valor = devolucao_depositado[chaves_depositado[m]]["SKU Subtotal After Discount"].sum()
        despesa += float(valor)
    return despesa
    
def devolucoes_TK(data_vendas):
    despesa = 0
    n_pedidos_devolvidos = 0
    separa_per_status = {separa_per_status: grupo for separa_per_status, grupo in data_vendas_final.groupby('Status')}
    aDepositar = separa_per_status["A Depositar"]
    Depositado = separa_per_status["Depositado"]
    devolução_aDepositar = {separa_per_status: grupo for separa_per_status, grupo in aDepositar.groupby('Data de Devolução')}
    devolucao_depositado = {separa_per_status: grupo for separa_per_status, grupo in Depositado.groupby('Data de Devolução')}
    chaves_adeposita = list(devolução_aDepositar.keys())
    print(chaves_adeposita)
    chaves_adeposita.remove('Não devolvido')
    chaves_depositado = list(devolucao_depositado.keys())
    print(chaves_depositado)
    chaves_depositado.remove('Não devolvido')
    for i in range(len(chaves_adeposita)):
        valor = devolução_aDepositar[chaves_adeposita[i]]["Estimativa de Taxa"].sum()
        n_pedidos_devolvidos += devolução_aDepositar[chaves_adeposita[i]]["Package ID"].nunique() -1
        despesa += float(valor)
    for m in range(len(chaves_depositado)):
        valor = devolucao_depositado[chaves_depositado[m]]["Estimativa de Taxa"].sum()
        n_pedidos_devolvidos += devolucao_depositado[chaves_depositado[m]]["Package ID"].nunique() -1
        despesa += float(valor)
    return despesa + float(n_pedidos_devolvidos*4)

def devolucoes_Custo(data_vendas):
    despesa = 0
    separa_per_status = {separa_per_status: grupo for separa_per_status, grupo in data_vendas_final.groupby('Status')}
    aDepositar = separa_per_status["A Depositar"]
    Depositado = separa_per_status["Depositado"]
    devolução_aDepositar = {separa_per_status: grupo for separa_per_status, grupo in aDepositar.groupby('Data de Devolução')}
    devolucao_depositado = {separa_per_status: grupo for separa_per_status, grupo in Depositado.groupby('Data de Devolução')}
    chaves_adeposita = list(devolução_aDepositar.keys())
    chaves_adeposita.remove('Não devolvido')
    chaves_depositado = list(devolucao_depositado.keys())
    chaves_depositado.remove('Não devolvido')
    for i in range(len(chaves_adeposita)):
        valor = devolução_aDepositar[chaves_adeposita[i]]["Custo Total"].sum()
        despesa += float(valor)
    for m in range(len(chaves_depositado)):
        valor = devolucao_depositado[chaves_depositado[m]]["Custo Total"].sum()
        despesa += float(valor)
    return despesa

def ajustes(data_vendas): #verificar isso
    separa_per_status = {separa_per_status: grupo for separa_per_status, grupo in data_vendas_final.groupby('Status')}
    depositado = separa_per_status["Depositado"]
    separa_per_datadevolucao = {separa_per_status: grupo for separa_per_status, grupo in depositado.groupby('Data de Devolução')}
    ajuste = separa_per_datadevolucao["Não devolvido"]["Diferênça"].sum()
    n_pedidos = separa_per_datadevolucao["Não devolvido"]["Package ID"].nunique() - 1
    taxa = 4*n_pedidos
    return float(ajuste+taxa)

#importacao dos dados
receitaDevenda = receita_vendas(data_vendas_final) #Valor da receita
devolucoesComissao = devolucoes_TK(data_vendas_final) #valor da comissicao tk dos produtos devolvidos
despesaDeVenda = despesas_vendas(data_vendas_final) #Valor davo as vendas devolvidas
comicaoTk = comissao_tk(data_vendas_final) #Valor da Taxa de Comissao do TK

devolucoesCusto = devolucoes_Custo(data_vendas_final) #custo de devolucao
comicaoTk = comissao_tk(data_vendas_final) #Valor da Taxa de Comissão do TK
custo_de_venda = custo(data_vendas_final)
ajuste = ajustes(data_vendas_final)
receita_liquida = receitaDevenda - despesaDeVenda
lucroLiquidooperacional = receita_liquida - comicaoTk + devolucoesComissao
lucroBruto = lucroLiquidooperacional + devolucoesCusto + ajuste - custo_de_venda

#escrita do Resumo da loja
print("Insira o nome da loja que estamos calculando")
nome_loja = str(input())
print("Insira o nome do mes de calculo")
mes = str(input())

with open(f'Resumo_ {nome_loja}.txt', 'a', encoding='utf-8') as f:
    f.write(f'Resumo da loja {nome_loja} período {mes}\n')
    f.write(f'_________________________________________\n')
    f.write(f'Receita de Venda                 {receitaDevenda:<30.2f}\n')
    f.write(f'Vendas que sofreram devolução    {-despesaDeVenda:>30.2f}\n')
    f.write(f'_________________________________________\n')
    f.write(f'Receita Liquida                  {(receita_liquida):^30.2f}\n')
    f.write(f'\n')
    f.write(f'Devolução da Comissão            {devolucoesComissao:<30.2f}\n')
    f.write(f'Comissão do Tik Tok              {-comicaoTk:>30.2f}\n')
    f.write(f'_________________________________________\n')
    f.write(f'Lucro Liquido Operacional        {lucroLiquidooperacional:^30.2f}\n')
    f.write(f'\n')
    f.write(f'Custo das vendas                 {-custo_de_venda:>30.2f}\n')
    f.write(f'Devolução do Custo               {devolucoesCusto:<30.2f}\n')
    if ajuste >= 0:
        f.write(f'Ajustes                         {ajuste:<30.2f}\n')
    if ajuste <= 0:
        f.write(f'Ajustes                         {ajuste:>30.2f}\n')
    f.write(f'_________________________________________\n')
    f.write(f'Lucro Bruto                      {lucroBruto:^30.2f}\n')
    f.write(f'\n')