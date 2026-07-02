from src.models import user
from src.models import historic_site


def init_seeds():
    """Carga datos de prueba para la aplicación"""

    # Roles
    admin_role = user.create_role("Administrador")
    editor_role = user.create_role("Editor")

    # Permissions
    user_index = user.create_permission("user_index")
    user_show = user.create_permission("user_show")
    user_create = user.create_permission("user_create")
    user_update = user.create_permission("user_update")
    user_delete = user.create_permission("user_delete")

    historic_site_index = user.create_permission("historic_site_index")
    historic_site_show = user.create_permission("historic_site_show")
    historic_site_create = user.create_permission("historic_site_create")
    historic_site_update = user.create_permission("historic_site_update")
    historic_site_delete = user.create_permission("historic_site_delete")
    historic_site_exprot_csv = user.create_permission("exprot_csv_historic_site")
    historic_site_history = user.create_permission("historic_site_history")

    tag_index = user.create_permission("tag_index")
    tag_show = user.create_permission("tag_show")
    tag_create = user.create_permission("tag_create")
    tag_update = user.create_permission("tag_update")
    tag_delete = user.create_permission("tag_delete")

    admin_permission = [
        user_index,
        user_show,
        user_create,
        user_update,
        user_delete,
        historic_site_index,
        historic_site_show,
        historic_site_create,
        historic_site_update,
        historic_site_delete,
        historic_site_exprot_csv,
        historic_site_history,
        tag_index,
        tag_show,
        tag_create,
        tag_update,
        tag_delete,
    ]
    editor_permission = [
        historic_site_index,
        historic_site_show,
        historic_site_create,
        historic_site_update,
        historic_site_history,
        tag_index,
        tag_show,
        tag_create,
        tag_update,
        tag_delete,
    ]

    for permission in admin_permission:
        user.assign_permission_to_role(permission, admin_role)

    for permission in editor_permission:
        user.assign_permission_to_role(permission, editor_role)

    # Users
    super_user = user.create_super_user(
        "Jhon", "Doe", "superuser@example.com", "password", admin_role.id
    )
    super_user = user.create_user(
        "Jhon", "Doe", "admin@example.com", "password", admin_role.id
    )
    super_user = user.create_user(
        "Jhon", "Doe", "editor@example.com", "password", editor_role.id
    )

    # Conservation_statuses
    good_status = historic_site.create_conservation_status("Bueno")
    average_status = historic_site.create_conservation_status("Regular")
    bad_status = historic_site.create_conservation_status("Malo")

    # Categories
    category1 = historic_site.create_category("Sitio Arqueológico")
    category2 = historic_site.create_category("Arquitectura")
    category3 = historic_site.create_category("Infraestructura")
    category4 = historic_site.create_category("Monumento Histórico")
    category5 = historic_site.create_category("Espacio Público")
    category6 = historic_site.create_category("Institución")
    category7 = historic_site.create_category("Patrimonio Industrial")
    category8 = historic_site.create_category("Sitio Natural")
