from typing import List, Optional
from datetime import date

# Classe base para representar uma Pessoa
class Pessoa:
    def __init__(self, nome: str, endereco: 'Endereco'):
        self.nome = nome
        self.endereco = endereco

    def __str__(self) -> str:
        return f"{self.nome} - {self.endereco}"

# Classe para representar um Autor
class Autor:
    def __init__(self, nome: str, nacionalidade: str):
        self.nome = nome
        self.nacionalidade = nacionalidade

    def __str__(self) -> str:
        return f"{self.nome} ({self.nacionalidade})"

# Classe para representar uma Categoria de livro
class Categoria:
    def __init__(self, nome: str):
        self.nome = nome

    def __str__(self) -> str:
        return self.nome

# Classe para representar um Endereço
class Endereco:
    def __init__(self, rua: str, numero: int, cidade: str, estado: str, cep: str):
        self.rua = rua
        self.numero = numero
        self.cidade = cidade
        self.estado = estado
        self.cep = cep

    def __str__(self) -> str:
        return f"{self.rua}, {self.numero} - {self.cidade}/{self.estado} - {self.cep}"

# Classe base para representar um Livro
class Livro:
    def __init__(self, titulo: str, autor: Autor, categoria: Categoria, ano_publicacao: int):
        self.titulo = titulo
        self.autor = autor
        self.categoria = categoria
        self.ano_publicacao = ano_publicacao
        self.disponivel = True

    def emprestar(self) -> bool:
        if self.disponivel:
            self.disponivel = False
            return True
        return False

    def devolver(self) -> None:
        self.disponivel = True

    def __str__(self) -> str:
        return f"{self.titulo} por {self.autor} ({self.ano_publicacao}) - Categoria: {self.categoria}"

# Classe derivada para representar um Livro de Ficção
class LivroFiccao(Livro):
    def __init__(self, titulo: str, autor: Autor, categoria: Categoria, ano_publicacao: int, tema: str):
        super().__init__(titulo, autor, categoria, ano_publicacao)
        self.tema = tema

    def __str__(self) -> str:
        return f"{super().__str__()} - Tema: {self.tema}"

# Classe base para representar um Membro
class Membro(Pessoa):
    def __init__(self, nome: str, endereco: Endereco):
        super().__init__(nome, endereco)
        self.emprestimos: List[Livro] = []

    def emprestar_livro(self, livro: Livro) -> bool:
        if livro.emprestar():
            self.emprestimos.append(livro)
            return True
        return False

    def devolver_livro(self, livro: Livro) -> bool:
        if livro in self.emprestimos:
            livro.devolver()
            self.emprestimos.remove(livro)
            return True
        return False

# Classe derivada para representar um Membro Premium
class MembroPremium(Membro):
    def __init__(self, nome: str, endereco: Endereco, limite_emprestimos: int):
        super().__init__(nome, endereco)
        self.limite_emprestimos = limite_emprestimos

    def emprestar_livro(self, livro: Livro) -> bool:
        if len(self.emprestimos) < self.limite_emprestimos:
            return super().emprestar_livro(livro)
        return False

# Classe para representar um Empréstimo
class Emprestimo:
    def __init__(self, livro: Livro, membro: Membro, data_emprestimo: date, data_devolucao: date):
        self.livro = livro
        self.membro = membro
        self.data_emprestimo = data_emprestimo
        self.data_devolucao = data_devolucao

    def __str__(self) -> str:
        return (f"Empréstimo de '{self.livro}' para {self.membro} em {self.data_emprestimo}. "
                f"Devolução prevista para {self.data_devolucao}.")

# Classe para representar a Biblioteca
class Biblioteca:
    def __init__(self):
        self.livros: List[Livro] = []
        self.membros: List[Membro] = []
        self.emprestimos: List[Emprestimo] = []

    def adicionar_livro(self, livro: Livro) -> None:
        self.livros.append(livro)

    def adicionar_membro(self, membro: Membro) -> None:
        self.membros.append(membro)

    def registrar_emprestimo(self, livro: Livro, membro: Membro, data_emprestimo: date, data_devolucao: date) -> Optional[Emprestimo]:
        if livro in self.livros and membro in self.membros:
            if membro.emprestar_livro(livro):
                emprestimo = Emprestimo(livro, membro, data_emprestimo, data_devolucao)
                self.emprestimos.append(emprestimo)
                return emprestimo
        return None

    def encontrar_livro(self, titulo: str) -> Optional[Livro]:
        for livro in self.livros:
            if livro.titulo == titulo:
                return livro
        return None

    def encontrar_membro(self, nome: str) -> Optional[Membro]:
        for membro in self.membros:
            if membro.nome == nome:
                return membro
        return None

    def __str__(self) -> str:
        return (f"Biblioteca com {len(self.livros)} livros, "
                f"{len(self.membros)} membros e "
                f"{len(self.emprestimos)} empréstimos.")

# Exemplo de uso
if __name__ == "__main__":
    autor = Autor("J.K. Rowling", "Britânica")
    categoria = Categoria("Ficção Fantástica")
    endereco = Endereco("Rua das Flores", 123, "São Paulo", "SP", "01234-567")

    livro = LivroFiccao("Harry Potter e a Pedra Filosofal", autor, categoria, 1997, "Magia")
    membro = MembroPremium("João Silva", endereco, limite_emprestimos=5)

    biblioteca = Biblioteca()
    biblioteca.adicionar_livro(livro)
    biblioteca.adicionar_membro(membro)

    print(biblioteca)

    emprestimo = biblioteca.registrar_emprestimo(livro, membro, date(2024, 9, 16), date(2024, 10, 16))
    if emprestimo:
        print(f"Empréstimo registrado: {emprestimo}")

    print(membro)
    print(livro)
    
    if membro.devolver_livro(livro):
        print(f"{membro.nome} devolveu {livro.titulo}")
    
    print(biblioteca)
