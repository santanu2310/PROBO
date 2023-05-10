from django.conf import settings
from django.utils.text import slugify
from django.core.mail import get_connection, EmailMessage
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.template.loader import get_template
from . models import Subscriber,Blog, Category


@receiver(pre_save, sender=Category)
def create_slug(sender, instance, *args, **kwargs):
    if not instance.url:
        instance.url = slugify(instance.name)

@receiver(pre_save, sender=Blog)
def create_slug(sender, instance, *args, **kwargs):
    if not instance.url:
        instance.url = slugify(instance.name)



@receiver(post_save, sender=Blog)
def sendEmail(sender,instance, created, *args, **kwargs):
    if created:
        email_list = Subscriber.objects.values_list("email",flat=True)
        with get_connection(host=settings.EMAIL_HOST, port=settings.EMAIL_PORT,  username=settings.EMAIL_HOST_USER, password=settings.EMAIL_HOST_PASSWORD, use_tls=settings.EMAIL_USE_TLS ) as connection:
            subject = instance.name  
            email_from = settings.EMAIL_HOST_USER  
            recipient_list = email_list
            context={'article': instance.context_to_dict()}
            message = get_template("blog_app/emails/newsletter.html").render(
                context
            )
            msg = EmailMessage(subject, message, f"PROBO <{email_from}>", recipient_list, connection=connection)
            msg.content_subtype = "html"
            msg.send()