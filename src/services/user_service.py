from src import db, bcrypt
from src.models.user.user import User
from src.models.user.role import Role
from src.models.user.permission import Permission
from typing import List, Optional
from sqlalchemy import select


def create_user(
    name: str, lastname: str, email: str, password: str, role_id: int
) -> Optional[User]:
    """Crea y carga un registro de users. Devuelve None si el email ya está en uso."""

    if get_user_by_email(email):
        return None

    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    new_user = User(
        name=name,
        lastname=lastname,
        email=email,
        password_hash=password_hash,
        role_id=role_id,
    )

    db.session.add(new_user)
    db.session.commit()
    return new_user


def create_super_user(
    name: str, lastname: str, email: str, password: str, role_id: int
) -> Optional[User]:
    """Crea y carga un registro de users. Devuelve None si el email ya está en uso."""

    if get_user_by_email(email):
        return None

    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    new_user = User(
        name=name,
        lastname=lastname,
        email=email,
        password_hash=password_hash,
        role_id=role_id,
        is_superuser=True,
    )

    db.session.add(new_user)
    db.session.commit()
    return new_user


def get_user_by_id(user_id: int) -> Optional[User]:
    """Busca un registro de users por su ID. Devuelve None si no existe."""

    return db.session.get(User, user_id)


def get_user_by_email(user_email: str) -> Optional[User]:
    """Busca un registro de users por su email. Devuelve None si no existe."""

    stmt = select(User).where(User.email == user_email)
    return db.session.scalars(stmt).first()


def list_all_users() -> List[User]:
    """Devuelve todos los registros de users como una lista."""

    stmt = select(User)
    return db.session.scalars(stmt).all()


def update_user(user_id: int, name: str, lastname: str) -> Optional[User]:
    """Modifica un registro existente de users. Si no existe devuelve None."""

    user = get_user_by_id(user_id)
    if not user:
        return None

    user.name = name
    user.lastname = lastname

    db.session.commit()
    return user


def delete_user(user_id: int) -> bool:
    """Elimina un registro de users de la base de datos por su ID. Si no existe devuelve False."""

    user = get_user_by_id(user_id)
    if not user:
        return False

    db.session.delete(user)
    db.session.commit()
    return True


def create_role(name: str) -> Role:
    """Crea y carga un registro de roles."""

    new_role = Role(name=name)

    db.session.add(new_role)
    db.session.commit()
    return new_role


def get_role_by_id(role_id: int) -> Optional[Role]:
    """Busca un registro de roles por su ID. Devuelve None si no existe."""

    return db.session.get(Role, role_id)


def list_all_roles() -> List[Role]:
    """Devuelve todos los registros de roles como una lista."""

    stmt = select(Role)
    return db.session.scalars(stmt).all()


def create_permission(name: str) -> Permission:
    """Crea y carga un registro de permissions."""

    new_permission = Permission(name=name)

    db.session.add(new_permission)
    db.session.commit()
    return new_permission


def get_permission_by_id(permission_id: int) -> Optional[Permission]:
    """Busca un registro de permissions por su ID. Devuelve None si no existe."""

    return db.session.get(Permission, permission_id)


def list_all_permissions() -> List[Permission]:
    """Devuelve todos los registros de permissions como una lista."""

    stmt = select(Permission)
    return db.session.scalars(stmt).all()


def assign_permission_to_role(permission: Permission, role: Role) -> None:
    """Asigna un permission a un role."""

    role.permissions.append(permission)
    db.session.commit()
