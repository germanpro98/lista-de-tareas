from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CustomUserChangeForm  # ✅ Solo este es necesario
from django.contrib.auth.views import LogoutView


@login_required
def profile_edit(request):
    user = request.user  # Esto es un CustomUser

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('task_list') #redirecciona a la pagina de inicio
    else:
        form = CustomUserChangeForm(instance=user)

    return render(request, 'profile_edit.html', {'form': form})

class LogoutGetRedirectView(LogoutView):
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return redirect('login')
