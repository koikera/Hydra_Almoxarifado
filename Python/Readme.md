# Projeto Flask com Agendador e Banco de Dados

Este é um exemplo de projeto em Flask que utiliza o agendador de tarefas `APScheduler`, gerenciamento de banco de dados, e permite configurar o modo de execução da aplicação (Desenvolvimento ou Produção). Ele também oferece uma API com um endpoint básico de status e integração com o CORS para permitir requisições de diferentes origens.

## Pré-requisitos

Certifique-se de que você tenha as seguintes dependências instaladas no seu ambiente:

- **Python 3.x**
- **pip** (Gerenciador de pacotes Python)
- **Virtualenv** (opcional, mas recomendado)

## Instalando Dependências

1. Instale o Flask API no seu ambiente: `pip install Flask Flask-CORS Flask-APScheduler apscheduler`

## Configuração do Projeto
O projeto oferece duas configurações principais: modo desenvolvimento e modo produção.

1. Modo de Desenvolvimento: 
O servidor Flask será executado com recarregamento automático de código e com depuração ativada.

2. Modo de Produção: 
O servidor Flask será executado sem depuração, mais adequado para ambientes de produção.

Você pode definir o modo de execução através de um parâmetro de linha de comando --mode. O valor pode ser developer ou production.

## Rodando o projeto

Para rodar o projeto, execute o seguinte comando:

`python app.py --mode <modo>`

Onde `<modo>` pode ser:

- `developer`: Para rodar a aplicação em modo de desenvolvimento.

- `production`: Para rodar a aplicação em modo de produção

Exemplo bash:

`python app.py --mode developer`

O Flask será iniciado no host `127.0.0.1` na porta `3000` por padrão. Você pode acessar a API via `http://localhost:3000/api/status` para validar se o projeto está funcionando normalmente.

- O endpoint de status deverá retornar um json igual a esse `{
  "status": "API is running",
  "version": "v1"
}`

