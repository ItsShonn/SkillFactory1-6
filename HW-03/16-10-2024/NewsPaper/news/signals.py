from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import send_mail
from .models import Post, Category, UserToCategory, User, PostCategory
import os
from django.urls import reverse
from django.shortcuts import resolve_url


# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
@receiver(m2m_changed, sender=PostCategory)
def created_post(sender, instance, **kwargs):
    post = Post.objects.get(id=instance.id)
    subject = f'Вышла {'статья' if post.type == 'A' else 'новость'} {post.title} в {post.date.strftime("%d %m %Y")}'

    post_to_category = PostCategory.objects.filter(post_id__id=post.id).first()
    category = post_to_category.category if post_to_category else None
    users = []
    if category:
        for connection in UserToCategory.objects.filter(category=category):
            users.append(User.objects.get(id=connection.user.id))

    send_mail(
        f'{subject}',
        f'{post.content[:50]}' + f'...' + f'127.0.0.1:8000{resolve_url("news_detail", pk=post.id)}',
        f'{str(os.getenv('EMAIL'))}@yandex.ru',
        [user.email for user in users]
    )