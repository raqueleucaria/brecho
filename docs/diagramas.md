# Diagramas

## Adaptações e Considerações
Levando em conta a necessidade de refator o código originalmente em Java para Python é importante ter algumas considerações sobre alguns conceitos das linguagens.

| Conceito              | Java                                           | Python                                                |
| --------------------- | ---------------------------------------------- | ----------------------------------------------------- |
| Encapsulamento        | Modificadores `private`, `protected`, `public` | Convenções: `_protegido`, `__privado` (name mangling) |
| Tipagem               | Estática                                       | Dinâmica (mas pode usar type hints)                   |
| Pacotes/modularização | `package`, estrutura rígida                    | Módulos (`.py`) e pacotes (pastas com `__init__.py`)  |
| MVC Formal            | Usa diagramas de pacotes/arquitetura formal    | Python tende a ter arquitetura mais leve e flexível   |

## Diagrama UML Ajustado (com base no MER e backlog)
```mermaid
classDiagram
    %% Classes principais
    class Usuario {
        -user_id: int
        -nome: str
        -email: str
        -senha: str
        -telefone: list
        -enderecos: list
        +login()
        +logout()
        +editar_perfil()
    }

    class Cliente {
        +visualizar_produtos()
        +adicionar_favorito()
        +visualizar_favoritos()
        +realizar_compra()
        +rastrear_pedido()
    }

    class Vendedor {
        +criar_loja()
        +cadastrar_produto()
        +editar_produto()
        +confirmar_venda()
        +notificar_envio()
    }

    class Loja {
        -store_id: int
        -status: str
        -produtos: list
        +ativar()
        +desativar()
    }

    class Produto {
        -product_id: int
        -nome: str
        -descricao: str
        -preco: float
        -categoria: str
        -tamanho: str
        -cor: str
        +atualizar_estoque()
    }

    class Carrinho {
        -itens: list
        +adicionar_item()
        +remover_item()
        +calcular_total()
    }

    class Pedido {
        -order_id: int
        -produtos: list
        -status: str
        +confirmar()
        +cancelar()
    }

    class Pagamento {
        -payment_id: int
        -tipo: str
        -status: str
        +escolher_metodo()
        +confirmar()
    }

    class Cartao {
        -card_id: int
        -numero: str
        -titular: str
        -validade: str
        -cvv: str
    }

    class ContaBancaria {
        -bank_id: int
        -banco: str
        -agencia: str
        -conta: str
        -tipo: str
    }

    class Rastreio {
        -tracking_id: int
        -status: str
        -localizacao: str
        -data: datetime
    }

    class Notificacao {
        -notification_id: int
        -status: str
        -enviada_em: datetime
    }

    class Favorito {
        -user_id: int
        -product_id: int
    }

    %% Relações
    Usuario <|-- Cliente
    Usuario <|-- Vendedor
    Cliente --> Carrinho
    Cliente --> Pedido
    Cliente --> Favorito
    Favorito --> Produto
    Carrinho --> Produto
    Pedido --> Produto
    Pedido --> Pagamento
    Pedido --> Rastreio
    Vendedor --> ContaBancaria
    Vendedor --> Loja
    Loja --> Produto
    Pedido --> Notificacao
    Pagamento --> Cartao
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
