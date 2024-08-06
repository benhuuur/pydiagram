# Classe base
class Animal:
    def __init__(self, nome):
        self.nome = nome

    def fazer_som(self):
        raise NotImplementedError("Esse método deve ser sobrescrito na classe filha")

# Classe derivada
class Cachorro(Animal):
    def fazer_som(self):
        return "Au Au!"

# Classe derivada
class Gato(Animal):
    def fazer_som(self):
        return "Miau!"