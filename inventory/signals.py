import uuid

from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage
from django.contrib.sessions.models import Session
from django.utils.text import slugify

from PIL import Image, ImageOps

from .models import Book, Stock


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

            # Save the resized image using the storage backend
            with default_storage.open(instance.image.name, 'wb') as dest:
                img.save(dest, format="webp")

            # Generate a safe file name based on the book's title
            new_uuid = str(uuid.uuid4())[:4]
            safe_filename = slugify(f"{instance.title}-{new_uuid}") + '.webp'

            instance.image.name = safe_filename
        except Exception:
            # If there is any error, do not save the image
            pass


@receiver(pre_delete, sender=Session)
def un_block_stock(sender, instance, **kwargs):
    """ If the session is about to be deleted or expired, unblock the stock
    that was blocked by putting books in the shopping bag.
    """

    # Get the bag from the session
    bag = instance.get_decoded().get('bag', {})

    # Loop through the bag and unblock the stock
    for stock_id, quantity in bag.items():
        stock = Stock.objects.get(id=stock_id)
        stock.blocked -= quantity
        stock.save()
