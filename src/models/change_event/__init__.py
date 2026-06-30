from src import db
from src.models.change_event.change_event import ChangeEvent
from src.models.user.user import User
from src.models.historic_site.historic_site import HistoricSite
from typing import List, Optional
from sqlalchemy import select


def create_change_event(
    action: str, user_id: int, historic_site_id: int
) -> ChangeEvent:
    """Crea y carga un registro de change_events."""
    new_change_event = ChangeEvent(
        action=action, user_id=user_id, historic_site_id=historic_site_id
    )

    db.session.add(new_change_event)
    db.session.commit()
    return new_change_event


def get_change_event_by_id(change_event_id: int) -> Optional[ChangeEvent]:
    """Busca un registro de change_events por su ID. Devuelve None si no existe."""
    return db.session.get(ChangeEvent, change_event_id)


def list_all_change_events() -> List[ChangeEvent]:
    """Devuelve todos los registros de change_events como una lista de python."""
    stmt = select(ChangeEvent)
    return db.session.scalars(stmt).all()


def update_change_event(
    change_event_id: int, action: str, user_id: int, historic_site_id: int
) -> Optional[ChangeEvent]:
    """Modifica un registro existente de change_event. Si no existe devuelve None."""
    change_event = get_change_event_by_id(change_event_id)
    if not change_event:
        return None

    change_event.action = action
    change_event.user_id = user_id
    change_event.historic_site_id = historic_site_id

    db.session.commit()
    return change_event


def delete_change_event(change_event_id: int) -> bool:
    """Elimina un registro de la base de datos por su ID."""
    change_event = get_change_event_by_id(change_event_id)
    if not change_event:
        return False

    db.session.delete(change_event)
    db.session.commit()
    return True
