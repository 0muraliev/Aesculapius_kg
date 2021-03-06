from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from clinic.models import Clinic
from user_account.decorators import clinic_required, doctor_required
from user_account.models import Profile, Doctor
from .forms import MessageForm, AppointmentForm, LetterForm
from .models import Appointment


def contact(request):
    """Контактные данные сайта."""
    if request.method == 'POST':
        form = MessageForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            try:
                message.user = request.user
                message.email = request.user.email
                message.save()
                messages.success(request, 'Сообщение отправлено.')
            except AttributeError:
                messages.info(request, 'Чтобы отправить сообщение, пожалуйста, войдите в аккаунт.')
            except ValueError:
                messages.info(request, 'Чтобы оставить заявку, авторизуйтесь через аккаунт профиля.'
                                       ' Или воспользуйтесь нашими контактными данными.')
            return redirect('contact')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибку ниже.')

    return render(request, 'communication/contact.html', {'form': MessageForm})


@login_required
def make_appointment_clinic(request, id):
    """Отправка заявки на прием в клинику."""
    clinic = Clinic.objects.get(id=id)
    if request.method == 'POST':
        form = AppointmentForm(data=request.POST)
        if form.is_valid():
            try:
                profile = request.user.profile
                appointment_form = Appointment(
                    user=request.user,
                    profile=profile,
                    clinic=clinic,
                    email=request.user.email,
                    phone_number=form.cleaned_data['phone_number'],
                    message=form.cleaned_data['message'],
                    itn=profile.itn,
                    birth_date=profile.birth_date,
                    gender=profile.gender,
                    blood_type=profile.blood_type
                )
                appointment_form.save()
                messages.success(
                    request,
                    'Заявка отправлена. В течение 24 часов мы отправим Вам письмо в личный кабинет.'
                )
            except Profile.DoesNotExist:
                messages.info(
                    request,
                    'Чтобы записаться на прием, авторизуйтесь через аккаунт профиля.'
                )
        else:
            messages.info(request, 'Пожалуйста, проверьте правильность заполнения формы.')

    appointment_form = AppointmentForm()
    return render(request, 'communication/appointment.html', {'appointment_form': appointment_form,
                                                              'clinic': clinic})


@login_required
def make_appointment_doctor(request, id):
    """Отправка заявки на прием к доктору."""
    doctor = Doctor.objects.get(id=id)
    if request.method == 'POST':
        form = AppointmentForm(data=request.POST)
        if form.is_valid():
            try:
                profile = request.user.profile
                appointment_form = Appointment(
                    user=request.user,
                    profile=profile,
                    email=request.user.email,
                    phone_number=form.cleaned_data['phone_number'],
                    message=form.cleaned_data['message'],
                    itn=profile.itn,
                    birth_date=profile.birth_date,
                    gender=profile.gender,
                    blood_type=profile.blood_type
                )
                appointment_form.save()
                messages.success(
                    request,
                    'Заявка отправлена. В течение 24 часов мы отправим Вам письмо в личный кабинет.'
                )
            except Profile.DoesNotExist:
                messages.info(
                    request,
                    'Чтобы записаться на прием, авторизуйтесь через аккаунт профиля.'
                )
        else:
            messages.info(request, 'Пожалуйста, проверьте правильность заполнения формы.')

    appointment_form = AppointmentForm()
    return render(request, 'communication/appointment.html', {'appointment_form': appointment_form,
                                                              'doctor': doctor})


@clinic_required
def letter_clinic(request, id):
    """Отправка сообщения клиенту от клиники."""
    clinic = Clinic.objects.get(user_id=request.user)
    appointment = Appointment.objects.get(id=id)
    if request.method == 'POST':
        form = LetterForm(request.POST)
        if form.is_valid():
            letter_form = form.save(commit=False)
            letter_form.appointment = appointment
            letter_form.save()
            messages.info(request, 'Письмо отправлено')
            return redirect('clinic_profile', id=clinic.id)

    return render(request, 'communication/letter.html', {'appointment': appointment,
                                                         'clinic': clinic,
                                                         'letter_form': LetterForm()})


@doctor_required
def letter_doctor(request, id):
    """Отправка сообщения клиенту от доктора."""
    doctor = Doctor.objects.get(user_id=request.user)
    appointment = Appointment.objects.get(id=id)
    if request.method == 'POST':
        form = LetterForm(request.POST)
        if form.is_valid():
            letter_form = form.save(commit=False)
            letter_form.appointment = appointment
            letter_form.save()
            messages.info(request, 'Письмо отправлено')
            return redirect('doctor_profile', id=doctor.id)

    return render(request, 'communication/letter.html', {'appointment': appointment,
                                                         'doctor': doctor,
                                                         'letter_form': LetterForm()})
