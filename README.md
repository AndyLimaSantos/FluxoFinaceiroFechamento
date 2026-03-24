# Projeto de Integração e Análise de Dados de E-commerce

## Sobre o Projeto

Este projeto tem como objetivo integrar dados de vendas provenientes de diferentes plataformas de e-commerce, realizar o tratamento e transformação desses dados (ETL) e gerar insights estratégicos para apoio à tomada de decisão. Utilizando como base de dados planilhas coletadas dos próprios e-commerce como de sistemas que utiizam de ERP.

A solução foi desenvolvida em Python com foco em automação, análise de dados e geração de métricas relevantes como KPIs de vendas.

## Funcionalidades

1.  Integração de dados de múltiplas fontes (e-commerces).

    - Shien, Shopee, Mercado Livre, Tik Tok entre outros que podem vir a aparecer futuramente.

2. Tratamento e limpeza de dados

    - Remoção de valores nulos
    - Padronização de tipos de dados
    - Correção de inconsistências

3. Processo de ETL (Extract, Transform, Load) ou ELT dependendo do processo, e ao mesmo tempo aplicação do EDA.

4. Cálculo de KPIs de vendas, como:
    - Receita total
    - Ticket médio
    - Volume de vendas
    - Produtos mais vendidos

5. Geração de insights estratégicos
6. Preparação dos dados para visualização (BI / dashboards)

## Tecnologias Utilizadas
- Python
- Pandas
- NumPy
- Matplotlib / Seaborn
- APIs de e-commerce (atualmente esse é o que esta sendo estudado)

# Como Executar o Projeto

1. Clonar o repositório
~~~python
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
~~~


~~~python
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
~~~


~~~python
pip install -r requirements.txt
~~~

~~~python
python src/main.py
~~~


## Exemplos de Insights Gerados

    - Identificação dos produtos mais rentáveis
    - Análise de sazonalidade nas vendas
    - Comparação de performance entre plataformas
    - Detecção de padrões de comportamento de compra

## Possíveis Melhorias Futuras

    - Integração com ferramentas de BI (Power BI, Tableau)
    - Deploy em ambiente cloud (AWS, GCP)
    - Criação de API para consumo dos dados
    - Implementação de modelos de Machine Learning
    - Previsão de vendas
    - Recomendação de produtos

## Licença

Este projeto está sob a licença MIT.

## Autor
Anderson Lima dos Santos