# Casos de Uso

## [UC01] Cadastro de Usuário

| **ID**  | **UC01**                                              |
|---------|--------------------------------------------------------|
| **Ator** | Usuário                                                |
| **Descrição** | O usuário preenche um formulário com dados pessoais como nome, e-mail e senha para criar uma conta no sistema. |
| **Fluxo Principal** | 1. O usuário acessa a tela de cadastro. <br> 2. O usuário preenche seus dados pessoais. <br> 3. O sistema valida os dados e cria a conta. <br> 4. O sistema envia um e-mail de confirmação de cadastro. <br> 5. O usuário é redirecionado para a tela de login. |


## [UC02] Login

| **ID**  | **UC02**                                              |
|---------|--------------------------------------------------------|
| **Ator** | Usuário                                                |
| **Descrição** | O usuário realiza o login no sistema com seu e-mail e senha. |
| **Fluxo Principal** | 1. O usuário acessa a tela de login. <br> 2. O usuário insere e-mail e senha. <br> 3. O sistema valida os dados e, se corretos, autentica o usuário. <br> 4. O usuário é redirecionado para a tela inicial. |

## [UC03] Logout

| **ID**  | **UC03**                                              |
|---------|--------------------------------------------------------|
| **Ator** | Usuário                                                |
| **Descrição** | O usuário faz logout do sistema para encerrar a sessão. |
| **Fluxo Principal** | 1. O usuário clica no botão de logout. <br> 2. O sistema encerra a sessão do usuário e o redireciona para a tela de login. |


## [UC04] Edição de Perfil

| **ID**  | **UC04**                                              |
|---------|--------------------------------------------------------|
| **Ator** | Usuário                                                |
| **Descrição** | O usuário pode alterar suas informações pessoais. |
| **Fluxo Principal** | 1. O usuário acessa a tela de edição de perfil. <br> 2. O usuário edita suas informações pessoais. <br> 3. O sistema valida e atualiza os dados no banco de dados. |

## [UC05] Cadastro de Endereço

| **ID**  | **UC05**                                              |
|---------|--------------------------------------------------------|
| **Ator** | Usuário                                                |
| **Descrição** | O usuário pode cadastrar um novo endereço para entrega. |
| **Fluxo Principal** | 1. O usuário acessa a tela de cadastro de endereço. <br> 2. O usuário preenche o formulário com os dados de endereço. <br> 3. O sistema valida e salva o endereço no banco de dados. |

## [UC06] Edição de Endereço

| **ID**  | **UC06**                                              |
|---------|--------------------------------------------------------|
| **Ator** | Usuário                                                |
| **Descrição** | O usuário pode editar um endereço cadastrado. |
| **Fluxo Principal** | 1. O usuário acessa a lista de endereços cadastrados. <br> 2. O usuário seleciona um endereço para editar. <br> 3. O usuário altera os dados e salva as mudanças. |

## [UC07] Exclusão de Endereço

| **ID**  | **UC07**                                              |
|---------|--------------------------------------------------------|
| **Ator** | Usuário                                                |
| **Descrição** | O usuário pode excluir um endereço cadastrado. |
| **Fluxo Principal** | 1. O usuário acessa a lista de endereços cadastrados. <br> 2. O usuário seleciona um endereço para excluir. <br> 3. O sistema confirma a exclusão e remove o endereço. |

## [UC08] Cadastro de Telefone

| **ID**  | **UC08**                                              |
|---------|--------------------------------------------------------|
| **Ator** | Usuário                                                |
| **Descrição** | O usuário pode cadastrar múltiplos números de telefone. |
| **Fluxo Principal** | 1. O usuário acessa a tela de cadastro de telefone. <br> 2. O usuário preenche o número de telefone. <br> 3. O sistema valida e salva o número no banco de dados. |

## [UC09] Edição de Telefone

| **ID**  | **UC09**                                              |
|---------|--------------------------------------------------------|
| **Ator** | Usuário                                                |
| **Descrição** | O usuário pode editar um número de telefone cadastrado. |
| **Fluxo Principal** | 1. O usuário acessa a lista de telefones cadastrados. <br> 2. O usuário seleciona um telefone para editar. <br> 3. O usuário altera o número e salva a alteração. |

## [UC10] Exclusão de Telefone

| **ID**  | **UC10**                                              |
|---------|--------------------------------------------------------|
| **Ator** | Usuário                                                |
| **Descrição** | O usuário pode excluir um número de telefone cadastrado. |
| **Fluxo Principal** | 1. O usuário acessa a lista de telefones cadastrados. <br> 2. O usuário seleciona um telefone para excluir. <br> 3. O sistema confirma a exclusão e remove o número. |

## [UC11] Cadastro de Pagamento

| **ID**  | **UC11**                                              |
|---------|--------------------------------------------------------|
| **Ator** | Usuário (Cliente)                                      |
| **Descrição** | O cliente pode cadastrar um método de pagamento, como cartão de crédito. |
| **Fluxo Principal** | 1. O cliente acessa a tela de cadastro de pagamento. <br> 2. O cliente preenche os dados do cartão de crédito. <br> 3. O sistema valida e salva os dados de pagamento. |

## [UC12] Edição de Pagamento

| **ID**  | **UC12**                                              |
|---------|--------------------------------------------------------|
| **Ator** | Usuário (Cliente)                                      |
| **Descrição** | O cliente pode editar um método de pagamento previamente cadastrado. |
| **Fluxo Principal** | 1. O cliente acessa a lista de métodos de pagamento cadastrados. <br> 2. O cliente seleciona um método de pagamento para editar. <br> 3. O cliente altera os dados e salva as alterações. |

