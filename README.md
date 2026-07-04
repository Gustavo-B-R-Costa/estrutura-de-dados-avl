Índice Remissivo com Árvore AVL

Projeto desenvolvido para a disciplina de Estrutura de Dados do curso de Gestão da Informação (UFU).

O objetivo deste trabalho é construir automaticamente um índice remissivo de um arquivo de texto utilizando uma árvore AVL, permitindo armazenar as palavras em ordem alfabética e registrar em quais linhas cada uma delas aparece.

---

# Objetivo

O programa lê um arquivo de texto linha por linha, identifica todas as palavras presentes e cria um índice remissivo semelhante ao encontrado no final de livros.
Por exemplo, se o texto possuir as seguintes linhas:

```
1. Python é uma linguagem.
2. A árvore AVL é balanceada.
3. Python é muito utilizada.
```

O índice gerado será semelhante a:

```
a 2
avl 2
balanceada 2
é 1,2,3
linguagem 1
muito 3
python 1,3
utilizada 3
árvore 2
```

Cada palavra aparece apenas uma vez e, ao lado dela, são mostradas as linhas onde ela ocorre.

---

# Estrutura do projeto

```
indice-remissivo-avl/
│
├── main.py               # Programa principal
├── avl.py                # Implementação da árvore AVL
├── no.py                 # Classe que representa um nó da árvore
├── texto_origem.txt      # Arquivo de entrada (Nesse caso Dom_Casmurro.txt)
├── indice_remissivo.txt  # Arquivo gerado pelo programa
└── README.md
```

---

# Como funciona

O funcionamento do programa pode ser dividido em quatro etapas.

# 1. Leitura do arquivo

O arquivo de texto é lido linha por linha.
Cada linha é processada por uma expressão regular que extrai apenas palavras, ignorando números e sinais de pontuação.
Além disso, todas as palavras são convertidas para letras minúsculas para evitar diferenças entre, por exemplo:

```
Python
python
PYTHON
```

Todas passam a ser tratadas como:

```
python
```

---

# 2. Construção da árvore AVL

Cada palavra encontrada é inserida na árvore AVL.
Se a palavra ainda não existir, um novo nó é criado.
Se ela já existir, apenas a linha onde foi encontrada é adicionada à lista de ocorrências daquela palavra.
Cada nó da árvore armazena:
- a palavra;
- a lista das linhas em que ela aparece;
- a altura do nó;
- referências para os filhos esquerdo e direito.

---

# 3. Balanceamento

Após cada inserção ou remoção, a árvore verifica se continua balanceada.
Caso seja necessário, são executadas rotações AVL (LL, RR, LR ou RL).
Isso garante que as operações continuem eficientes mesmo para arquivos grandes.

---

# 4. Geração do índice

Depois que todas as palavras são inseridas, é feito um percurso em ordem.
Como uma árvore AVL também é uma árvore binária de busca, esse percurso percorre os nós em ordem alfabética.
As informações são gravadas no arquivo `indice_remissivo.txt`.
No final do arquivo também são exibidas algumas estatísticas sobre a construção do índice.

---

# Funcionalidades implementadas

O projeto possui as seguintes operações:

- Inserção de palavras
- Busca por palavra
- Busca por prefixo
- Remoção de ocorrências
- Palavra mais frequente
- Medidor de equilíbrio
- Geração do índice remissivo

---

# Explicação das principais funções

# Inserção

Quando uma palavra é encontrada no texto, ela é inserida na árvore.
Se a palavra ainda não existir:

```
python
```

é criado um novo nó.
Caso ela já exista não é criado outro nó.
Apenas a linha é adicionada à lista de ocorrências.

---

# Busca

A busca segue exatamente o funcionamento de uma árvore binária de busca.
Se a palavra procurada for menor que a palavra atual, a busca continua pela esquerda.
Se for maior, continua pela direita.
Quando encontra a palavra, retorna a lista de linhas onde ela aparece.

---

# Palavra mais frequente

Percorre toda a árvore e verifica qual palavra aparece no maior número de linhas diferentes.
Durante o percurso são mantidas duas variáveis:

- melhor palavra encontrada até o momento;
- maior quantidade de linhas encontrada.

Sempre que uma palavra possui mais ocorrências do que a melhor atual, essas variáveis são atualizadas.

---

# Remoção

A remoção acontece em duas etapas.
Primeiro é removida apenas a linha da lista de ocorrências.
Somente quando a lista fica vazia o nó inteiro é removido da árvore.
Após isso, a AVL atualiza as alturas e faz o rebalanceamento, caso seja necessário.

---

# Percurso em ordem

O índice é gerado utilizando um percurso em ordem.
A ordem de visita é:
Esquerda, Nó atual, Direita
Como toda árvore AVL segue as regras de uma árvore binária de busca, esse percurso produz automaticamente as palavras em ordem alfabética.

---

# Estruturas utilizadas

Durante o desenvolvimento foram utilizadas:

- Classes
- Objetos
- Recursão
- Listas
- Expressões regulares
- Manipulação de arquivos
- Árvore AVL

---

# Estatísticas geradas

Ao final da execução, o programa informa:

- Número total de palavras processadas;
- Número de palavras distintas;
- Quantidade de palavras repetidas;
- Tempo gasto para construir a árvore;
- Quantidade de rotações executadas.

Exemplo:

Número total de palavras: 1897
Número de palavras distintas: 698
Número de palavras descartadas: 1199
Tempo de construção do índice usando árvore AVL: 0.0078 s
Total de rotações executadas: 527

---

# Como executar

Clone o repositório:

```bash
git clone https://github.com/seu-usuario/indice-remissivo-avl.git
```

Entre na pasta:

```bash
cd indice-remissivo-avl
```

Execute:

```bash
python main.py
```

Ao final será criado automaticamente o arquivo:
indice_remissivo.txt
---

# O que foi aprendido

Durante o desenvolvimento deste projeto foi possível praticar diversos conceitos vistos na disciplina, como:

- implementação de árvores AVL;
- rotações para balanceamento;
- inserção e remoção em árvores binárias de busca;
- utilização de recursão para percorrer árvores;
- leitura e escrita de arquivos texto;
- uso de expressões regulares para extração de palavras;
- organização de um projeto em diferentes módulos.

Além disso, o projeto mostrou na prática a principal vantagem de uma árvore AVL: manter a árvore balanceada automaticamente, garantindo que operações como inserção, busca e remoção permaneçam eficientes mesmo quando a quantidade de palavras cresce bastante.

---

Aluno: Gustavo Borges Rodrigues Costa
Curso de Gestão da Informação – Universidade Federal de Uberlândia (UFU)