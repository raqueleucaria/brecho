# Arquitetura recomendada para APIs FastAPI

O projeto segue uma arquitetura modular, baseada em boas práticas de Clean Code, Domain Driven Design (DDD) e recomendações oficiais do [FastAPI](https://fastapi.tiangolo.com/tutorial/bigger-applications/). O uso do [Poetry](https://python-poetry.org/) para gerenciamento de dependências reforça a organização e reprodutibilidade do ambiente.

No contexto dos testes, utilizamos o **factory-boy** para facilitar a criação de dados de teste. Essa biblioteca permite gerar instâncias de modelos (como usuários, produtos, endereços, etc.) de forma automatizada e flexível, tornando os testes mais limpos, reutilizáveis e fáceis de manter. Com factories, é possível simular cenários variados e garantir que cada teste tenha dados isolados e consistentes, seguindo as melhores práticas de Clean Code e arquitetura.

## Camadas e Motivos

- **`model/`**  
Contém as entidades do domínio e o mapeamento ORM (SQLAlchemy). Cada classe representa uma tabela do banco e seus relacionamentos.  
*Referência:* [DDD - Entities](https://martinfowler.com/bliki/Entity.html)  
*Motivo:* Centraliza a lógica de dados e facilita a manutenção do modelo de negócio.

- **`schema/`**  
Define os contratos de dados (DTOs) usando Pydantic. Os schemas são usados para validação, serialização e documentação automática dos endpoints.  
*Referência:* [FastAPI - Pydantic Models](https://fastapi.tiangolo.com/tutorial/body/)  
*Motivo:* Garante que os dados recebidos e enviados pela API estejam sempre corretos e bem definidos.

- **`repository/`**  
Isola a lógica de acesso ao banco de dados (CRUD, queries complexas). Cada repositório manipula uma entidade específica.  
*Referência:* [Repository Pattern](https://martinfowler.com/eaaCatalog/repository.html)  
*Motivo:* Reduz o acoplamento entre regras de negócio e persistência, facilitando testes e refatorações.

- **`service/`**  
Implementa as regras de negócio e orquestra operações entre repositórios. Serviços podem ser reutilizados por diferentes rotas e facilitam a separação entre lógica de negócio e apresentação.  
*Referência:* [Service Layer Pattern](https://martinfowler.com/eaaCatalog/serviceLayer.html)  
*Motivo:* Mantém a lógica de negócio centralizada, evitando duplicidade e facilitando a evolução do sistema.

- **`router/`**  
Define os endpoints da API, conectando as rotas aos serviços. Cada router trata um contexto (ex: usuário, produto, pagamento), tornando o código mais organizado e legível.  
*Referência:* [FastAPI - Routers](https://fastapi.tiangolo.com/tutorial/bigger-applications/#apirouter)  
*Motivo:* Facilita a navegação e manutenção dos endpoints, além de permitir o versionamento e modularização da API.

- **`tests/`**  
Testes unitários e de integração, separados por contexto. O uso de factories (factory-boy) torna a criação dos dados de teste mais eficiente e alinhada com boas práticas.  
*Referência:* [Testing Python Applications](https://docs.pytest.org/en/latest/)  
*Motivo:* Garante qualidade e segurança nas mudanças do código.

## Clean Code e Arquitetura

- **Baixo acoplamento:** Cada camada depende apenas da anterior, facilitando testes e refatorações ([Clean Architecture](https://8thlight.com/blog/uncle-bob/2012/08/13/the-clean-architecture.html)).
- **Alta coesão:** Cada pasta agrupa arquivos com propósito único.
- **Testabilidade:** Separação clara permite testes unitários e de integração eficientes.
- **Escalabilidade:** Adicionar novas features é simples e não afeta outras partes do sistema.

## Poetry

O [Poetry](https://python-poetry.org/docs/) é recomendado para gerenciamento de dependências e ambientes virtuais, garantindo reprodutibilidade, facilidade de deploy e atualização segura de pacotes.

## Resumo

Essa arquitetura torna o projeto organizado, escalável, testável e fácil de manter, seguindo recomendações do FastAPI, Clean Code e padrões clássicos de arquitetura de software. Cada camada tem responsabilidade única e clara, facilitando o trabalho em equipe e a evolução do sistema.
