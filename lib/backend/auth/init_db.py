from models.database import SessionLocal
from models.models import User
from auth.auth import get_password_hash
from config import settings

def init_db():
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == "admin").first()
        if not user:
            admin_user = User(
                username="admin",
                email="admin@example.com",
                hashed_password=get_password_hash(settings.admin_password),
                is_superuser=True
            )
            db.add(admin_user)
            db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()