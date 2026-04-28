import pandas as pd
#Funcoes utilizadas para o calculo
def verifica_in_armazem(dado_loja, dado_armazem):
    linhas = int(dado_loja.shape[0])
    colunas = list(dado_loja.columns)
    naoEncontrados = []
    valorCusto = []
    if 'Número de referência SKU' in colunas:
        for i in range(0, linhas):
            Sku_seller = dado_loja.loc[i, 'Número de referência SKU']
            existe = dado_armazem['SKU (Armazém)'].isin([Sku_seller]).any()
            if existe == False:
                naoEncontrados.append(Sku_seller)
                valorCusto.append(dado_loja.loc[i,"Custo unitário"])
    if 'SKU' in colunas:
        for i in range(0, linhas):
            Sku_seller = dado_loja.loc[i, 'SKU']
            existe = dado_armazem['SKU (Armazém)'].isin([Sku_seller]).any()
            if existe == False:
                naoEncontrados.append(Sku_seller)
                valorCusto.append(dado_loja.loc[i,"Custo Unitário"])
    return pd.DataFrame(data = {"SKU não encontrados": naoEncontrados,"Custo Unitário":valorCusto})

def main():
    print("Insira o numero de calculos que deverão ser feitos")
    n_calculos = int(input())
    cont = 0
    while cont < n_calculos:
        print("insira o nome do arquivo com os dados de todos os pedidos, com a extensao")
        nome_pedidos = str(input())
        print(f"Tipo de arquivo lido (informe o numero):\n 1) A planilha dos pedidos esta na aba 'orders all';\n 2) A planilha de pedidos esta no 'Vendas BR'.\n")
        aba = int(input())
        if aba == 1:
            pedidos = pd.read_excel(nome_pedidos,  sheet_name="orders all")
            pedidos1 = pedidos[pedidos['Número de referência SKU'].duplicated() == False].reset_index()
            compara_pedidos1 = pd.DataFrame(data = {'SKU':pedidos1['Número de referência SKU'],\
                                       'Custo unitário':pedidos1['Custo unitário'].astype(float).round(2)})
        if aba == 2:
            pedidos = pd.read_excel(nome_pedidos, header=2, sheet_name = "Vendas BR")
            pedidos1 = pedidos[pedidos['SKU'].duplicated() == False].reset_index()
            compara_pedidos1 = pd.DataFrame(data = {'SKU':pedidos1['SKU'],\
                                  'Custo Unitário':pedidos1['Custo Unitário'].astype(float).round(2)})
        
        print(f"Insira o nome do arquivo com os custos dos produtos.\nEsse arquivo é o arquivo é extraido do UpSeller.")
        custo = str(input())
        custo_pedidos =  pd.read_excel(custo)
        custo_modelado = custo_pedidos[custo_pedidos['SKU (Armazém)'].duplicated() == False].reset_index()
        custo_utilizavel = pd.DataFrame(data = {'SKU (Armazém)':custo_modelado['SKU (Armazém)'],\
                                'Custo Médio':custo_modelado['Custo Médio'].astype(float).round(2)})
        
        #Aqui temnos a verificaçõa de que se os custos utilizados na conta, batem com aqueles encontradosno UpSeller
        data_compara = pd.merge(compara_pedidos1, custo_utilizavel, left_on='SKU',\
                         right_on='SKU (Armazém)', how='inner')
        data_compara['Correto'] = data_compara['Custo Médio'] == data_compara['Custo Unitário']
        data_compara.reindex(columns=['SKU', 'SKU (Armazém)', 'Custo unitário', 'Custo Médio','Correto'])
        #Verificação de quais Sku não foram encontrados os custos dentro do UPSeller
        data_compara2 = verifica_in_armazem(compara_pedidos1, custo_utilizavel)


        print("Deseja gerar a planilha em csv e xlsx?\n Sim[Y,y]\n Não[N,n]")
        resposta1= str(input())
        if resposta1 not in ["Não", "não", "n", "N"]:
            print("Nome da loja")
            nome = str(input())
            data_compara.to_excel(f"{nome}.xlsx")
            data_compara.to_csv(f"{nome}.csv")
            data_compara2.to_excel(f"{nome}_comparaSKU.xlsx")
            data_compara2.to_csv(f"{nome}_comparaSKU.csv")
        cont += 1
if __name__ == "__main__":
    main()