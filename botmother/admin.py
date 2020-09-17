from django.contrib import admin
from botmother.models import Chat, Push
from django.utils.html import format_html


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'chat_id',
        'type',
        'username',
        'last_activity',
    )

    fields = (
        'first_name',
        'chat_id',
        'type',
        'username',
    )


@admin.register(Push)
class PushAdmin(admin.ModelAdmin):
    def admin_image(self, obj):
        image = format_html(
            f'<a href="/{obj.image.url}"><img src="/{obj.image.url}" width="100"/><a>'
        ) if obj.image else None

        return image

    admin_image.allow_tags = True

    list_display = ('admin_image',)
    fields = ('image', 'sms')
