# Classe NO — representa um único nó da árvore AVL usada no
# índice remissivo.
#
# Cada nó guarda:
#   - palavra : o termo do texto (sempre em minúsculas)
#   - linhas  : lista das linhas do documento em que a palavra
#               foi encontrada (sem repetição de linha)
#   - altura  : altura do nó dentro da árvore (usada para o
#               cálculo do fator de balanceamento da AVL)
#   - esq/dir : referências para os filhos esquerdo e direito

class NO:
    def __init__(self, palavra, linha):
        self.palavra = palavra
        self.linhas = [linha]   # primeira ocorrência da palavra
        self.altura = 0
        self.esq = None
        self.dir = None

    def adicionaLinha(self, linha):
        """Adiciona uma nova linha à lista de ocorrências da palavra,
        evitando duplicar a mesma linha caso a palavra apareça
        mais de uma vez na mesma linha do texto."""
        if linha not in self.linhas:
            self.linhas.append(linha)
            return True   # nova ocorrência registrada
        return False       # mesma linha já estava registrada

    def removeLinha(self, linha):
        """Remove uma linha específica da lista de ocorrências.
        Retorna True se a lista de linhas ficou vazia após a
        remoção (sinal de que o nó inteiro deve ser removido)."""
        if linha in self.linhas:
            self.linhas.remove(linha)
        return len(self.linhas) == 0 #apenas verificação se a lista ficou vazia

    def __repr__(self):
        return f'{self.palavra} {self.linhas}'
