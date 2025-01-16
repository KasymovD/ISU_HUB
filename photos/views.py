from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from .models import Photo
from .forms import PhotoForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.postgres.search import SearchVector, SearchQuery
from django.db.models import Q
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.contrib.auth.models import User, Group

# photos/views.py

def is_super_admin_or_photo_uploader(user):
    return user.is_superuser or user.groups.filter(name='Photo Uploaders').exists()

# Проверка: является ли пользователь администратором
def is_admin(user):
    return user.is_superuser

def is_photo_uploader(user):
    return user.groups.filter(name='Photo Uploaders').exists()

@login_required(login_url='login')  # Перенаправление на 'login' при неаутентифицированном пользователе
@user_passes_test(is_super_admin_or_photo_uploader, login_url='login')  # Проверка на супер админа или группу
def photo_upload(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.uploader = request.user  # Назначение текущего пользователя как загрузчика
            photo.save()
            return redirect('photo_list')
    else:
        form = PhotoForm()

    return render(request, 'photos/photo_upload.html', {'form': form})

def is_super_admin(user):
    return user.is_superuser or user.groups.filter(name='Super Admins').exists()

def photo_list(request):
    query = request.GET.get('q', '')
    file_type = request.GET.get('file_type', '')
    location = request.GET.get('location', '')
    event_type = request.GET.get('event_type', '')
    camera_shot = request.GET.get('camera_shot', '')
    camera_angle = request.GET.get('camera_angle', '')
    atmosphere = request.GET.get('atmosphere', '')
    language = request.GET.get('language', '')
    race = request.GET.get('race', '')

    # Списки для выпадающих фильтров
    file_type_choices = ['Photo', 'Video']
    location_choices = ['Off-campus', 'On-campus']
    event_type_choices = [
        'Award', 'Seminar', 'Performance', 'Conference', 'Speech',
        'Pickup', 'Cultural', 'Cultural Experience', 'Booth',
        'Corporate Trip', 'Others'
    ]
    camera_shot_choices = ['Long Shot', 'Close Shot', 'Medium Shot']
    camera_angle_choices = ['Back', 'Front', 'Side', 'High-angle', 'Low-angle']
    atmosphere_choices = ['Not recognized', 'Positive', 'Joyful', 'Serious', 'Interactive']
    language_choices = ['English', 'Chinese', 'Other']
    race_choices = ['White', 'Asian', 'Afro', 'Other']

    # Начальный набор данных
    photos = Photo.objects.all()

    # Применение поиска
    if query:
        photos = photos.filter(
            Q(activity__icontains=query) |
            Q(description__icontains=query)
        )

    # Применение фильтров
    if file_type:
        photos = photos.filter(file_type=file_type)
    if location:
        photos = photos.filter(location=location)
    if event_type:
        photos = photos.filter(event_type=event_type)
    if camera_shot:
        photos = photos.filter(camera_shot=camera_shot)
    if camera_angle:
        photos = photos.filter(camera_angle=camera_angle)
    if atmosphere:
        photos = photos.filter(atmosphere=atmosphere)
    if language:
        photos = photos.filter(language=language)
    if race:
        photos = photos.filter(race=race)

    # Настройка пагинации: 9 фотографий на страницу
    paginator = Paginator(photos, 9)  # 9 объектов на страницу
    page = request.GET.get('page')

    try:
        photos_page = paginator.page(page)
    except PageNotAnInteger:
        photos_page = paginator.page(1)
    except EmptyPage:
        photos_page = paginator.page(paginator.num_pages)

    current_year = datetime.datetime.now().year

    return render(request, 'photos/photo_list.html', {
        'photos': photos_page,
        'file_type_choices': file_type_choices,
        'location_choices': location_choices,
        'event_type_choices': event_type_choices,
        'camera_shot_choices': camera_shot_choices,
        'camera_angle_choices': camera_angle_choices,
        'atmosphere_choices': atmosphere_choices,
        'language_choices': language_choices,
        'race_choices': race_choices,
        'current_year': current_year,
    })

@login_required
@user_passes_test(is_super_admin, login_url='login')  # Ограничение для супер админов
def photo_delete(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if request.user.is_superuser:  # Только админы могут удалять
        photo.delete()
        return redirect('photo_list')
    else:
        return redirect('photo_list')  # Если не админ, перенаправить на список

def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    return render(request, 'photos/photo_detail.html', {'photo': photo})

def resize_image(image_field, width=300, height=200):
    img = Image.open(image_field)
    img = img.convert('RGB')
    img = img.resize((width, height), Image.ANTIALIAS)

    buffer = BytesIO()
    img.save(buffer, format='JPEG')
    file_content = ContentFile(buffer.getvalue())

    return file_content

@login_required(login_url='login')
@user_passes_test(is_super_admin_or_photo_uploader, login_url='login')
def manage_uploads(request):
    photos = Photo.objects.all()
    return render(request, 'photos/manage_uploads.html', {'photos': photos})