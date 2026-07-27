import cloudinary.uploader


def upload_image(file_storage, folder="historic-sites-app") -> dict:
    """Sube un archivo recibido a Cloudinary y retorna la URL segura y el public_id."""

    upload_result = cloudinary.uploader.upload(
        file_storage, folder=folder, format="webp"
    )

    return {
        "cover_image_url": upload_result.get("secure_url"),
        "cover_image_public_id": upload_result.get("public_id"),
    }


def delete_image(public_id: str) -> bool:
    """Elimina una imagen de Cloudinary usando su public_id. Retorna True si se eliminó con éxito, False en caso contrario."""

    try:
        response = cloudinary.uploader.destroy(public_id)
        return response.get("result") in ["ok", "not found"]
    except Exception:
        return False
