# Controle de Animais — Pipeline ETL

## 1. Introdução

Este projeto implementa um pipeline de **ETL (Extract, Transform, Load)** para processamento de dados de animais obtidos a partir de um dataset público do Kaggle.

O objetivo é automatizar o fluxo de extração, tratamento e carga dos dados, organizando as informações em tabelas por domínio e disponibilizando os dados finais em diferentes formatos:

* Arquivos **CSV**
* Arquivos **Parquet**
* Tabelas no **MySQL**

O pipeline é executado em Python e pode ser iniciado via Docker, facilitando a configuração do ambiente e a criação do banco de dados local.

---

## 2. Arquitetura do Pipeline

### Visão geral

O fluxo do projeto segue as etapas abaixo:

```text
Kaggle → Python ETL → Transformações com Pandas → CSV / Parquet / MySQL
```

### Etapas do processo

1. **Extração**

   * Autenticação na API do Kaggle.
   * Download do dataset `jinbonnie/animal-data`.
   * Extração do arquivo `.zip`.
   * Leitura do arquivo CSV original.

2. **Transformação**

   * Padronização dos nomes das colunas.
   * Conversão da idade dos animais para meses.
   * Tradução de valores categóricos para português.
   * Separação dos dados em tabelas por domínio.
   * Salvamento dos dados tratados em formato Parquet.

3. **Carga**

   * Leitura dos arquivos transformados.
   * Geração de arquivos CSV.
   * Geração de arquivos Parquet.
   * Carga das tabelas no MySQL.

---

## 3. Tecnologias Utilizadas

* **Python 3.11**
* **Pandas**
* **Kaggle API**
* **SQLAlchemy**
* **PyMySQL**
* **MySQL 8.0**
* **Docker**
* **Docker Compose**
* **Parquet**
* **CSV**

---

## 4. Estrutura do Projeto

```text
controle-animais/
├── data/
│   ├── raw/                  # Arquivos brutos extraídos do Kaggle
│   ├── transform/            # Arquivos tratados em Parquet
│   └── output/
│       ├── csv/              # Saída final em CSV
│       └── parquet/          # Saída final em Parquet
├── src/
│   ├── extract/
│   │   └── extract.py        # Extração dos dados do Kaggle
│   ├── transform/
│   │   └── transform.py      # Transformações e separação dos dados
│   └── load/
│       └── load.py           # Carga em CSV, Parquet e MySQL
├── main.py                   # Arquivo principal do pipeline
├── requirements.txt          # Dependências Python
├── Dockerfile                # Imagem da aplicação Python
├── docker-compose.yml        # Serviços da aplicação e MySQL
├── .env                      # Variáveis de ambiente
└── pipeline.log              # Logs de execução do pipeline
```

---

## 5. Pré-requisitos

Antes de executar o projeto, é necessário ter instalado:

* Docker
* Docker Compose
* Conta no Kaggle
* Credenciais da API do Kaggle

---

## 6. Configuração das Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes informações:

```env
MYSQL_USER=appuser
MYSQL_PASSWORD=apppass
MYSQL_HOST=mysql
MYSQL_PORT=3306
MYSQL_DATABASE=controle_animais

KAGGLE_USERNAME=seu_usuario_kaggle
KAGGLE_KEY=sua_chave_kaggle
```

Essas variáveis são usadas pela aplicação para conectar no MySQL e autenticar na API do Kaggle.

---

## 7. Configuração do Docker

O projeto possui dois serviços principais:

### MySQL

Banco de dados usado para armazenar as tabelas finais do pipeline.

```yaml
mysql:
  image: mysql:8.0
  container_name: controleanimais-mysql
  restart: always
  environment:
    MYSQL_ROOT_PASSWORD: root
    MYSQL_DATABASE: controle_animais
    MYSQL_USER: appuser
    MYSQL_PASSWORD: apppass
  ports:
    - "3306:3306"
  volumes:
    - mysql_data:/var/lib/mysql
```

### Aplicação Python

