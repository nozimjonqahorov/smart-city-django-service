from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.http import JsonResponse
from .models import Viloyat, Tuman


def send_activation_email(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    activation_url = request.build_absolute_uri(
        reverse('activate_account', kwargs={'uidb64': uid, 'token': token})
    )
    message = (
        f"Assalomu alaykum, {user.first_name or user.username}!\n\n"
        "Smart City hisobingizni tasdiqlash uchun quyidagi havolani oching:\n"
        f"{activation_url}\n\n"
        "Agar bu ro'yxatdan o'tishni siz qilmagan bo'lsangiz, xabarni e'tiborsiz qoldiring."
    )
    send_mail(
        "Smart City hisobingizni tasdiqlang",
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            form.save_m2m()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            authenticated_user = authenticate(request, username=username, password=raw_password)
            if authenticated_user is not None:
                login(request, authenticated_user)
            else:
                # Fall back to explicit backend assignment when authenticate cannot resolve the backend.
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def activate_account(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save(update_fields=['is_active'])
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return redirect('dashboard')

    return render(request, 'accounts/account_activation_invalid.html')

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, 'Profilingiz muvaffaqiyatli yangilandi!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'u_form': u_form})

class MyPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('profile')


# JSON API Views for Region and District selection
def get_viloyatlar(request):
    viloyatlar = list(Viloyat.objects.order_by('name').values('id', 'name'))
    return JsonResponse({'regions': viloyatlar})


def get_tumanlar(request, viloyat_id):
    if not Viloyat.objects.filter(id=viloyat_id).exists():
        return JsonResponse({'error': 'Viloyat topilmadi'}, status=404)

    tumanlar = list(
        Tuman.objects.filter(viloyat_id=viloyat_id)
        .order_by('name')
        .values('id', 'name')
    )
    return JsonResponse({'districts': tumanlar})
