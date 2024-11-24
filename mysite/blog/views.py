from django.shortcuts import render, get_object_or_404, redirect
from .forms import AthleteForm
from .models import Athlete, Equipment
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.utils.timezone import make_aware
from datetime import datetime
import json

def add_athlete(request):
    athlete = None
    if request.method == 'POST':
        athlete_id = request.POST.get('athlete_id')
        if athlete_id:
            athlete = get_object_or_404(Athlete, id=athlete_id)

        form = AthleteForm(request.POST, instance=athlete) 
        if form.is_valid():
            athlete = form.save(commit=False)

            old_equipment = athlete.current_equipment
            new_equipment_id = request.POST.get('current_equipment')

            if old_equipment and old_equipment.id != int(new_equipment_id):
                old_equipment.status = 'libre'
                old_equipment.save()

            if new_equipment_id:
                new_equipment = get_object_or_404(Equipment, id=new_equipment_id)

                if athlete.is_using_machine:
                    new_equipment.status = 'occupé'
                else:
                    new_equipment.status = 'libre'

                new_equipment.save()
                athlete.current_equipment = new_equipment
            else:
                athlete.current_equipment = None

            athlete.save()
            messages.success(request, "Athlète ajouté ou modifié avec succès.")
            return redirect('athlete_list')
        else:
            messages.error(request, "Erreur dans le formulaire. Veuillez vérifier les champs.")
    else:
        athlete_id = request.GET.get('id')
        if athlete_id:
            athlete = get_object_or_404(Athlete, id=athlete_id)
        form = AthleteForm(instance=athlete)

    return render(request, 'blog/add_athlete.html', {'form': form, 'athlete': athlete})

def athlete_list(request):
    athletes = Athlete.objects.all()
    all_equipments = Equipment.objects.filter(status='libre')

    if request.method == 'POST' and 'athlete_id' in request.POST and 'action' in request.POST:
        athlete_id = request.POST.get('athlete_id')
        try:
            athlete = Athlete.objects.get(id=athlete_id)
            if request.POST.get('action') == "delete":
                athlete.delete()
                messages.success(request, f"L'athlète {athlete.name} a été supprimé avec succès!")
        except Athlete.DoesNotExist:
            messages.error(request, "L'athlète demandé n'existe pas.")
        return redirect('athlete_list')

    return render(request, 'blog/athlete_list.html', {
        'athletes': athletes,
        'all_equipments': all_equipments,
    })

def update_equipment_status(request, equipment_id=None):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': "Méthode non autorisée."})
    
    try:
        if equipment_id:
            equipment = get_object_or_404(Equipment, id=equipment_id)
            new_status = request.POST.get('status')

            if new_status == 'réservé':
                reserved_by_username = request.POST.get('reserved_by', '').strip()
                reservation_date = request.POST.get('reservation_date')
                reservation_time = request.POST.get('reservation_time')
                
                if not all([reserved_by_username, reservation_date, reservation_time]):
                    return JsonResponse({'status': 'error', 'message': "Veuillez remplir tous les champs de réservation."})

                try:
                    user = User.objects.get(username=reserved_by_username)
                    reservation_datetime = make_aware(datetime.strptime(f"{reservation_date} {reservation_time}", "%Y-%m-%d %H:%M"))

                    equipment.status = new_status
                    equipment.reserved_by = user
                    equipment.reservation_datetime = reservation_datetime
                    equipment.save()

                except User.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': "Utilisateur non trouvé."})
                except ValueError:
                    return JsonResponse({'status': 'error', 'message': "Format de date ou d'heure invalide."})

            else:
                equipment.status = new_status
                equipment.reserved_by = None
                equipment.reservation_datetime = None
                equipment.save()

            return JsonResponse({
                'status': 'success',
                'message': f"L'état de l'équipement {equipment.name} a été mis à jour à {new_status}."
            })
        # Si equipment_id n'est pas fourni, mise à jour via le corps de la requête
        else:
            data = json.loads(request.body)
            response_data = {'success': True, 'updated_equipment': []}

            if data.get('current_equipment'):
                equipment = get_object_or_404(Equipment, id=data['current_equipment'])
                equipment.status = 'occupé'
                equipment.save()
                response_data['updated_equipment'].append({'id': equipment.id, 'status': equipment.status})

            if data.get('reservation_equipment'):
                equipment = get_object_or_404(Equipment, id=data['reservation_equipment'])
                equipment.status = 'réservé'
                if data.get('reservation_date'):
                    equipment.reservation_date = data['reservation_date']
                if data.get('reservation_time'):
                    equipment.reservation_time = data['reservation_time']
                equipment.save()
                response_data['updated_equipment'].append({'id': equipment.id, 'status': equipment.status})

            return JsonResponse(response_data)

    except Equipment.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': "Équipement non trouvé."})

def equipment_list(request):
    all_equipments = Equipment.objects.all()
    available_count = Equipment.objects.filter(status='libre').count()
    in_use_count = Equipment.objects.filter(status='occupé').count()
    total_athletes = Athlete.objects.all()
    form_athlete = AthleteForm()

    context = {
        'all_equipments': all_equipments,
        'available_count': available_count,
        'in_use_count': in_use_count,
        'total_athletes': total_athletes,
        'form_athlete': form_athlete,
    }

    if request.method == 'POST':
        if 'submit_athlete' in request.POST:
            form_athlete = AthleteForm(request.POST)
            if form_athlete.is_valid():
                athlete = form_athlete.save()
                messages.success(request, f"L'athlète {athlete.name} a été ajouté avec succès!")
                return redirect('equipment_list')
            else:
                messages.error(request, "Erreur dans le formulaire d'athlète")

    return render(request, 'blog/equipment_list.html', context)

def home(request):
    if request.method == 'POST' and 'submit_athlete' in request.POST:
        form_athlete = AthleteForm(request.POST)
        if form_athlete.is_valid():
            form_athlete.save()
            messages.success(request, "L'athlète a été ajouté avec succès!")
            return redirect('home')  
    else:
        form_athlete = AthleteForm()

    context = {
        'form_athlete': form_athlete,
        'total_athletes': Athlete.objects.all(),
        'all_equipments': Equipment.objects.all(),  
    }
    return render(request, 'blog/home.html', context)

def delete_athlete(request, athlete_id):
    athlete = get_object_or_404(Athlete, id=athlete_id)
    
    if request.method == 'POST':
        if athlete.current_equipment:
            equipment = athlete.current_equipment
            equipment.status = 'libre'
            equipment.save()

        athlete.delete()
        
        return JsonResponse({'success': True, 'message': 'Athlète supprimé avec succès.'})

    elif request.method == 'GET':  
        if athlete.current_equipment:
            equipment = athlete.current_equipment
            equipment.status = 'libre'
            equipment.save()
        
        athlete.delete()
        
        return JsonResponse({'success': True, 'message': 'Athlète supprimé avec succès.'})
    
    return JsonResponse({'success': False, 'message': 'Erreur lors de la suppression.'})