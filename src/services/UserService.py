from src.db.models.User import User
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from src.models.User import UserCreateModel
from src.utils.Utils import generate_password_hash

class UserService:
    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)

        result = await session.exec(statement)

        user = result.first()

        return user if user is not None else None

    async def is_email_exist(self, email: str, session: AsyncSession):
        user = await self.get_user_by_email(email, session)

        return user is not None

    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        user_data_dict = user_data.model_dump()
        
        new_user = User(**user_data_dict)
        
        new_user.password_hash = generate_password_hash(user_data_dict['password'])
        new_user.role = "user"
        
        session.add(new_user)

        await session.commit()

        return new_user