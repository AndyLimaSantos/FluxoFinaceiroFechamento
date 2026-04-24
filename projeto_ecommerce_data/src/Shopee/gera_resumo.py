#Esse script vai receber a planilha anmterior de Dados_venda_final.csv,
#e vai gerar os arquivos de resumo com o fechamento que vai para o DRE

#importacao das bibliotecas
import pandas as pd

# Receita de Venda ----------------------------------------------------------------
def receita_vendas(data_vendas):
    separa_per_status = {separa_per_status: grupo for separa_per_status, grupo in data_vendas.groupby('Status')}
    depositado = separa_per_status["Depositado"]["SKU Subtotal After Discount"].sum()
    aDepositar = separa_per_status["A Depositar"]["SKU Subtotal After Discount"].sum()
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
        valor = devolução_aDepositar[chaves_adeposita[i]]["SKU Subtotal After Discount"].sum()
        despesa += float(valor)
    for m in range(len(chaves_depositado)):
        valor = devolucao_depositado[chaves_depositado[m]]["SKU Subtotal After Discount"].sum()
        despesa += float(valor)
    return despesa
# Comisoes e taxas ----------------------------------------------------------------
def taxa_comicao(data_vendas):
    separa_per_status = {separa_per_status: grupo for separa_per_status, grupo in data_vendas.groupby('Status')}
    depositado = separa_per_status["Depositado"]["Taxa de comissão bruta"].sum()
    aDepositar = separa_per_status["A Depositar"]["Taxa de comissão bruta"].sum()
    taxa = float(depositado) + float(aDepositar)
    return taxa
    
def taxa_servico(data_vendas):
    separa_per_status = {separa_per_status: grupo for separa_per_status, grupo in data_vendas.groupby('Status')}
    depositado = separa_per_status["Depositado"]["Taxa de serviço bruta"].sum()
    aDepositar = separa_per_status["A Depositar"]["Taxa de serviço bruta"].sum()
    taxa = float(depositado) + float(aDepositar)
    return taxa
    
def taxa_envio_reversa(data_vendas):
    separa_per_status = {separa_per_status: grupo for separa_per_status, grupo in data_vendas.groupby('Status')}
    depositado = separa_per_status["Depositado"]["Taxa de Envio Reversa"].sum()
    aDepositar = separa_per_status["A Depositar"]["Taxa de Envio Reversa"].sum()
    taxa = float(depositado) + float(aDepositar)
    return taxa
    
def taxa_transacao(data_vendas):
    separa_per_status = {separa_per_status: grupo for separa_per_status, grupo in data_vendas.groupby('Status')}
    depositado = separa_per_status["Depositado"]["Taxa de transação"].sum()
    aDepositar = separa_per_status["A Depositar"]["Taxa de transação"].sum()
    taxa = float(depositado) + float(aDepositar)
    return taxa

def comissao_SH(data_vendas):
    separa_per_status = {separa_per_status: grupo for separa_per_status, grupo in data_vendas.groupby('Status')}
    depositado = separa_per_status["Depositado"]["Estimativa de Taxa"].sum()
    aDepositar = separa_per_status["A Depositar"]["Estimativa de Taxa"].sum()
    taxa = float(depositado) + float(aDepositar)
    return taxa

def devolucoes_SH(data_vendas):
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

#Ajuste ----------------------------------------------------------------------------
def ajustes(data_vendas, correcao): #ele não pode pegar a coluna inteira, o motivo é que senão ele pega taxas repetidas, aumentando assim o valor dado
    separa_per_status = {separa_per_status: grupo for separa_per_status, grupo in data_vendas.groupby('Status')}
    depositado = separa_per_status["Depositado"]
    separa_per_datadevolucao = {separa_per_status: grupo for separa_per_status, grupo in depositado.groupby('Data de Devolução')}

    separa_per_status2 = {separa_per_status: grupo for separa_per_status, grupo in correcao.groupby('Status')}
    depositado2 = separa_per_status2["Depositado"]
    separa_per_datadevolucao2 = {separa_per_status2: grupo for separa_per_status2, grupo in depositado2.groupby('Data de Devolução')}
    
    ajuste = separa_per_datadevolucao["Não devolvido"]["Diferênça"].sum()
    ajuste2 = separa_per_datadevolucao2["Não devolvido"]["SKU Subtotal After Discount"].sum()
    return float(ajuste - ajuste2)

def frete(data_vendas):
    return float(data_vendas["Frete"].sum())

def main():
    #importação dos dados que desejamos
    data_vendas_final = pd.read_csv("Dados_venda_final.csv").drop("Unnamed: 0", axis = 1)
    dadoSemDuplicacao = data_vendas_final[data_vendas_final["Order ID"].duplicated() == False]
    dadosDuplicados = data_vendas_final[data_vendas_final["Order ID"].duplicated() == True]
    # Receita de Venda ----------------------------------------------------------------
    receita = receita_vendas(data_vendas_final)
    receitaRetornada = despesas_vendas(data_vendas_final)
    # Despesas ------------------------------------------------------------------------
    taxaDservico = taxa_servico(dadoSemDuplicacao)
    taxaDcomicao = taxa_comicao(dadoSemDuplicacao)    
    taxaDenvio = taxa_envio_reversa(dadoSemDuplicacao)    
    taxaDtransacao = taxa_transacao(dadoSemDuplicacao)
    estimativaComicao = comissao_SH(dadoSemDuplicacao)
    frete_pago = frete(dadoSemDuplicacao)
    # Devolucoes -----------------------------------------------------------------
    devolucaoTaxa = devolucoes_SH(dadoSemDuplicacao)
    devolucaoProduto = devolucoes_Custo(data_vendas_final)

    # Custos ---------------------------------------------------------------------------
    custoProduto = custo(data_vendas_final)

    #Ajuste ----------------------------------------------------------------------------
    valorAjustado = ajustes(dadoSemDuplicacao,dadosDuplicados)



    receitaliquida = receita - receitaRetornada
    lucroliquidooperacional = receitaliquida - taxaDcomicao -taxaDservico -taxaDenvio -taxaDtransacao -frete_pago + devolucaoTaxa
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
        f.write(f'Devolução da Comissão            {devolucaoTaxa:<30.2f}\n')
        f.write(f'Comissão Shopee                  {-taxaDcomicao:>30.2f}\n')
        f.write(f'Taxa de Serviço                  {-taxaDservico:>30.2f}\n')
        f.write(f'Taxa de envio                    {-taxaDenvio:>30.2f}\n')
        f.write(f'Taxa de Transação                {-taxaDtransacao:>30.2f}\n')
        f.write(f'Frete                            {-frete_pago:>30.2f}\n')
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