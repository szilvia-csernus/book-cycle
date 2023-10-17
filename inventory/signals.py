import uuid

from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage
from django.contrib.sessions.models import Session
from django.utils.text import slugify
from pathlib import Path

from PIL import Image, ImageOps

from .models import Book, Stock


# @receiver(pre_delete, sender=Book)
# def delete_image(sender, instance, **kwargs):
#     """
#     Delete the image from the storage when the book is deleted.
#     """
#     if instance.image:
#         storage, url = instance.image.storage, instance.image.url
#         if storage.exists(url):
#             storage.delete(url)


@receiver(pre_save, sender=Book)
def resize_and_convert_image(sender, instance, **kwargs):
    """
    Resize and convert the uploaded image to webp format.
    """
    if instance.image:
        try:
            # Open the uploaded image using Pillow
            img = Image.open(instance.image)

            # Apply EXIF orientation (auto-rotate)
            img = ImageOps.exif_transpose(img)

            # Resize while preserving aspect ratio
            if instance.image.height > 368 or instance.image.width > 320:
                img.thumbnail((320, 368))

            # Save the resized image back to the same path
            source = Path(instance.image.path)
            destination = source.with_suffix(".webp")
            img.save(destination, format="webp")

            instance.image = destination.name

            # Generate a safe file name based on the book's title
            # new_uuid = str(uuid.uuid4())[:4]
            # safe_filename = slugify(f"{instance.title}-{new_uuid}") + '.webp'

            # instance.image.name = safe_filename
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
