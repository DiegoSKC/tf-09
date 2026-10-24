from abc import ABC, abstractmethod


class Medivel(ABC):
    __slots__ = ()

    @abstractmethod
    def tamanho(self):
        pass


class Item(Medivel):
    __slots__ = ("__nome", "__pai")

    def __init__(self, nome, pai=None):
        self.__validar_nome(nome)
        self.__nome = nome
        self.__pai = None

        if pai is not None:
            self.mover_para(pai)

    def __validar_nome(self, nome):
        if nome == "" or "/" in nome:
            raise ValueError("nome inválido: " + repr(nome))

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, novo_nome):
        self.__validar_nome(novo_nome)
        self.__nome = novo_nome

    @property
    def pai(self):
        return self.__pai

    def mover_para(self, destino):
        if destino is self.__pai:
            return

        destino._receber(self)

        if self.__pai is not None:
            self.__pai._soltar(self)

        self.__pai = destino

    def _receber(self, item):
        raise ValueError(self.__nome + " é um arquivo, não pode conter itens")

    def caminho(self):
        if self.__pai is None:
            return self.__nome
        return self.__pai.caminho() + "/" + self.__nome

    def profundidade(self):
        if self.__pai is None:
            return 0
        return self.__pai.profundidade() + 1

    @abstractmethod
    def mostrar(self):
        pass


class Arquivo(Item):
    __slots__ = ("__bytes",)

    def __init__(self, nome, tamanho_bytes, pai=None):
        if tamanho_bytes < 0:
            raise ValueError("tamanho não pode ser negativo")

        self.__bytes = tamanho_bytes
        super().__init__(nome, pai)

    def tamanho(self):
        return self.__bytes

    def mostrar(self):
        recuo = "    " * self.profundidade()
        print(recuo + self.nome + " (" + str(self.tamanho()) + " B)")


class Pasta(Item):
    __slots__ = ("__filhos",)

    def __init__(self, nome, pai=None):
        self.__filhos = []
        super().__init__(nome, pai)

    @property
    def filhos(self):
        return tuple(self.__filhos)

    def _receber(self, item):
        ancestral = self

        while ancestral is not None:
            if ancestral is item:
                raise ValueError(
                    "não dá para mover " + item.nome + " para dentro dela mesma"
                )
            ancestral = ancestral.pai

        self.__filhos.append(item)

    def _soltar(self, item):
        self.__filhos.remove(item)

    def tamanho(self):
        total = 0

        for filho in self.__filhos:
            total = total + filho.tamanho()

        return total

    def mostrar(self):
        recuo = "    " * self.profundidade()
        print(recuo + self.nome + "/ (" + str(self.tamanho()) + " B)")

        for filho in self.__filhos:
            filho.mostrar()


class Lixeira(Medivel):
    __slots__ = ("__descartados",)

    def __init__(self):
        self.__descartados = []

    def descartar(self, arquivo):
        self.__descartados.append(arquivo)

    def tamanho(self):
        total = 0

        for arquivo in self.__descartados:
            total = total + arquivo.tamanho()

        return total


def espaco_total(coisas):
    total = 0

    for coisa in coisas:
        total = total + coisa.tamanho()

    return total


def tentar(rotulo, acao):
    try:
        acao()
        print(rotulo, "-> passou (!)")
    except Exception as erro:
        print(rotulo, "->", type(erro).__name__ + ":", erro)


class Atalho(Item):
    __slots__ = ("__destino",)

    def __init__(self, nome, destino, pai=None):
        self.__destino = None
        super().__init__(nome, pai)
        self.redirecionar(destino)

    @property
    def destino(self):
        return self.__destino

    def redirecionar(self, novo_destino):
        if novo_destino is self:
            raise ValueError("um atalho não pode apontar para si mesmo")

        ancestral = self.pai

        while ancestral is not None:
            if ancestral is novo_destino:
                raise ValueError(
                    "um atalho não pode apontar para uma pasta que o contém"
                )
            ancestral = ancestral.pai

        self.__destino = novo_destino

    def tamanho(self):
        return 1

    def mostrar(self):
        recuo = "    " * self.profundidade()
        print(recuo + self.nome + " -> " + self.destino.caminho())


disco = Pasta("C:")
usuarios = Pasta("Users", disco)
usuario = Pasta("Diego", usuarios)
desktop = Pasta("Desktop", usuario)
trabalhos = Pasta("Trabalhos", desktop)

arquivo_texto = Arquivo("anotacoes.txt", 120, desktop)
arquivo_codigo = Arquivo("projeto.py", 800, trabalhos)
arquivo_pdf = Arquivo("aula.pdf", 5000, trabalhos)

atalho_arquivo = Atalho("atalho_anotacoes", arquivo_texto, desktop)
atalho_pasta = Atalho("atalho_trabalhos", trabalhos, desktop)

disco.mostrar()

lixeira = Lixeira()
lixeira.descartar(Arquivo("rascunho.txt", 40))

print(
    "Espaço total:",
    espaco_total([arquivo_texto, trabalhos, lixeira])
)

tentar(
    "Alterar destino diretamente",
    lambda: setattr(atalho_arquivo, "destino", arquivo_pdf)
)

tentar(
    "Atalho apontando para si mesmo",
    lambda: atalho_arquivo.redirecionar(atalho_arquivo)
)

tentar(
    "Atalho apontando para a pasta que o contém",
    lambda: atalho_arquivo.redirecionar(desktop)
)
