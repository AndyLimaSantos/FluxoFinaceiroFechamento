#Aqui vamos executar as contas de maneira automatica, ele vai executar tudo no terminal sozinho.
import subprocess

scripts =["Start_EDA.py",\
          "SKUSeller2SKUArmazem_feito.py",\
          "Corrige CustoUP.py",\
          "Dados_vendas.py",\
          "Gerar_resumo.py"]

for script in scripts:
    print(f"Executando {script}...")
    subprocess.run(["py", script], check=True)