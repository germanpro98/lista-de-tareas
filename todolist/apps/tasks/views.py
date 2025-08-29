from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, TaskImage
from .forms import TaskForm, TaskImageForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user).order_by('-id')

    if request.method == 'POST':
        task_form = TaskForm(request.POST)
        image_form = TaskImageForm(request.POST, request.FILES)

        if task_form.is_valid() and image_form.is_valid():   #aqui se valida
            task = task_form.save(commit=False)   #aqui se guarda la tarea
            task.user = request.user  # Asigna la tarea al usuario actual
            task.save()   #aqui se guarda la tarea
            
            for field_name in ['image1', 'image2', 'image3']:   #aqui se obtienen las imagenes
                img = image_form.cleaned_data.get(field_name)  #aqui se obtiene cada imagen
                if img:  
                    TaskImage.objects.create(task=task, image=img)  #aqui se crea la imagen
        return redirect('task_list')   #aqui se redirige a la lista de tareas

    else:
        task_form = TaskForm()
        image_form = TaskImageForm()

    return render(request, 'task_list.html', {
        'tasks': tasks,
        'task_form': task_form,
        'image_form': image_form
    })


@require_POST
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)  # Solo del usuario actual
    task.completed = not task.completed
    task.save()
    return redirect('task_list')

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    TaskImageFormSet = modelformset_factory(TaskImage, fields=('image',), extra=0, can_delete=True)

    if request.method == 'POST':
        task_form = TaskForm(request.POST, instance=task)
        image_formset = TaskImageFormSet(request.POST, request.FILES, queryset=task.images.all())
        new_images = request.FILES.getlist('new_images')

        if task_form.is_valid() and image_formset.is_valid():
            task_form.save()
            image_formset.save()

            # Limitar a 3 imágenes
            existing_count = task.images.count()
            if existing_count + len(new_images) > 3:
                # Puedes mostrar un mensaje de error aquí si querés
                pass
            else:
                for img in new_images:
                    TaskImage.objects.create(task=task, image=img)

            return redirect('task_list')
    else:
        task_form = TaskForm(instance=task)
        image_formset = TaskImageFormSet(queryset=task.images.all())

    context = {
        'form': task_form,
        'image_formset': image_formset,
        'task': task,
    }
    return render(request, 'edit_task.html', context)


def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        task.delete()
        return redirect('task_list')

    return render(request, 'confirm_delete.html', {'task': task})

