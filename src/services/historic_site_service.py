from src import db
from src.models.historic_site.historic_site import HistoricSite
from src.models.historic_site.category import Category
from src.models.historic_site.conservation_status import ConservationStatus
from src.services.change_event_service import create_change_event
from src.models.tag.tag import Tag
from typing import List, Optional
from sqlalchemy import select, asc, desc


def create_historic_site(
    name: str,
    short_description: str,
    full_description: str,
    city: str,
    province: str,
    inauguration_year: int,
    cover_image_url: str,
    category_id: int,
    conservation_status_id: int,
    user_id: int,
    latitude: float,
    longitude: float,
    cover_image_public_id: Optional[str] = None,
) -> HistoricSite:
    """Crea y carga un registro de historic_sites."""

    new_historic_site = HistoricSite(
        name=name,
        short_description=short_description,
        full_description=full_description,
        city=city,
        province=province,
        inauguration_year=inauguration_year,
        cover_image_url=cover_image_url,
        cover_image_public_id=cover_image_public_id,
        category_id=category_id,
        conservation_status_id=conservation_status_id,
        latitude=latitude,
        longitude=longitude,
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


def list_filtered_historic_sites(
    name="",
    city="",
    province="",
    tags=None,
    conservation_status_id="",
    registered_at_start=None,
    registered_at_end=None,
    is_visible="",
    sort_by="registered_desc",
) -> List[HistoricSite]:
    """Devuelve todos los registros de historic_sites que cumplan los filtros como una lista."""
    stmt = select(HistoricSite)

    if name:
        stmt = stmt.where(HistoricSite.name.ilike(f"%{name}%"))

    if city:
        stmt = stmt.where(HistoricSite.city.ilike(f"%{city}%"))

    if province:
        stmt = stmt.where(HistoricSite.province == province)

    if tags:
        stmt = stmt.join(HistoricSite.tags).where(Tag.id.in_(tags)).distinct()

    if conservation_status_id:
        stmt = stmt.where(
            HistoricSite.conservation_status_id == int(conservation_status_id)
        )

    if registered_at_start:
        stmt = stmt.where(HistoricSite.registered_at >= registered_at_start)

    if registered_at_end:
        stmt = stmt.where(HistoricSite.registered_at <= registered_at_end)

    if is_visible:
        value = is_visible == "1"
        stmt = stmt.where(HistoricSite.is_visible.is_(value))

    order = sort_by.split("_")
    if order[0] == "registered":
        if order[1] == "asc":
            stmt = stmt.order_by(asc(HistoricSite.registered_at))
        else:
            stmt = stmt.order_by(desc(HistoricSite.registered_at))
    elif order[0] == "name":
        if order[1] == "asc":
            stmt = stmt.order_by(asc(HistoricSite.name))
        else:
            stmt = stmt.order_by(desc(HistoricSite.name))
    else:
        if order[1] == "asc":
            stmt = stmt.order_by(asc(HistoricSite.city))
        else:
            stmt = stmt.order_by(desc(HistoricSite.city))

    return db.session.scalars(stmt).all()


def update_historic_site(
    historic_site_id: int,
    name: str,
    short_description: str,
    full_description: str,
    city: str,
    province: str,
    inauguration_year: int,
    cover_image_url: str,
    category_id: int,
    conservation_status_id: int,
    user_id: int,
    latitude: float,
    longitude: float,
    cover_image_public_id: Optional[str] = None,
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
    historic_site.cover_image_url = cover_image_url
    historic_site.cover_image_public_id = cover_image_public_id
    historic_site.category_id = category_id
    historic_site.conservation_status_id = conservation_status_id
    historic_site.latitude = latitude
    historic_site.longitude = longitude

    change_event = create_change_event(
        action="UPDATE", user_id=user_id, historic_site_id=historic_site_id
    )
    db.session.add(change_event)

    db.session.commit()
    return historic_site


def delete_historic_site(historic_site_id: int) -> bool:
    """Elimina un registro lógicamente de historic_sites de la base de datos por su ID. Si no existe devuelve False."""

    historic_site = get_historic_site_by_id(historic_site_id)
    if not historic_site:
        return False

    historic_site.is_delete = True
    db.session.commit()
    return True


def assign_tags_to_historic_site(
    new_tags: list[Tag], historic_site: HistoricSite, user_id: int
) -> bool:
    """Asigna los tags ingresados a un historic_site. Devuelve False si los tags no cambiaron."""
    current_tags_set = set(historic_site.tags)
    new_tags_set = set(new_tags)

    if current_tags_set == new_tags_set:
        return False

    historic_site.tags = list(new_tags_set)

    change_event = create_change_event(
        action="UPDATE_TAGS", user_id=user_id, historic_site_id=historic_site.id
    )
    db.session.add(change_event)
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
