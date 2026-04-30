import pandas as pd
from datetime import datetime

# Receita de Venda ----------------------------------------------------------------
def receita_vendas(data_vendas):
    separa_per_status = {separa_per_status: grupo for separa_per_status, grupo in data_vendas.groupby('Status')}
    depositado = separa_per_status["Depositado"]['Receita'].sum()
    aDepositar = separa_per_status["A Depositar"]['Receita'].sum()
    valor = float(depositado+aDepositar)
    return valor


# Despesas ------------------------------------------------------------------------
def despesas_vendas(data_vendas):
    despesa = 0
    separa_per_status = {separa_per_status: grupo for separa_per_status, grupo in data_vendas.groupby('Status')}
    aDepositar = separa_per_status["A Depositar"]
    Depositado = separa_per_status["Depositado"]
    devolução_aDepositar = {separa_per_status: grupo for separa_per_status, grupo in aDepositar.groupby('Data de Devolução')}
    devolucao_depositado = {separa_per_status: grupo for separa_per_status, grupo in Depositado.groupby('Data de Devolução')}
    chaves_adeposita = list(devolução_aDepositar.keys())
    chaves_adeposita.remove('Não devolvido')
    chaves_depositado = list(devolucao_depositado.keys())
    chaves_depositado.remove('Não devolvido')
    for i in range(len(chaves_adeposita)):
        valor = devolução_aDepositar[chaves_adeposita[i]]['Estimativa de Recebimento'].sum()
        despesa += float(valor)
    for m in range(len(chaves_depositado)):
        valor = devolucao_depositado[chaves_depositado[m]]['Estimativa de Recebimento'].sum()
        despesa += float(valor)
    return despesa


# Comisoes e taxas ----------------------------------------------------------------
def taxa_comicao(data_vendas):
    separa_per_status = {separa_per_status: grupo for separa_per_status, grupo in data_vendas.groupby('Status')}
    depositado = separa_per_status["Depositado"]["Taxa de comissão bruta"].sum()
    aDepositar = separa_per_status["A Depositar"]["Taxa de comissão bruta"].sum()
    taxa = float(depositado) + float(aDepositar)
    return taxa
    
def taxa_frete(data_vendas):
    separa_per_status = {separa_per_status: grupo for separa_per_status, grupo in data_vendas.groupby('Status')}
    depositado = separa_per_status["Depositado"]['Taxa de intermediação de frete'].sum()
    aDepositar = separa_per_status["A Depositar"]['Taxa de intermediação de frete'].sum()
    taxa = float(depositado) + float(aDepositar)
    return taxa
    
def taxa_estocagem(data_vendas):
    separa_per_status = {separa_per_status: grupo for separa_per_status, grupo in data_vendas.groupby('Status')}
    depositado = separa_per_status["Depositado"]['Taxa de operação de estocagem'].sum()
    aDepositar = separa_per_status["A Depositar"]['Taxa de operação de estocagem'].sum()
    taxa = float(depositado) + float(aDepositar)
    return taxa
    
def valor_cupom(data_vendas):
    separa_per_status = {separa_per_status: grupo for separa_per_status, grupo in data_vendas.groupby('Status')}
    depositado = separa_per_status["Depositado"]['Valor do cupom'].sum()
    aDepositar = separa_per_status["A Depositar"]['Valor do cupom'].sum()
    taxa = float(depositado) + float(aDepositar)
    return taxa

def comissao_shein(data_vendas):
    separa_per_status = {separa_per_status: grupo for separa_per_status, grupo in data_vendas.groupby('Status')}
    depositado = separa_per_status["Depositado"]["Estimativa de Taxa"].sum()
    aDepositar = separa_per_status["A Depositar"]["Estimativa de Taxa"].sum()
    taxa = float(depositado) + float(aDepositar)
    return taxa

def devolucoes_shein(data_vendas):
    despesa = 0
    separa_per_status = {separa_per_status: grupo for separa_per_status, grupo in data_vendas.groupby('Status')}
    aDepositar = separa_per_status["A Depositar"]
    Depositado = separa_per_status["Depositado"]
    devolução_aDepositar = {separa_per_status: grupo for separa_per_status, grupo in aDepositar.groupby('Data de Devolução')}
    devolucao_depositado = {separa_per_status: grupo for separa_per_status, grupo in Depositado.groupby('Data de Devolução')}
    chaves_adeposita = list(devolução_aDepositar.keys())
    chaves_adeposita.remove('Não devolvido')
    chaves_depositado = list(devolucao_depositado.keys())
    chaves_depositado.remove('Não devolvido')
    for i in range(len(chaves_adeposita)):
        valor = devolução_aDepositar[chaves_adeposita[i]]["Estimativa de Taxa"].sum()
        despesa += float(valor)
    for m in range(len(chaves_depositado)):
        valor = devolucao_depositado[chaves_depositado[m]]["Estimativa de Taxa"].sum()
        despesa += float(valor)
    return despesa
    
