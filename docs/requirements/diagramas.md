# Diagramas

## Adaptações e Considerações
Levando em conta a necessidade de refator o código originalmente em Java para Python é importante ter algumas considerações sobre alguns conceitos das linguagens.

| Conceito              | Java                                           | Python                                                |
| --------------------- | ---------------------------------------------- | ----------------------------------------------------- |
| Encapsulamento        | Modificadores `private`, `protected`, `public` | Convenções: `_protegido`, `__privado` (name mangling) |
| Tipagem               | Estática                                       | Dinâmica (mas pode usar type hints)                   |
| Pacotes/modularização | `package`, estrutura rígida                    | Módulos (`.py`) e pacotes (pastas com `__init__.py`)  |
| MVC Formal            | Usa diagramas de pacotes/arquitetura formal    | Python tende a ter arquitetura mais leve e flexível   |

## Diagrama UML
```mermaid
classDiagram
    %% Classe base
    class Usuario {
        _id_usuario: int
        _nome: str
        _email: str
        _senha: str
        _enderecos: list
        _telefones: list
        +login()
        +logout()
        +editar_perfil()
    }

    class Cliente {
        +visualizar_produtos()
        +realizar_compra()
        +rastrear_pedido()
    }

    class Vendedor {
        +criar_loja()
        +cadastrar_produto()
        +confirmar_venda()
        +notificar_envio()
    }

    class Loja {
        _id_loja: int
        _nome_loja: str
        _produtos: list
        _vendedor: Vendedor
        +editar_loja()
    }

    class Produto {
        _id_produto: int
        _nome: str
        _descricao: str
        _preco: float
        _estoque: int
        _categoria: str
        +atualizar_estoque()
    }

    class Carrinho {
        _itens: list
        +adicionar_item()
        +remover_item()
        +calcular_total()
    }

    class Pedido {
        _id_pedido: int
        _cliente: Cliente
        _produtos: list
        _status: str
        +atualizar_status()
    }

    class Pagamento {
        _metodos_pagamento: list
        +escolher_metodo()
    }

    class ContaBancaria {
        _banco: str
        _numero_conta: str
        +validar_dados()
    }

    %% Relações
    Usuario <|-- Cliente
    Usuario <|-- Vendedor
    Cliente --> Carrinho
    Carrinho --> Produto
    Cliente --> Pedido
    Pedido --> Produto
    Pedido --> Pagamento
    Vendedor --> ContaBancaria
    Vendedor --> Loja
    Loja --> Produto



```

## Estrutura

```
project/
├── app/
│   ├── controllers/ 
│   ├── models/ 
│   ├── views/ 
├── static/
├── tests/ 
├── main.py
```
