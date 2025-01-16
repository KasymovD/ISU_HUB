from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from photos.models import Photo


# Создаём группы и назначаем права
@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('activity', 'description', 'uploaded_at', 'uploader')
    list_filter = ('uploaded_at', 'file_type')

def setup_groups():
    # Создаём группу "Photo Uploaders"
    photo_uploaders, created = Group.objects.get_or_create(name='Photo Uploaders')
    # Права для Photo Uploaders
    content_type = ContentType.objects.get_for_model(Photo)
    permissions = Permission.objects.filter(content_type=content_type, codename__in=['add_photo', 'change_photo'])
    photo_uploaders.permissions.set(permissions)

    # Создаём группу "Super Admins"
    super_admins, created = Group.objects.get_or_create(name='Super Admins')
    # Super Admins получают все права
    all_permissions = Permission.objects.all()
    super_admins.permissions.set(all_permissions)

class LimitedAdminSite(admin.AdminSite):
    site_header = "Photo Uploader Admin"

    def has_permission(self, request):
        return request.user.is_active and request.user.groups.filter(name='Photo Uploaders').exists()

limited_admin_site = LimitedAdminSite(name='limited_admin')
limited_admin_site.register(Photo, PhotoAdmin)

# Вызов функции для настройки групп при загрузке админки
setup_groups()
