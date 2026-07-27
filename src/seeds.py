from src.services import user_service
from src.services import historic_site_service
from src.services import tag_service


def init_seeds():
    """Carga datos de prueba para la aplicación"""

    # Roles
    admin_role = user_service.create_role("Administrador")
    editor_role = user_service.create_role("Editor")

    # Permissions
    user_index = user_service.create_permission("user_index")
    user_show = user_service.create_permission("user_show")
    user_create = user_service.create_permission("user_create")
    user_update = user_service.create_permission("user_update")
    user_delete = user_service.create_permission("user_delete")

    historic_site_index = user_service.create_permission("historic_site_index")
    historic_site_show = user_service.create_permission("historic_site_show")
    historic_site_create = user_service.create_permission("historic_site_create")
    historic_site_update = user_service.create_permission("historic_site_update")
    historic_site_delete = user_service.create_permission("historic_site_delete")
    historic_site_exprot_csv = user_service.create_permission(
        "exprot_csv_historic_site"
    )
    historic_site_history = user_service.create_permission("historic_site_history")

    tag_index = user_service.create_permission("tag_index")
    tag_show = user_service.create_permission("tag_show")
    tag_create = user_service.create_permission("tag_create")
    tag_update = user_service.create_permission("tag_update")
    tag_delete = user_service.create_permission("tag_delete")

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
        user_service.assign_permission_to_role(permission, admin_role)

    for permission in editor_permission:
        user_service.assign_permission_to_role(permission, editor_role)

    # Users
    super_user = user_service.create_super_user(
        "John", "Doe", "superuser@example.com", "password", admin_role.id
    )
    admin_user = user_service.create_user(
        "John", "Smith", "admin@example.com", "password", admin_role.id
    )
    editor_user = user_service.create_user(
        "Richard", "Roe", "editor@example.com", "password", editor_role.id
    )

    # Conservation_statuses
    good_status = historic_site_service.create_conservation_status("Bueno")
    average_status = historic_site_service.create_conservation_status("Regular")
    bad_status = historic_site_service.create_conservation_status("Malo")

    # Categories
    category1 = historic_site_service.create_category("Sitio Arqueológico")
    category2 = historic_site_service.create_category("Arquitectura")
    category3 = historic_site_service.create_category("Infraestructura")
    category4 = historic_site_service.create_category("Monumento Histórico")
    category5 = historic_site_service.create_category("Espacio Público")
    category6 = historic_site_service.create_category("Institución")
    category7 = historic_site_service.create_category("Patrimonio Industrial")
    category8 = historic_site_service.create_category("Sitio Natural")

    # Historic_sites
    historic_site1 = historic_site_service.create_historic_site(
        name="Ruinas de San Ignacio Miní",
        short_description="Restos arqueológicos de la misión jesuítica guaraní mejor conservada en Argentina.",
        full_description="Fundada originalmente en el siglo XVII, es uno de los máximos exponentes del barroco americano. Sus imponentes muros de arenisca roja reflejan la organización social y arquitectónica del encuentro entre la cultura jesuita y los pueblos originarios.",
        city="San Ignacio",
        province="Misiones",
        inauguration_year=1696,
        category_id=category1.id,  # Sitio Arqueológico
        conservation_status_id=good_status.id,  # Bueno
        user_id=super_user.id,
        latitude=-27.2558,
        longitude=-55.5328,
        cover_image_url="https://res.cloudinary.com/q75kyjkr/image/upload/v1784580065/historic-sites-app/yjrpk3x0mfqx8cryrtzf.webp",
    )

    historic_site2 = historic_site_service.create_historic_site(
        name="Cabildo de Buenos Aires",
        short_description="Edificio colonial icónico del eje histórico, epicentro de la Revolución de Mayo.",
        full_description="Originalmente sede de la administración colonial, el edificio sufrió numerosas modificaciones y demoliciones parciales a lo largo del tiempo. Hoy funciona como museo y es el símbolo patrio fundamental de los acontecimientos de mayo de 1810.",
        city="Ciudad Autónoma de Buenos Aires",
        province="Buenos Aires",
        inauguration_year=1740,
        category_id=category2.id,  # Arquitectura
        conservation_status_id=average_status.id,  # Regular
        user_id=admin_user.id,
        latitude=-34.6087,
        longitude=-58.3736,
        cover_image_url="https://res.cloudinary.com/q75kyjkr/image/upload/v1784582407/historic-sites-app/od8suzxh3gtg8sqpjrbe.webp",
    )

    historic_site3 = historic_site_service.create_historic_site(
        name="Puente Transbordador Nicolás Avellaneda",
        short_description="Estructura de ingeniería industrial colosal, uno de los últimos ocho transbordadores que quedan en el mundo.",
        full_description="Inaugurado a principios del siglo XX para unir la Capital Federal con la Isla Maciel, es una joya de la ingeniería de hierro. Estuvo en desuso y abandono por décadas y, aunque fue recuperado y puesto en funcionamiento, requiere mantenimiento constante en su estructura portante.",
        city="Buenos Aires",
        province="Buenos Aires",
        inauguration_year=1914,
        category_id=category3.id,  # Infraestructura
        conservation_status_id=average_status.id,  # Regular
        user_id=editor_user.id,
        latitude=-34.6386,
        longitude=-58.3557,
        cover_image_url="https://res.cloudinary.com/q75kyjkr/image/upload/v1784582598/historic-sites-app/itf63dqihhmaxnyzsz4q.webp",
    )

    historic_site4 = historic_site_service.create_historic_site(
        name="Pucará de Tilcara",
        short_description="Fortaleza prehispánica omaguaca ubicada estratégicamente en la Quebrada de Humahuaca.",
        full_description="Un sitio arqueológico clave construido por los nativos de la zona. Se compone de viviendas, corrales, un centro ceremonial y un sector de entierros. Aunque fue parcialmente reconstruido con fines turísticos en el siglo XX, sufre cierto desgaste por el alto tránsito y factores climáticos.",
        city="Tilcara",
        province="Jujuy",
        inauguration_year=1200,
        category_id=category1.id,  # Sitio Arqueológico
        conservation_status_id=bad_status.id,  # Malo
        user_id=super_user.id,
        latitude=-23.5886,
        longitude=-65.3922,
        cover_image_url="https://res.cloudinary.com/q75kyjkr/image/upload/v1784582699/historic-sites-app/im7qkvqnarr79knz9wbw.webp",
    )

    # Tags
    tag1 = tag_service.create_tag("Época Colonial")
    tag2 = tag_service.create_tag("Patrimonio de la Humanidad")
    tag3 = tag_service.create_tag("Prehispánico")
    tag4 = tag_service.create_tag("Ingeniería de Hierro")

    historic_site_service.assign_tag_to_historic_site(
        [tag1, tag2], historic_site1, editor_user.id
    )
    historic_site_service.assign_tag_to_historic_site(
        [tag1], historic_site2, editor_user.id
    )
    historic_site_service.assign_tag_to_historic_site(
        [tag3], historic_site4, editor_user.id
    )
