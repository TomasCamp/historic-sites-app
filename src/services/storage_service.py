import cloudinary.uploader


def upload_image(file_storage, folder="historic-sites-app") -> dict:
    """Sube un archivo recibido a Cloudinary y retorna la URL segura y el public_id."""

    upload_result = cloudinary.uploader.upload(
        file_storage, folder=folder, format="webp"
    )

    return {
        "url": upload_result.get("secure_url"),
        "public_id": upload_result.get("public_id"),
    }
