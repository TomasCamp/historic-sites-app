from src import db
from src.models.historic_site.historic_site import HistoricSite
from src.models.historic_site.category import Category
from src.models.historic_site.conservation_status import ConservationStatus
from src.services.change_event_service import create_change_event
from src.models.tag.tag import Tag
from typing import List, Optional
from sqlalchemy import select


def create_historic_site(
    name: str,
    short_description: str,
    full_description: str,
    city: str,
    province: str,
    inauguration_year: int,
    category_id: int,
    conservation_status_id: int,
    user_id: int,
) -> HistoricSite:
    """Crea y carga un registro de historic_sites."""

    new_historic_site = HistoricSite(
        name=name,
        short_description=short_description,
        full_description=full_description,
        city=city,
        province=province,
        inauguration_year=inauguration_year,
        category_id=category_id,
        conservation_status_id=conservation_status_id,
    )
    db.session.add(new_historic_site)
    db.session.flush()

    change_event = create_change_event(
        action="CREATE", user_id=user_id, historic_site_id=new_historic_site.id
    )
    db.session.add(change_event)

    db.session.commit()
    return new_historic_site


def get_historic_site_by_id(historic_site_id: int) -> Optional[HistoricSite]:
    """Busca un registro de historic_sites por su ID. Devuelve None si no existe."""

    return db.session.get(HistoricSite, historic_site_id)


def list_all_historic_sites() -> List[HistoricSite]:
    """Devuelve todos los registros de historic_sites como una lista."""

    stmt = select(HistoricSite)
    return db.session.scalars(stmt).all()


def update_historic_site(
    historic_site_id: int,
    name: str,
    short_description: str,
    full_description: str,
    city: str,
    province: str,
    inauguration_year: int,
    category_id: int,
    conservation_status_id: int,
) -> Optional[HistoricSite]:
    """Modifica un registro existente de historic_sites. Si no existe devuelve None."""

    historic_site = get_historic_site_by_id(historic_site_id)
    if not historic_site:
        return None

    historic_site.name = name
    historic_site.short_description = short_description
    historic_site.full_description = full_description
    historic_site.city = city
    historic_site.province = province
    historic_site.inauguration_year = inauguration_year
    historic_site.category_id = category_id
    historic_site.conservation_status_id = conservation_status_id

    db.session.commit()
    return historic_site


def delete_historic_site(historic_site_id: int) -> bool:
    """Elimina un registro de historic_sites de la base de datos por su ID. Si no existe devuelve False."""

    historic_site = get_historic_site_by_id(historic_site_id)
    if not historic_site:
        return False

    db.session.delete(historic_site)
    db.session.commit()
    return True


def assign_tag_to_historic_site(tag: Tag, historic_site: HistoricSite) -> bool:
    """Asigna un tag a un historic_site."""

    if tag in historic_site.tags:
        return False

    historic_site.tags.append(tag)
    db.session.commit()
    return True


def create_category(name: str) -> Category:
    """Crea y carga un registro de categorys."""

    new_category = Category(name=name)

    db.session.add(new_category)
    db.session.commit()
    return new_category


def get_category_by_id(category_id: int) -> Optional[Category]:
    """Busca un registro de categorys por su ID. Devuelve None si no existe."""

    return db.session.get(Category, category_id)


def list_all_categorys() -> List[Category]:
    """Devuelve todos los registros de categorys como una lista."""

    stmt = select(Category)
    return db.session.scalars(stmt).all()


def create_conservation_status(name: str) -> ConservationStatus:
    """Crea y carga un registro de conservation_statuses."""

    new_conservation_status = ConservationStatus(name=name)

    db.session.add(new_conservation_status)
    db.session.commit()
    return new_conservation_status


def get_conservation_status_by_id(
    conservation_status_id: int,
) -> Optional[ConservationStatus]:
    """Busca un registro de conservation_statuses por su ID. Devuelve None si no existe."""

    return db.session.get(ConservationStatus, conservation_status_id)


def list_all_conservation_statuses() -> List[ConservationStatus]:
    """Devuelve todos los registros de conservation_statuses como una lista."""

    stmt = select(ConservationStatus)
    return db.session.scalars(stmt).all()
