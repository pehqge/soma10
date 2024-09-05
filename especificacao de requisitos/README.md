Projeto jogo soma 10
--

Especificação de Requisitos de Software

<!-- comando para iniciar linhas de divisão da tabela-->
<style>
table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
    padding: 5px;
}
</style> 


| Versão   | Autor(es)     | Data    | Ação|
|:-----------:|:----------:|:-----------:|:-----------:|
| 1.0   |Pedro Felipe Menezes <br> Pedro Henrique Gimenez <br> Victória Rodrigues Veloso   | conclusão da versão   | Especificaçõ dos requisitos  |

### Conteúdo:

1. Introdução
2. Visão Geral
3. Requisitos da aplicação

Apêndice: regras do jogo soma 10 

<div style="page-break-before: always;"></div> <!-- comando para iniciar nova pagina -->

## 1. Introdução 

### 1.1 Objetivo

Desenvolvimento de um programa distribuído que suporte a disputa de partidas do jogo soma 10, na modalidade usuário contra usuário, on-line.

### 1.2 Definiçõs e abreviaturas

Regras do jogo: ver apêndice.

### 1.3 Referência

Apresentação das regras do jogo (video do canal 
Booktoy Livraria e Editora): https://youtu.be/1ZkDNbzL2qE
## 2. Visão geral

### 2.1 Arquitetura do software

O software desenvolvido conta com a arquitetura cliente-servidor distribuído.

### 2.2 Premissas de desenvolvimento

- O programa deve ser implementado em python;
- O programa deve utilizar a plataforma DOG como suporte de execução distribuída;
- O projeto deve ser produzido utilizando o Visual Paradigm;
- O projeto deve ser produzido utilizando a linguagem UML, segunda versão.

## 3. Requisitos de Software

### 3.1 Requisitos funcionais

**Requisito funcional 1 - iniciar o programa:**  Ao ser executado, o programa deve apresentar na primeira interface (menu inicial) um botão para iniciar a partida .

**Requisito funcional 2 - iniciar partida:** Ao clicar no botão 'iniciar', o programa deve exibir toda a interface da partida.

**Requisito funcional 3 - distribuição de fiehcas iniciais:** O programa deve iniciar a partida distribuindo 3 cartas para cada jogador, retiradas aleatoriamente do baralho.


**Requisito funcional 4 - exibir tutorial do jogo:** O programa deve contar com um botão para o tutorial do jogo no menu inicial, que ao ser clicado, exibe as regras e instruções do jogo em uma nova janela ou seção.

**Requisito funcional 5 - colocar uma ficha no tabuleiro:** O programa deve permitir que o jogador selecione uma ficha da sua mão e a posicione em uma casa vazia no tabuleiro.

**Requisito funcional 6 - verificar somas de 10:** Ao posicionar uma ficha, o programa deve automaticamente verificar se a soma das cartas em uma linha, coluna ou diagonal resulta em 10 e, em caso afirmativo, recolher as cartas dessa linha e somá-las ao total do jogador.

**Requisito funcional 7 - repor cartas da mão:** Após o jogador inserir uma ficha no tabuleiro, o programa deve permitir que o usuário retire uma carta do baralho.

**Requisito funcional 8 - controlar equidade de cartas:** O programa deve garantir que o próximo jogador não possa iniciar sua jogada enquanto a quantidade de cartas nas mãos dos jogadores estiver desigual. A jogada só será liberada quando ambos os jogadores possuírem o mesmo número de cartas.

**Requisito funcional 9 -  controlar compra de carta em situação de impasse:** Se o jogador não puder realizar uma jogada com as cartas que possui, o programa deve permitir que ele compre apenas uma carta.

**Requisito funcional 10 - validar soma nas fileiras:** O sistema deve validar as somas de forma que, ao inserir a segunda carta, a soma das duas primeiras da fileira deve ser igual ou inferior a 8. Ao inserir a terceira carta, a soma das três cartas da fileira deve ser igual ou inferior a 9.

**Requisito funcional  11 - finalizar a partida:** O programa deve encerrar a partida quando o baralho estiver vazio e nenhum jogador puder realizar uma jogada válida. 

**Requisito funcional 12 - exibir o placar:** O sistema deve exibir o placar, mostrando a soma total de cada jogador e quem foi o campeão da partida.

### 3.2 Requisitos não funcionais
**Requisito não funcional 1 - tecnologia para interface gráfica:** O framework Tkinter deve ser utilizado para a construção da interface gráfica.

**Requisito não funcional 2 - modelo de interface gráfica:** A interface gráfica deve ser construída com base nas figuras 1 e 2.

<div style="text-align: center;">
    <img src="../assets/docs/menu.png">
    <p style="font-style: italic; font-size: 12px;">Figura 1. Interface do menu inicial do jogo.  </p>
</div>

<div style="text-align: center;">
    <img src="../assets/docs/partida.png">
    <p style="font-style: italic; font-size: 12px;">Figura 2. Interface da partida.  </p>
</div>

## Apêndice: Regras do jogo soma 10

O jogo soma 10 consiste na disputa entre dois participantes em um tabuleiro de 16 casas interligadas entre si. O objetivo do jogo é conseguir o maior número de cartas através de somas que resultam em 10.

#### Elementos do jogo

Ao total o baralho conta com 66 cartas enumeradas de 1 a 7, sendo: 

- 18 cartas número 1;
- 18 cartas número 2;
- 14 cartas número 3;
- 8 cartas número 4;
- 4 cartas número 5;
- 2 cartas número 6;
- 2 cartas número 7.

<div style="text-align: center;">
    <img src="../assets/docs/cartas.png">
    <p style="font-style: italic; font-size: 12px;">Figura 3. Cartas do jogo soma 10.  </p>
</div>

#### Como jogar

1. Cada jogador começa a partida com 3 cartas na mão.
2. O jogador escolhe uma de suas cartas para colocar no tabuleiro, depois deve comprar uma nova carta do monte.
3. Ao final de cada rodada, todos os jogadores devem ter exatamente o mesmo número de cartas. Caso um jogador tenha menos cartas, este deverá comprar no monte, se houver, até que seu número de cartas seja igual ao do outro jogador.
4. Se, durante a sua vez, o jogador conseguir somar 10 em uma linha vertical, horizontal ou diagonal, ele recolhe todas as 4 cartas dessa soma.
5. O jogo termina quando um dos competidores não puder mais realizar uma jogada, considerando as regras do jogo. Vence a partida quem possuir o maior número de cartas.

##### Regras adicionais:
- Ao inserir a segunda carta em uma fileira, a soma das duas primeiras cartas deve ser igual ou inferior a 8. Ao adicionar a terceira carta, a soma das três cartas da fileira deve ser igual ou inferior a 9. 

- O competidor que colocar a quarta carta, completando a soma de 10, recolhe todas as cartas daquela fileira e as guarda para a contagem final de pontos. Após isso, a vez passa para o próximo jogador.

- Se um jogador não puder realizar uma jogada com as cartas em sua mão, ele deve comprar uma carta do monte. Caso a nova carta ainda não permita uma jogada, ele deve passar a vez.

- Quando não houver mais cartas no monte, o jogador realiza sua jogada, se possível, e em seguida passa a vez para o próximo jogador.