Serviço responsável por executar o pipeline ETL.

```yaml
app:
  build: .
  container_name: controleanimais-app
  restart: always
  depends_on:
    - mysql
  env_file:
    - .env
  volumes:
    - .:/app
  command: python main.py
```

---

## 8. Como Executar o Projeto

Na raiz do projeto, execute:

```bash
docker compose up --build
```

Esse comando irá:

1. Criar o container do MySQL.
2. Criar o container da aplicação Python.
3. Instalar as dependências do projeto.
4. Executar o arquivo `main.py`.
5. Rodar o pipeline completo de ETL.

---

## 9. Fluxo de Execução

O arquivo `main.py` é responsável por coordenar o pipeline:

```text
main.py
├── load_dotenv()
├── extract_data()
├── transform_data()
└── load_data()
```

### Etapas executadas

| Etapa         | Função             | Descrição                              |
| ------------- | ------------------ | -------------------------------------- |
| Extração      | `extract_data()`   | Baixa e extrai o dataset do Kaggle     |
| Transformação | `transform_data()` | Trata, traduz e separa os dados        |
| Carga         | `load_data()`      | Salva os dados em CSV, Parquet e MySQL |

---

## 10. Transformações Realizadas

### Padronização dos nomes das colunas

Função:

```python
rename_columns_snake_case(df)
```

Padroniza os nomes das colunas para o formato `snake_case`, facilitando a manipulação dos dados no Pandas e no banco de dados.

---

### Conversão da idade dos animais

Função:

```python
transform_animal_age(df)
```

Converte a coluna de idade dos animais para meses.

Exemplo:

```text
2 years 3 months → 27
1 year → 12
6 months → 6
```

Essa transformação facilita análises numéricas sobre faixa etária dos animais.

---

### Tradução de colunas categóricas

Função:

```python
translate_categorical_columns(df)
```

Traduz valores categóricos do inglês para o português, como:

* Espécie
* Sexo
* Cor
* Localização
* Motivo de entrada
* Tipo de movimentação
* Motivo de retorno
* Motivo de óbito

Exemplo:

```text
Dog → Cachorro
Cat → Gato
Adoption → Adoção
Stray → Animal Errante
```

---

### Separação por domínios

Função:

```python
extract_domain_dataframes(df)
```

Separa o DataFrame original em três conjuntos principais:

| Domínio       | Descrição                                                 |
| ------------- | --------------------------------------------------------- |
| `animal_base` | Informações cadastrais dos animais                        |
| `fluxo`       | Dados de entrada, localização e movimentação              |
| `desfecho`    | Dados relacionados a óbito, eutanásia ou chegada sem vida |

---

### Renomeação das colunas para português

Função:

```python
rename_columns_ptbr(dict_df)
```

Renomeia as colunas finais para português, tornando as tabelas mais claras para análise.

---

## 11. Estrutura dos Dados Finais

### Tabela `animal_base`

Contém os dados principais dos animais.

| Coluna             | Descrição                 |
| ------------------ | ------------------------- |
| `id_animal`        | Identificador do animal   |
| `numero_microchip` | Número do microchip       |
| `nome_animal`      | Nome do animal            |
| `especie`          | Espécie do animal         |
| `raca`             | Raça                      |
| `cor_base`         | Cor principal             |
| `sexo`             | Sexo do animal            |
| `idade_animal`     | Idade convertida em meses |

---

### Tabela `fluxo`

Contém informações sobre entrada, localização e movimentação dos animais.

| Coluna              | Descrição                         |
| ------------------- | --------------------------------- |
| `id_animal`         | Identificador do animal           |
| `data_entrada`      | Data de entrada                   |
| `motivo_entrada`    | Motivo da entrada                 |
| `transferencia`     | Indica se houve transferência     |
| `codigo_abrigo`     | Código do abrigo                  |
| `localizacao`       | Localização do animal             |
| `data_movimentacao` | Data da movimentação              |
| `tipo_movimentacao` | Tipo da movimentação              |
| `adocao_teste`      | Indica adoção em período de teste |
| `data_retorno`      | Data de retorno                   |
| `motivo_retorno`    | Motivo do retorno                 |

