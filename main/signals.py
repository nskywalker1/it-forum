from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Post, Category


@receiver([post_save, post_delete], sender=Post)
@receiver([post_save, post_delete], sender=Category)
def clear_cache(sender, **kwargs):
    cache.delete("category_data")
