import factory
import factory.fuzzy

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
    user_phone_country_code = factory.LazyAttribute(lambda n: f'+{n}{n}')
    user_phone_state_code = factory.LazyAttribute(lambda n: f'{n}{n}')
    user_phone_number = factory.LazyAttribute(lambda n: f'{n}' * 5)