---

### Tabela `desfecho`

Contém informações relacionadas ao desfecho do animal.

| Coluna                  | Descrição                        |
| ----------------------- | -------------------------------- |
| `id_animal`             | Identificador do animal          |
| `data_obito`            | Data de óbito                    |
| `motivo_obito`          | Motivo do óbito                  |
| `morreu_fora_do_abrigo` | Indica se morreu fora do abrigo  |
| `eutanasiado`           | Indica se foi eutanasiado        |
| `morto_ao_chegar`       | Indica se chegou morto ao abrigo |

---

## 12. Saídas Geradas

Após a execução do pipeline, os arquivos tratados são gerados nos seguintes diretórios:

```text
data/output/csv/
├── animal_base.csv
├── fluxo.csv
└── desfecho.csv
```

```text
data/output/parquet/
├── animal_base.parquet
├── fluxo.parquet
└── desfecho.parquet
```

Também são criadas as tabelas no MySQL:

```text
animal_base
fluxo
desfecho
```

---

## 13. Carga no MySQL

A função responsável pela carga no MySQL é:

```python
save_to_mysql(df, table_name)
```

Ela utiliza as variáveis de ambiente para montar a conexão:

```text
mysql+pymysql://appuser:apppass@mysql:3306/controle_animais
```

As tabelas são salvas com o parâmetro:

```python
if_exists="replace"
```

Ou seja, a cada execução, as tabelas existentes são substituídas pelos dados mais recentes.

---

## 14. Como Acessar o Banco MySQL

Com os containers em execução, é possível acessar o banco usando:

```bash
docker exec -it controleanimais-mysql mysql -u appuser -p
```

Senha:

```text
apppass
```

Depois, selecione o banco:

```sql
USE controle_animais;
```

Exemplo de consulta:

```sql
SELECT * FROM animal_base LIMIT 10;
```

---

## 15. Logs

O pipeline gera logs em dois locais:

* Console do Docker
* Arquivo `pipeline.log`

Os logs registram:

* Início e fim do pipeline
* Etapa de extração
* Etapa de transformação
* Etapa de carga
* Erros inesperados
* Avisos sobre arquivos ausentes ou DataFrames vazios

---

## 16. Tratamento de Erros

O projeto possui blocos `try/except` nas principais etapas do pipeline.

Isso permite:

* Registrar falhas no log
* Interromper o pipeline em caso de erro crítico
* Facilitar a identificação da etapa com problema
* Melhorar a rastreabilidade da execução

---

## 17. Observações Importantes

* O dataset só é baixado novamente caso o arquivo `.zip` ainda não exista em `data/raw`.
* Os arquivos transformados são salvos inicialmente em `data/transform`.
* A carga final gera tanto CSV quanto Parquet.
* O volume `mysql_data` garante persistência dos dados do MySQL.
* Como o projeto usa volume local no Docker, os arquivos gerados dentro do container também ficam disponíveis na pasta do projeto.

---

## 18. Possíveis Melhorias Futuras

* Adicionar orquestração com Apache Airflow.
* Criar validações automáticas de qualidade dos dados.
* Implementar carga incremental.
* Criar dashboard em Power BI.
* Adicionar testes unitários para as funções de transformação.
* Criar documentação com prints da execução.
* Separar ambientes de desenvolvimento e produção.
* Adicionar controle de versão dos arquivos processados por data.

---

## 19. Conclusão

Este projeto demonstra a construção de um pipeline ETL completo utilizando Python, Pandas, Docker e MySQL.

A solução permite extrair dados de uma fonte externa, transformar as informações para um formato mais analítico e disponibilizar os dados finais em arquivos e banco relacional.

Com isso, os dados ficam organizados, persistidos e prontos para análises futuras sobre animais, movimentações, adoções, retornos e desfechos.