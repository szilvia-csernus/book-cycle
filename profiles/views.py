from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


from .models import UserProfile
from .forms import UserProfileForm, CustomSignupForm
from orders.models import Order

from allauth.socialaccount.models import SocialAccount
from allauth.account.views import SignupView


class CustomSignupView(SignupView):
    form_class = CustomSignupForm


@login_required
def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)
    user = request.user

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Update failed. \
                Please ensure the form is valid.')
    else:
        form = UserProfileForm(instance=profile)

    orders = profile.orders.all()
    template = 'profiles/profile.html'
    context = {
        'user': user,
        'full_name': user.get_full_name(),
        'form': form,
        'orders': orders,
    }

    return render(request, template, context)


@login_required
def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'orders/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)


@login_required
@require_POST
def delete_profile(request):
    """ Delete the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)
    socialaccount = SocialAccount.objects.filter(user=profile.user)

    if profile.user.is_staff:
        messages.warning(request, 'Staff accounts cannot be deleted.')
        return redirect(reverse('profile'))

    if socialaccount.exists():
        socialaccount.delete()
        messages.success(request, 'Social account deleted successfully')

    profile.user.delete()
    messages.success(request, 'Profile deleted successfully')
    return redirect(reverse('home'))
