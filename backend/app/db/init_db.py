# Create superuser
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.user import User
from app.core.security import get_password_hash

def init_db(db: Session) -> None:
    # 创建超级用户
    user = db.query(User).filter(User.email == settings.FIRST_SUPERUSER).first()
    if not user:
        user = User(
            email=settings.FIRST_SUPERUSER,
            hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
            full_name="Initial Admin",
            is_superuser=True,
            is_active=True,
        )
        db.add(user)
        db.commit() 