## [UC13] Exclusão de Pagamento

| **ID**  | **UC13**                                              |
|---------|--------------------------------------------------------|
| **Ator** | Usuário (Cliente)                                      |
| **Descrição** | O cliente pode excluir um método de pagamento. |
| **Fluxo Principal** | 1. O cliente acessa a lista de métodos de pagamento. <br> 2. O cliente seleciona um método de pagamento para excluir. <br> 3. O sistema confirma a exclusão e remove o método de pagamento. |

## [UC14] Escolher Método de Pagamento

| **ID**  | **UC14**                                              |
|---------|--------------------------------------------------------|
| **Ator** | Usuário (Cliente)                                      |
| **Descrição** | O cliente escolhe um método de pagamento durante o checkout. |
| **Fluxo Principal** | 1. O cliente acessa a página de checkout. <br> 2. O cliente escolhe um método de pagamento da lista de opções. <br> 3. O sistema processa o pagamento e finaliza a compra. |

## [UC15] Gerenciamento do Carrinho

| **ID**  | **UC15**                                              |
|---------|--------------------------------------------------------|
| **Ator** | Usuário (Cliente)                                      |
| **Descrição** | O cliente pode adicionar e remover itens do carrinho de compras. |
| **Fluxo Principal** | 1. O cliente visualiza o carrinho. <br> 2. O cliente adiciona ou remove itens do carrinho. <br> 3. O sistema atualiza o carrinho com os itens escolhidos. |

## [UC16] Análise de Compra

| **ID**  | **UC16**                                              |
|---------|--------------------------------------------------------|
| **Ator** | Usuário (Cliente)                                      |
| **Descrição** | O cliente pode visualizar o total da compra, incluindo o valor do frete, antes de confirmar a compra. |
| **Fluxo Principal** | 1. O cliente visualiza o total do carrinho com frete. <br> 2. O cliente confirma a compra e escolhe a forma de pagamento. |

## [UC17] Acompanhamento de Pedido

| **ID**  | **UC17**                                              |
|---------|--------------------------------------------------------|
| **Ator** | Usuário (Cliente)                                      |
| **Descrição** | O cliente pode acompanhar o status de seu pedido. |
| **Fluxo Principal** | 1. O cliente acessa a página de acompanhamento de pedidos. <br> 2. O sistema exibe o status atual do pedido (preparando, enviado, entregue, etc.). |

## [UC18] Cadastro de Loja

| **ID**  | **UC18**                                              |
|---------|--------------------------------------------------------|
| **Ator** | Vendedor                                               |
| **Descrição** | O vendedor cria sua loja para começar a vender produtos. |
| **Fluxo Principal** | 1. O vendedor acessa a tela de criação de loja. <br> 2. O vendedor preenche o nome e informações da loja. <br> 3. O sistema cria a loja e confirma a operação. |

## [UC19] Edição de Loja
| **ID**              | **UC19**                                                                                                                                                                     |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Ator**            | Vendedor                                                                                                                                                                     |
| **Descrição**       | O vendedor pode editar as informações de sua loja.                                                                                                                           |
| **Fluxo Principal** | 1. O vendedor acessa as configurações de sua loja. <br> 2. O vendedor edita informações como nome, descrição e logo da loja. <br> 3. O sistema valida e salva as alterações. |

## [UC20] Gerenciamento de Produtos
| **ID**              | **UC20**                                                                                                                                                                                             |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Ator**            | Vendedor                                                                                                                                                                                             |
| **Descrição**       | O vendedor pode cadastrar, editar ou excluir produtos na loja.                                                                                                                                       |
| **Fluxo Principal** | 1. O vendedor acessa a tela de gerenciamento de produtos. <br> 2. O vendedor cadastra ou edita informações sobre um produto. <br> 3. O sistema valida e salva os dados do produto no banco de dados. |

## [UC21] Confirmação de Venda
| **ID**              | **UC21**                                                                                                                                                         |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Ator**            | Vendedor                                                                                                                                                         |
| **Descrição**       | O vendedor confirma uma venda para iniciar o processo de envio.                                                                                                  |
| **Fluxo Principal** | 1. O vendedor acessa a lista de pedidos. <br> 2. O vendedor confirma que a venda foi realizada. <br> 3. O sistema atualiza o status do pedido para "confirmado". |

## [UC22] Notificação de Envio
| **ID**              | **UC22**                                                                                                                        |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| **Ator**            | Vendedor                                                                                                                        |
| **Descrição**       | O vendedor envia uma notificação ao cliente informando que o pedido foi enviado.                                                |
| **Fluxo Principal** | 1. O vendedor acessa o pedido. <br> 2. O vendedor clica em "notificar envio". <br> 3. O sistema envia a notificação ao cliente. |

## [UC23] Cadastro de Conta Bancária
| **ID**              | **UC23**                                                                                                                                                                                     |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Ator**            | Vendedor                                                                                                                                                                                     |
| **Descrição**       | O vendedor cadastra sua conta bancária para receber pagamentos.                                                                                                                              |
| **Fluxo Principal** | 1. O vendedor acessa a tela de cadastro de conta bancária. <br> 2. O vendedor preenche os dados da conta (banco, número, etc.). <br> 3. O sistema valida e salva os dados da conta bancária. |
