# FAT_FREE_API

## Descrição do Projeto
FAT_FREE_API é um projeto em Python projetado para fornecer uma API leve e eficiente. A estrutura do projeto é organizada para facilitar o desenvolvimento, teste e implantação.

## Estrutura do Projeto
O projeto é organizado nas seguintes diretórios e arquivos:

- **.pytest_cache**: Diretório para arquivos de cache do pytest.
- **.ruff_cache**: Diretório para arquivos de cache do Ruff.
- **fat_free_api**: Diretório principal do aplicativo.
  - **__pycache__**: Diretório para arquivos Python compilados.
  - **__init__.py**: Arquivo de inicialização para o pacote fat_free_api.
  - **app.py**: Arquivo principal do aplicativo que contém a lógica da API.
  - **tests**: Diretório contendo arquivos de teste para o aplicativo.
- **poetry.lock**: Arquivo de bloqueio do Poetry, especificando as versões exatas das dependências.
- **pyproject.toml**: Arquivo de configuração do projeto, incluindo dependências e requisitos do sistema de build.

## Começando
Para começar com o projeto FAT FREE API, siga estas etapas:

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seuusuario/fat_free_api.git
   cd fat_free_api

2. **Instale as dependências**:
    ```bash
    poetry install

3. **Para executar a aplicação**:
    ```bash
    task run

4. **Para executar testes com PyTest**:
    ```bash
    task test