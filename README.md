#Desafio Técnico Luiza Labs
Esse repositório tem o propósito de apresentar a solução do desafio técnico Luiza Labs. Veja a [descrição completa do desafio](https://gist.github.com/dcassiano-luizalabs/325d6cdeb05394572a88/).

[![Build Status](https://travis-ci.org/drgarcia1986/desafio-luiza-labs.png)](http://travis-ci.org/drgarcia1986/desafio-luiza-labs)
[![Coverage Status](https://coveralls.io/repos/drgarcia1986/desafio-luiza-labs/badge.png)](https://coveralls.io/r/drgarcia1986/desafio-luiza-labs)

### Pré requisitos
#### Mysql
Se optar pelo modo de uso MySql, será necessária uma instância do MySql rodando com algum schema destinado a aplicação, uma sugestão seria um schema chamado **luizalabs**.

```mysql
CREATE SCHEMA `luizalabs` ;
```
### Realizando download da aplicação
```bash
user@host:~$ git clone https://github.com/drgarcia1986/desafio-luiza-labs luiza-labs
```
### Criando e ativando o VirtualEnv
```bash
user@host:~$ virtualenv venv_luiza_labs
user@host:~$ source venv_luiza_labs/bin/activate
(venv_luiza_labs) user@host:~$
```
### Instalando as depêndencias
```bash
(venv_luiza_labs) user@host:~/luiza-labs$ pip install -r requirements.txt
```
### Parâmetros de execução
| Parâmetro  | Propósito | Valor default |
|---|---|---|
| memory  | Define se as informações serão armazenadas em memória (SQLite) ou em um banco MySql | False |
| mysql_host  | Ip e porta do MySql | localhost:3306 |
| mysql_user  | Usuário de acesso ao MySql  | root |
| mysql_passwd  | Senha de acesso ao MySql  | admin |
| mysql_db | Schema do MySql utilizado pela aplicação | luizalabs |
| http_port | Porta que o servidor ficará ouvindo | 8888 |
| logging | Nível de apresentação de log (_debug_, _info_, _warning_, _error_ ou _none_) | info |
| log_file_prefix | Define o caminho do arquivo de log (sem informar esse parâmetro os logs serão exibidos no terminal) |  | 

### Executando a aplicação
#### Modo MySql
```bash
(venv_luiza_labs) user@host:~/luiza-labs$ python luiza_labs --mysql_host=localhost:3306 --mysql_user=root --mysql_passwd=admin --mysql_db=luizalabs --http_port=8888
```

#### Modo em memoria (SQLite)
```bash
(venv_luiza_labs) user@host:~/luiza-labs$ python luiza_labs --memory=True --http_port=8888
```

### API REST
#### /person (Operações sobre pessoas)
##### **POST** /person
Cadastra uma nova pessoa.
###### body
| Parâmetro | Descrição | Obrigatório |
| --- | --- | --- |
| facebookId | Id utilizado para consulta a Facebook Graph API | Sim |
###### Sucesso
201 Created
###### Possíveis erros
| Código HTTP  | Mensagem |
| --- | --- |
| 404 | Some of the aliases you requested do not exist |
| 500 | facebookId required |

##### **GET** /person
Retorna uma lista de pessoas.
###### querystring
| Parâmetro | Descrição | Obrigatório |
| --- | --- | --- |
| limit | Quantidade de pessoas que devem retornar na listagem | Não |
###### Sucesso
200 OK
```json
[
   {
      "username":"foo",
      "facebookId":"12313123123",
      "name":"For Bar",
      "gender":"male"
   }
]
```
##### **DELETE** /person/{facebook_id}
Deleta uma pessoa.
###### url
| Parâmetro | Descrição | Obrigatório |
| --- | --- | --- |
| facebook_id | Id do Facebook da pessoa a ser excluída | Sim |
###### Sucesso
204 No Content
