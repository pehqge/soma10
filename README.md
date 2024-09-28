# Jogo Soma 10

## Sobre o jogo
O jogo Soma 10 consiste na disputa entre dois participantes em um tabuleiro de 16 casas interligadas entre si. O objetivo do jogo é conseguir o maior número de fichas através de somas que resultam em 10.

## Documentação
A documentação do jogo pode ser acessada no diretório [doc](doc) em [Especificacao de Requisitos.pdf](doc/Especificacao%20de%20Requisitos.pdf). Para detalhes de modelagem, abra o projeto ```doc/modelagem/soma10.vpp``` com o software [Visual Paradigm](https://www.visual-paradigm.com/).

## Como executar
Para executar o jogo, é necessário ter o Python instalado em sua máquina. Caso não tenha, você pode baixá-lo [aqui](https://www.python.org/downloads/).

### 1º Passo
Criar um ambiente virtual para instalar as dependências do jogo. Para isso, abra o terminal e execute o comando:
```sh
python3 -m venv venv
```

### 2º Passo
Ativar o ambiente virtual, executando o comando:
```sh
source venv/bin/activate
```

### 3º Passo
Instalar as dependências do jogo, executando o comando:
```sh
pip3 install -r requirements.txt
```

### 4º Passo
Executar o jogo, executando os comandos:
```sh
cd src
python3 main.py
```