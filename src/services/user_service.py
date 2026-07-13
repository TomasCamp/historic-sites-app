from src import db, bcrypt
from src.models.user.user import User
from src.models.user.role import Role
from src.models.user.permission import Permission
from typing import List, Optional
from sqlalchemy import select, asc, desc


def create_user(
    name: str, lastname: str, email: str, password: str, role_id: int
) -> Optional[User]:
    """Crea y carga un registro de users. Devuelve None si el email ya está en uso."""

    normalized_email = email.strip().lower()
    if get_user_by_email(normalized_email):
        return None

    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    new_user = User(
        name=name,
        lastname=lastname,
        email=normalized_email,
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

    normalized_email = email.strip().lower()
    if get_user_by_email(normalized_email):
        return None

    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    new_user = User(
        name=name,
        lastname=lastname,
        email=normalized_email,
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

    normalized_email = user_email.strip().lower()
    stmt = select(User).where(User.email == normalized_email)
    return db.session.scalars(stmt).first()


def list_filtered_users(
    email=None, active=None, role_id=None, sort_by="created_at_desc"
) -> List[User]:
    """Devuelve todos los registros de users que cumplan los filtros como una lista."""
    stmt = select(User).where(User.is_delete.is_(False))

    if email:
        print(email)
        stmt = stmt.where(User.email.ilike(f"%{email}%"))

    if active:
        is_active_bool = active == "1"
        stmt = stmt.where(User.is_active.is_(is_active_bool))

    if role_id:
        stmt = stmt.where(User.role_id == int(role_id))

    if sort_by == "created_at_asc":
        stmt = stmt.order_by(asc(User.created_at))
    else:
        stmt = stmt.order_by(desc(User.created_at))

    return db.session.scalars(stmt).all()


def update_user(user_id: int, name: str, lastname: str, role_id: int) -> Optional[User]:
    """Modifica un registro existente de users. Si no existe devuelve None."""

    user = get_user_by_id(user_id)
    if not user:
        return None

    user.name = name
    user.lastname = lastname
    user.role_id = role_id

    db.session.commit()
    return user


def delete_user(user_id: int) -> bool:
    """Elimina lógicamente un registro de users de la base de datos por su ID. Si no existe devuelve False."""

    user = get_user_by_id(user_id)
    if not user:
        return False

    user.is_delete = True
    db.session.commit()
    return True


def authenticate_user(email: str, password: str) -> User:
    """Compara las credenciales ingresadas con los registros de User y lo devuelve. Si no se encuentra devuelve None."""

    user = get_user_by_email(email)
    if not user:
        return None

    if bcrypt.check_password_hash(user.password_hash, password):
        return user
    return None


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

    stmt = select(Role).order_by(asc(Role.name))
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
