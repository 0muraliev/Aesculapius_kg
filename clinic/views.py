from django.contrib import messages
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import render, redirect

from .forms import ReviewForm
from .models import Clinic, Review, MedicalDepartment


def clinics(request):
    """Страница всех клиник, а также поисковик"""
    if 'key' in request.GET:
        key = request.GET.get('key')
        # SQLite не поддерживает поиск без учета регистра
        clinics = Clinic.objects.filter(
            Q(name__icontains=key) |
            Q(medical_departments__name__icontains=key) |
            Q(address__icontains=key)
        ).distinct()
    else:
        clinics = Clinic.objects.all()

    """Пагинация страницы"""
    paginator = Paginator(clinics, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'clinic/clinics.html', {'clinics': clinics,
                                                   'page_obj': page_obj})


def clinic(request, slug, id):
    """Все о клинике"""
    clinic = Clinic.objects.get(slug=slug, id=id)
    favorite_add_or_remove(request, clinic)
    return review_leave_or_change(request, clinic)


def favorite_add_or_remove(request, clinic):
    """
    Метод добавления/удаления клиники в/из Избранные
    """
    try:
        if 'favorite' in request.POST:
            clinic.favorite_clinics.add(request.user.profile)
            messages.info(request, 'Сохранено в избранные.')

        elif 'favorite_remove' in request.POST:
            clinic.favorite_clinics.remove(request.user.profile)
            messages.info(request, 'Удалено из избранных.')

    except AttributeError:
        messages.info(request, 'Чтобы сохранить клинику в Избранные, нужно авторизоваться')


def review_leave_or_change(request, clinic):
    """Методы оставить отзыв/изменить отзыв"""
    reviews = Review.objects.filter(clinic__name=clinic)
    if not request.user.is_authenticated:
        return render(request, 'clinic/clinic.html', {'clinic': clinic,
                                                      'reviews': reviews})

    if not reviews:
        return render(request, 'clinic/clinic.html', {'clinic': clinic,
                                                      'reviews': reviews,
                                                      'form': ReviewForm()})

    elif reviews:
        if 'review_leave' in request.POST:
            form = ReviewForm(data=request.POST)
            if form.is_valid():
                clinic_review = form.save(commit=False)
                clinic_review.clinic = clinic
                clinic_review.user = request.user
                try:
                    clinic_review.save()
                    messages.success(request, 'Вы успешно оставили отзыв!')
                except IntegrityError:
                    messages.info(request, 'Вы уже оставили свой отзыв:)')

                return redirect('clinic', slug=clinic.slug, id=clinic.id)
            else:
                messages.error(request, 'Пожалуйста, исправьте ошибку ниже.')

        elif 'review_change' in request.POST:
            review = reviews.get(user_id=request.user.id)
            form_change = ReviewForm(data=request.POST, instance=review)
            if form_change.is_valid():
                form_change.save()
                messages.info(request, 'Комментарий изменен')
                return redirect('clinic', slug=clinic.slug, id=clinic.id)
            else:
                form_change = ReviewForm(instance=review)
                return render(request, 'clinic/clinic.html', {'clinic': clinic,
                                                              'form': ReviewForm(),
                                                              'form_change': form_change,
                                                              'reviews': reviews})

        return render(request, 'clinic/clinic.html', {'clinic': clinic,
                                                      'form': ReviewForm(),
                                                      'reviews': reviews})


def departments(request):
    """Все медицинские отделения"""
    return render(request, 'clinic/departments.html',
                  {'departments': MedicalDepartment.objects.order_by('name')})


def department(request, slug):
    """Клиники связанные с медицинским отделением"""
    department_clinics = Clinic.objects.filter(medical_departments__slug=slug)
    department = MedicalDepartment.objects.get(slug=slug)
    return render(request, 'clinic/department-clinics.html',
                  {'department_clinics': department_clinics, 'department': department})
