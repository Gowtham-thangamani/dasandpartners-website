from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import News, Blogs

@receiver(post_delete, sender=News)
def delete_news_image(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)


@receiver(post_delete, sender=Blogs)
def delete_blogs_image(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)