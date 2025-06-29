# from sqlalchemy.orm import Session
# from model.user import User

# class UserRepository:
#     @staticmethod
#     def create(db: Session, user: User) -> User:
#         db.add(user)
#         db.commit()
#         db.refresh(user)
#         return user

#     @staticmethod
#     def get_by_id(db: Session, user_id: int) -> User | None:
#         return db.query(User).filter(User.user_id == user_id).first()

#     @staticmethod
#     def get_all(db: Session) -> list[User]:
#         return db.query(User).all()

#     @staticmethod
#     def delete(db: Session, user: User):
#         db.delete(user)
#         db.commit()