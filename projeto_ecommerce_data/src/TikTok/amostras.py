#Correção dos valores de amostra, insirindo os custos e somando para saber quando é o valor em amostras
import pandas as pd
#importaçõa dos valores
dados_amostras = pd.read_csv("amostras_HG.csv")
skus = pd.read_csv("SKU2SKUarmazem.csv")
amostras = pd.DataFrame(data = {"SKU Seller":dados_amostras["Seller SKU"], "Quantity":dados_amostras["Quantity"]})
#mesclagens dos dados de custo e criação da tabela que iremos utilizar
amostras_custo = pd.merge(amostras, skus, on = "SKU Seller").drop("Unnamed: 0", axis = 1)
amostras_custo["Custo Total"] = amostras_custo["Quantity"]*amostras_custo["Custo Médio"]
#exportação dos dados de custo que foram destinados as amostras
#amostras_custo.to_excel("amostras_final.xlsx")
amostras_custo.to_csv("amostras_final.csv")