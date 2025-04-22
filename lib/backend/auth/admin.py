from models.models import User, MLModel
from models.database import SessionLocal, engine
from auth.auth import get_password_hash, get_current_user, verify_password
from config import settings

from typing import Optional
from starlette_admin import BaseAdmin, DropDown
from starlette_admin.contrib.sqla import Admin, ModelView
from starlette_admin.auth import AuthProvider, AdminUser
from starlette_admin.exceptions import FormValidationError, LoginFailed
from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session

class DBAuthProvider(AuthProvider):
    """
    Аутентификация через базу данных
    """
    async def login(self, 
        username: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
        ) -> bool:
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.username == username).first()
            if user and verify_password(password, user.hashed_password):
                # Сохраняем только минимально необходимую информацию в сессии
                request.session.update({"username": user.username})
                return response
            raise LoginFailed("Invalid username or password")
        finally:
            db.close()

    async def is_authenticated(self, request: Request) -> bool:
        user = request.session.get("username", None)
        auth = user is not None
        if auth:
            request.state.user = request.session["username"]
        return auth
    
    def get_admin_user(self, request: Request) -> Optional[AdminUser]:
        user = request.state.user  # Retrieve current user
        photo_url = None
        return AdminUser(username=user, photo_url=photo_url)

    async def logout(self, request: Request, response: Response) -> bool:
        request.session.clear()
        return response

# Создаем административную панель
admin_app = Admin(
    engine,
    auth_provider=DBAuthProvider(login_path="/sign-in", logout_path="/sign-out"),
    base_url="/admin",
    middlewares=[Middleware(SessionMiddleware, secret_key=settings.secret_key)],
)

class UserModelView(ModelView):
    model = User
    icon = "users"
    name_plural = "Users"
    fields = [
        "id",
        "username",
        "email",
        "is_active",
        "is_superuser",
    ]

class MLModelModelView(ModelView):
    model = MLModel
    icon = "box"
    name_plural = "ML Models"
    fields = [
        "id",
        "name",
        "version",
        "path",
        "is_active",
    ]

admin_app.add_view(UserModelView(User))
admin_app.add_view(MLModelModelView(MLModel))