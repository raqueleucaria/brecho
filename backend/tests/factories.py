import factory
import factory.fuzzy

from src.model.address import Address
from src.model.category import Category
from src.model.color import Color
from src.model.seller import Seller
from src.model.user import User


class UserFactory(factory.Factory):
    class Meta:
        model = User
        exclude = ('addresses', 'clients', 'sellers')

    user_name = factory.Sequence(lambda n: f'test{n}')
    user_nickname = factory.LazyAttribute(lambda obj: f'{obj.user_name}_nick')
    user_email = factory.LazyAttribute(
        lambda obj: f'{obj.user_name}@email.com'
    )
    user_password = factory.LazyAttribute(
        lambda obj: f'{obj.user_name}_password'
    )
    user_phone_country_code = factory.LazyAttribute(lambda n: f'+{n}{n}')
    user_phone_state_code = factory.LazyAttribute(lambda n: f'{n}{n}')
    user_phone_number = factory.LazyAttribute(lambda n: f'{n}' * 5)
    addresses = None
    clients = None
    sellers = None


class AddressFactory(factory.Factory):
    class Meta:
        model = Address
        exclude = ('user',)

    address_country = factory.Sequence(lambda n: f'Country{n}')
    address_zip_code = factory.Sequence(lambda n: f'{n:05}-000')
    address_state = factory.Sequence(lambda n: f'State{n}')
    address_city = factory.Sequence(lambda n: f'City{n}')
    address_neighborhood = factory.Sequence(lambda n: f'Neighborhood{n}')
    address_street = factory.Sequence(lambda n: f'Street{n}')
    address_number = factory.Sequence(lambda n: f'{n:05d}')
    address_complement = factory.Sequence(lambda n: f'Complement{n}')

    user_id = factory.LazyAttribute(
        lambda obj: obj.user_id if hasattr(obj, 'user_id') else 1
    )


class SellerFactory(factory.Factory):
    class Meta:
        model = Seller

    seller_description = factory.Sequence(lambda n: f'Description {n}')
    seller_bank_account = factory.Sequence(lambda n: f'{n:07d}')
    seller_bank_agency = factory.Sequence(lambda n: f'{n:05d}')
    seller_bank_name = factory.Sequence(lambda n: f'Bank {n}')
    seller_bank_type = factory.Iterator(['checking', 'savings'])
    seller_status = factory.Iterator(['active', 'inactive'])
    user_id = factory.LazyAttribute(
        lambda obj: obj.user_id if hasattr(obj, 'user_id') else 1
    )


class CategoryFactory(factory.Factory):
    class Meta:
        model = Category

    category_name = factory.Sequence(lambda n: f'Category {n + 1}')


class ColorFactory(factory.Factory):
    class Meta:
        model = Color

    color_name = factory.Sequence(lambda n: f'Color {n + 1}')
