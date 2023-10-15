from django.db.models.signals import pre_save
from django.dispatch import receiver
from PIL import Image, ImageOps
from pathlib import Path

from .models import Book


@receiver(pre_save, sender=Book)
def resize_and_convert_image(sender, instance, **kwargs):
    """
    Resize and convert the uploaded image to webp format.
    """
    if instance.image:
        try:
            # Open the uploaded image using Pillow
            img = Image.open(instance.image)

            # Check if the image has EXIF data
            if hasattr(img, '_getexif'):
                exif = img._getexif()
                if exif:
                    # Apply EXIF orientation (auto-rotate) if available
                    orientation = exif.get(0x0112)
                    if orientation:
                        img = ImageOps.exif_transpose(img)

            # Resize while preserving aspect ratio
            if img.height > 368 or img.width > 320:
                img.thumbnail((320, 368))

            # Save the resized image back to the same path
            source = Path(instance.image.path)
            destination = source.with_suffix(".webp")
            img.save(destination, format="webp")

            instance.image = destination.name
        except Exception:
            print('An error occurred while resizing image')
