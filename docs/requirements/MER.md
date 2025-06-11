# Modelo Entidade Relacionamento

## Entidades

- USUARIO
- ENDERECO
- LOJA
- PRODUTO
- CARRINHO
- PEDIDO
- PAGAMENTO
- CARTAO
- CONTA_BANCARIA
- VENDA
- NOTIFICACAO

## Atributos

- **USUARIO** (<u>idUsuario</u>, nome, email, senha, dataCriacao, ddd, numero)
- **ENDERECO** (<u>idEndereco</u>, idUsuario, cep, estado, cidade, bairro, rua, numero, complemento)
- **LOJA** (<u>idLoja</u>, idUsuario, dataCriacao, status)
- **PRODUTO** (<u>idProduto</u>, idLoja, nome, descricao, preco, quantidade, categoria, tamanho, cor)
- **CARRINHO** (<u>idCarrinho</u>, idUsuario, {idProduto}, dataCriacao)
- **PEDIDO** (<u>idPedido</u>, idUsuario, idEndereco, status, dataPedido, {idProduto})
- **PAGAMENTO** (<u>idPagamento</u>, idPedido, tipo, status, dataPagamento)
  - **PAGAMENTO_PIX** (<u>idPagamento</u>, chavePix, comprovante)
  - **PAGAMENTO_BOLETO** (<u>idPagamento</u>, codigoBarras, dataVencimento, linhaDigitavel)
  - **PAGAMENTO_CARTAO** (<u>idPagamento</u>, idCartao)
- **CARTAO** (<u>idCartao</u>, idUsuario, numero, nomeTitular, validade, cvv, cpfTitular)
- **CONTA_BANCARIA** (<u>idContaBancaria</u>, idLoja, banco, agencia, conta, tipo)
- **VENDA** (<u>idVenda</u>, idLoja, idPedido, dataVenda, status)
- **NOTIFICACAO** (<u>idNotificacao</u>, idVenda, status, dataEnvio)

## Relacionamentos

- USUARIO **possui** ENDERECO  
  <br> Um USUARIO possui um ou vários ENDERECO(s) (1:N)

- USUARIO **tem** LOJA  
  <br> Um USUARIO pode ter nenhuma ou uma LOJA (0:1)

- LOJA **vende** PRODUTO  
  <br> Uma LOJA vende nenhum ou vários PRODUTO(s) (0:N)

- USUARIO **cria** CARRINHO  
  <br> Um USUARIO cria nenhum ou um CARRINHO(s) (0:1)

- USUARIO **realiza** PEDIDO  
  <br> Um USUARIO realiza nenhum ou vários PEDIDO(s) (0:N)

- PEDIDO **validado_por** PAGAMENTO 
  <br> Um PEDIDO é validado por um PAGAMENTO (1:1)

- USUARIO **salva** CARTAO  
  <br> Um USUARIO pode salvar nenhum ou vários CARTAO(s) (0:N)

- LOJA **cadastra** CONTA_BANCARIA  
  <br> Uma LIJA possui uma CONTA_BANCARIA (1:1)

- LOJA **realiza** VENDA  
  <br> Uma LOJA realiza uma ou várias VENDA(s) (1:N)

- VENDA **gera** NOTIFICACAO  
  <br> Uma VENDA pode gerar uma ou várias NOTIFICACAO(ões) (1:N)