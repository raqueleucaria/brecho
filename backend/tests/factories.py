import factory
import factory.fuzzy

from src.model.address import Address
from src.model.cart_want import CartWant
from src.model.category import Category
from src.model.client import Client
from src.model.color import Color
from src.model.product import Product
from src.model.seller import Seller
from src.model.user import User


class UserFactory(factory.Factory):
    class Meta:
        model = User

    user_name = factory.Sequence(lambda n: f'test{n}')
    user_nickname = factory.LazyAttribute(lambda obj: f'{obj.user_name}_nick')
    user_email = factory.LazyAttribute(
        lambda obj: f'{obj.user_name}@email.com'
    )
    user_password = factory.LazyAttribute(
        lambda obj: f'{obj.user_name}_password'
    )
    user_phone_country_code = factory.Sequence(lambda n: f'+{n:02d}')
    user_phone_state_code = factory.Sequence(lambda n: f'{n:02d}')
    user_phone_number = factory.Sequence(lambda n: f'{n:09d}')


class AddressFactory(factory.Factory):
    class Meta:
        model = Address
        exclude = (
            'user',
        )  # Impede que o objeto 'user' seja passado ao modelo

    # Aceita um objeto 'user' como parâmetro
    user = factory.SubFactory(UserFactory)

    # Usa o objeto 'user' para extrair o ID
    user_id = factory.LazyAttribute(lambda o: o.user.user_id)

    address_country = factory.Sequence(lambda n: f'Country{n}')
    address_zip_code = factory.Sequence(lambda n: f'{n:05}-000')
    address_state = factory.Sequence(lambda n: f'State{n}')
    address_city = factory.Sequence(lambda n: f'City{n}')
    address_neighborhood = factory.Sequence(lambda n: f'Neighborhood{n}')
    address_street = factory.Sequence(lambda n: f'Street{n}')
    address_number = factory.Sequence(lambda n: f'{n:03d}')
    address_complement = factory.Sequence(lambda n: f'Complement{n}')


class SellerFactory(factory.Factory):
    class Meta:
        model = Seller
        exclude = (
            'user',
        )  # Impede que o objeto 'user' seja passado ao modelo

    # Aceita um objeto 'user' como parâmetro
    user = factory.SubFactory(UserFactory)

    # Usa o objeto 'user' para extrair o ID
    user_id = factory.LazyAttribute(lambda o: o.user.user_id)

    seller_description = factory.Sequence(lambda n: f'Description {n}')
    seller_bank_account = factory.Sequence(lambda n: f'{n:07d}')
    seller_bank_agency = factory.Sequence(lambda n: f'{n:05d}')
    seller_bank_name = factory.Sequence(lambda n: f'Bank {n}')
    seller_bank_type = factory.Iterator(['checking', 'savings'])
    seller_status = factory.Iterator(['active', 'inactive'])


class ClientFactory(factory.Factory):
    class Meta:
        model = Client
        exclude = (
            'user',
        )  # Impede que o objeto 'user' seja passado ao modelo

    # Aceita um objeto 'user' como parâmetro
    user = factory.SubFactory(UserFactory)

    # Usa o objeto 'user' para extrair o ID
    user_id = factory.LazyAttribute(lambda o: o.user.user_id)


class CategoryFactory(factory.Factory):
    class Meta:
        model = Category

    category_name = factory.Sequence(lambda n: f'Category {n + 1}')


class ColorFactory(factory.Factory):
    class Meta:
        model = Color

    color_name = factory.Sequence(lambda n: f'Color {n + 1}')


class ProductFactory(factory.Factory):
    class Meta:
        model = Product

    product_name = factory.Sequence(lambda n: f'Product {n + 1}')
    product_description = factory.Sequence(lambda n: f'Description {n + 1}')
    product_price = factory.fuzzy.FuzzyDecimal(10.0, 1000.0)
    product_condition = factory.Iterator(['new', 'used'])
    product_gender = factory.Iterator(['female', 'male', 'unisex'])
    product_size = factory.Iterator(['S', 'M', 'L', 'XL'])
    product_status = factory.Iterator(['available', 'unavailable'])


class CartWantFactory(factory.Factory):
    class Meta:
        model = CartWant

    # Estes valores devem ser passados explicitamente nos testes
    # Ex: CartWantFactory(product_id=1, client_id=1)
