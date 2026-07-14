from src import db
from src.models.tag.tag import Tag
from typing import List, Optional
from sqlalchemy import select, asc, desc
import unicodedata


def generate_slug(text: str) -> str:
    """Recibe un texto y lo modifica para generar un slug."""

    text_normalize = unicodedata.normalize("NFKD", text)
    text_ascii = text_normalize.encode("ascii", "ignore").decode("utf-8")

    return text_ascii.strip().lower().replace(" ", "-")


def create_tag(name: str) -> Optional[Tag]:
    """Crea y carga un registro de tags. Devuelve None si existe un tag parecido o igual."""

    slug = generate_slug(name)

    if get_tag_by_slug(slug):
        return None

    new_tag = Tag(name=name, slug=slug)

    db.session.add(new_tag)
    db.session.commit()
    return new_tag


def get_tag_by_id(tag_id: int) -> Optional[Tag]:
    """Busca un registro de tags por su ID. Devuelve None si no existe."""

    return db.session.get(Tag, tag_id)


def get_tag_by_slug(tag_slug: str) -> Optional[Tag]:
    """Busca un registro de tags por su slug. Devuelve None si no existe."""

    stmt = select(Tag).where(Tag.slug == tag_slug)
    return db.session.scalars(stmt).first()


def list_all_tags() -> List[Tag]:
    """Devuelve todos los registros de tags como una lista."""

    stmt = select(Tag)
    return db.session.scalars(stmt).all()


def list_filtered_tags(name: str, sort_by: str) -> List[Tag]:
    """Devuelve los registros de tags filtrados como una lista"""

    stmt = select(Tag)

    if name:
        stmt = stmt.where(Tag.name.ilike(f"%{name}%"))

    if sort_by.split("_")[0] == "name":
        if sort_by == "name_asc":
            stmt = stmt.order_by(asc(Tag.name))
        else:
            stmt = stmt.order_by(desc(Tag.name))
    else:
        if sort_by == "created_at_desc":
            stmt = stmt.order_by(asc(Tag.name))
        else:
            stmt = stmt.order_by(desc(Tag.name))

    return db.session.scalars(stmt).all()


def delete_tag(tag_id: int) -> bool:
    """Elimina un registro de tags de la base de datos por su ID."""

    tag = get_tag_by_id(tag_id)
    if not tag:
        return False

    db.session.delete(tag)
    db.session.commit()
    return True
