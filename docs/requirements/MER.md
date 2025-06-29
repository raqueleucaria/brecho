# Entity-Relationship Model

## Entities

- USER
- ADDRESS
- STORE
- PRODUCT
- CART
- ORDER
- PAYMENT
- CARD
- BANK_ACCOUNT
- SALE
- NOTIFICATION

## Attributes

- **USER** (<u>userId</u>, name, email, password, createdAt, phone(ddd, phoneNumber))
- **ADDRESS** (<u>addressId</u>, userId, zipCode, state, city, district, street, number, complement)
- **STORE** (<u>storeId</u>, userId, createdAt, status)
- **PRODUCT** (<u>productId</u>, storeId, name, description, price, quantity, category, size, color)
- **CART** (<u>cartId</u>, userId, {productId}, createdAt)
- **ORDER** (<u>orderId</u>, userId, addressId, status, orderDate, {productId})
- **PAYMENT** (<u>paymentId</u>, orderId, type, status, paymentDate)
  - **PAYMENT_PIX** (<u>paymentId</u>, pixKey, receipt)
  - **PAYMENT_BOLETO** (<u>paymentId</u>, barCode, dueDate, digitLine)
  - **PAYMENT_CARD** (<u>paymentId</u>, cardId)
- **CARD** (<u>cardId</u>, userId, number, cardHolder, expiration, cvv, cardHolderCpf)
- **BANK_ACCOUNT** (<u>bankAccountId</u>, storeId, bank, agency, account, type)
- **SALE** (<u>saleId</u>, storeId, orderId, saleDate, status)
- **NOTIFICATION** (<u>notificationId</u>, saleId, status, sentAt)

## Relationships

- USER **has** ADDRESS <br> A USER has one or more ADDRESS(es) (1:N)

- USER **owns** STORE <br> A USER may own zero or one STORE (0:1)

- STORE **sells** PRODUCT <br> A STORE sells zero or more PRODUCT(s) (0:N)

- USER **creates** CART <br> A USER creates zero or one CART(s) (0:1)

- USER **places** ORDER <br> A USER places zero or more ORDER(s) (0:N)

- ORDER **validated_by** PAYMENT <br> An ORDER is validated by one PAYMENT (1:1)

- USER **saves** CARD <br> A USER may save zero or more CARD(s) (0:N)

- STORE **registers** BANK_ACCOUNT <br> A STORE has one BANK_ACCOUNT (1:1)

- STORE **makes** SALE <br> A STORE makes one or more SALE(s) (1:N)

- SALE **generates** NOTIFICATION <br> A SALE may generate one or more NOTIFICATION(s) (1:N)