# Custos ---------------------------------------------------------------------------
def custo(data_vendas):
    separa_per_status = {separa_per_status: grupo for separa_per_status, grupo in data_vendas.groupby('Status')}
    depositado = separa_per_status["Depositado"]["Custo Total"].sum()
    aDepositar = separa_per_status["A Depositar"]["Custo Total"].sum()
    taxa = float(depositado) + float(aDepositar)
    return taxa

def devolucoes_Custo(data_vendas):
    despesa = 0
    separa_per_status = {separa_per_status: grupo for separa_per_status, grupo in data_vendas.groupby('Status')}
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

def ajustes(data_vendas):
    separa_per_status = {separa_per_status: grupo for separa_per_status, grupo in data_vendas.groupby('Status')}
    depositado = separa_per_status["Depositado"]
    separa_per_datadevolucao = {separa_per_status: grupo for separa_per_status, grupo in depositado.groupby('Data de Devolução')}
    planilha = separa_per_datadevolucao["Não devolvido"]
    valor = planilha["Diferênça"].sum()
    return valor

def frete(data_vendas):
    return float(data_vendas["Taxa de intermediação de frete"].sum())

def main():
    data_vendas_final = pd.read_csv("Dados_venda_final.csv").drop("Unnamed: 0", axis = 1)
    # Receita de Venda ----------------------------------------------------------------
    receita = receita_vendas(data_vendas_final)
    receitaRetornada = despesas_vendas(data_vendas_final)
    # Despesas ------------------------------------------------------------------------
    taxaDestocagem = taxa_estocagem(data_vendas_final) #serviço -> estocagem
    taxaDcomicao = taxa_comicao(data_vendas_final)    
    taxaDenvio = taxa_frete(data_vendas_final)    
    taxaDcupom = valor_cupom(data_vendas_final) #transacao -> cupom
    estimativaComicao = comissao_shein(data_vendas_final)
    frete_pago = frete(data_vendas_final)
    # Devolucoes -----------------------------------------------------------------
    devolucaoTaxa = devolucoes_shein(data_vendas_final)
    devolucaoProduto = devolucoes_Custo(data_vendas_final)
    # Custos ---------------------------------------------------------------------------
    custoProduto = custo(data_vendas_final)
    #Ajuste ----------------------------------------------------------------------------
    valorAjustado = ajustes(data_vendas_final)
    #Calculos importantes
    receitaliquida = receita - receitaRetornada
    lucroliquidooperacional = receitaliquida - estimativaComicao + devolucaoTaxa - taxaDcupom
    lucroBruto = lucroliquidooperacional - custoProduto + devolucaoProduto + valorAjustado
    #escrita do Resumo da loja
    print("Insira o nome da loja que estamos calculando")
    nome_loja = str(input())
    print("Insira o nome do mes de calculo")
    mes = str(input())
    with open(f'Resumo_ {nome_loja}.txt', 'a', encoding='utf-8') as f:
            f.write(f'Resumo da loja {nome_loja} período {mes}\n')
            f.write(f'-------------------------------------------------------------\n')
            f.write(f'Receita de Venda                 {receita:<30.2f}\n')
            f.write(f'Vendas que sofreram devolução    {-receitaRetornada:>30.2f}\n')
            f.write(f'-------------------------------------------------------------\n')
            f.write(f'Receita Liquida                  {(receitaliquida):^30.2f}\n')
            f.write(f'\n')
            f.write(f'Devolução da taxas + comissão    {devolucaoTaxa:<30.2f}\n')
            f.write(f'Comissão Shein                   {-taxaDcomicao:>30.2f}\n')
            f.write(f'Taxa de estocagem                {-taxaDestocagem:>30.2f}\n')
            f.write(f'Taxa de envio                    {-taxaDenvio:>30.2f}\n')
            f.write(f'Cupons                           {-taxaDcupom:>30.2f}\n')
            f.write(f'-------------------------------------------------------------\n')
            f.write(f'Lucro Liquido Operacional        {lucroliquidooperacional:^30.2f}\n')
            f.write(f'\n')
            f.write(f'Custo das vendas                 {-custoProduto:>30.2f}\n')
            f.write(f'Devolução do Custo               {devolucaoProduto:<30.2f}\n')
            if valorAjustado >= 0:
                f.write(f'Ajustes                          {valorAjustado:<30.2f}\n')
            if valorAjustado < 0:
                f.write(f'Ajustes                          {valorAjustado:>30.2f}\n')
            f.write(f'-------------------------------------------------------------\n')
            f.write(f'Lucro Bruto                      {lucroBruto:^30.2f}\n')
            f.write(f'\n')
    return

if __name__ == "__main__":
    main()