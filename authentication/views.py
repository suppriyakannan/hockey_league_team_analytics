from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout

from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from .models import CustomUser
def is_superuser(user):
    return user.is_superuser
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('/login/')  # Assuming you have a URL named 'login'
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/home/')
        else:
            return render(request, 'templates/login.html', {'error': 'Invalid credentials'})
    else:
        if request.user.is_authenticated:
            return redirect('/home/')
        return render(request, 'login.html')


@login_required(login_url='/login/')
@user_passes_test(lambda user: user.is_superuser, login_url='/login/', redirect_field_name=None)
def home_view(request):
    return render(request, 'templates/home.html')

def image_view(request):
    return render(request,'templates/background.jpg')

def match_analysis_view(request):
    return render(request, 'templates/match.html')

def record_view(request):
    return render(request, 'templates/record.html')

def visualize_view(request):
    return render(request, 'templates/visualize.html')

from django.shortcuts import render,redirect
from .models import Team

def ballpossession_view(request):
    teams = Team.objects.all()
    return render(request, 'templates/ballpossession.html', {'teams': teams})

from .forms import PossessionDataForm

# views.py

from django.http import JsonResponse
from .models import PossessionData
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def record_possession_data(request):
    if request.method == 'POST':
        # Extract data from request.POST and save it
        PossessionData.objects.create(
            match_number=request.POST.get('match_number'),
            team1_name=request.POST.get('team1_name'),
            team2_name=request.POST.get('team2_name'),
            team1_possession_percentage=request.POST.get('team1_possession_percentage'),
            team2_possession_percentage=request.POST.get('team2_possession_percentage')
        )
        return JsonResponse({'message': 'Data stored successfully!'})

    return JsonResponse({'error': 'Request must be POST.'}, status=400)

def goal_view(request):
    teams = Team.objects.all()
    return render(request, 'templates/goal.html', {'teams': teams})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Goal,Circle,Shots,Card,PC,PS

@csrf_exempt
def save_goals(request):
    if request.method == 'POST':
        # Extract all data from the request
        data = request.POST
        match_number = int(data.get('match_number'))
        team1_FG = int(data.get('team1_FG'))
        team1_PG = int(data.get('team1_PG'))
        team2_FG = int(data.get('team2_FG'))
        team2_PG = int(data.get('team2_PG'))
        team1_total = int(data.get('team1_total'))
        team2_total = int(data.get('team2_total'))
        team1_circle = int(data.get('team1_circle'))
        team1_shots = int(data.get('team1_shots'))
        team2_circle = int(data.get('team2_circle'))
        team2_shots = int(data.get('team2_shots'))

        # Update or create the goal record
        goal, created = Goal.objects.update_or_create(
            match_number=match_number,
            defaults={
                'team1_name': data.get('team1'), 
                'team2_name': data.get('team2'),
                'team1_FG': team1_FG, 'team1_PG': team1_PG,
                'team2_FG': team2_FG, 'team2_PG': team2_PG,
                'team1_total': team1_total, 'team2_total': team2_total
            }
        )
        circle, created = Circle.objects.update_or_create(
            match_number=match_number,
            defaults={
                'team1_name': data.get('team1'), 
                'team2_name': data.get('team2'),
                'team1_circle': team1_circle, 'team2_circle': team2_circle,
            }
        )
        shots, created = Shots.objects.update_or_create(
            match_number=match_number,
            defaults={
                'team1_name': data.get('team1'), 
                'team2_name': data.get('team2'),
                'team1_shots': team1_shots, 'team2_shots': team2_shots,
            }
        )
        return JsonResponse({'status': 'success'})
    return JsonResponse({'error': 'Invalid request'}, status=400)
from django.views.decorators.http import require_http_methods

@csrf_exempt
@require_http_methods(["POST"])
def check_match_number(request):
    match_number = int(request.POST.get('match_number', 0))
    exists = Goal.objects.filter(match_number=match_number).exists()
    return JsonResponse({'exists': exists})


def penalty_view(request):
    teams = Team.objects.all()
    return render(request, 'templates/penalty.html', {'teams': teams})


@csrf_exempt
def save_penalty(request):
    if request.method == 'POST':
        # Extract all data from the request
        data = request.POST
        match_number = int(data.get('match_number'))
        team1_gy = int(data.get('team1_gy'))
        team1_r = int(data.get('team1_r'))
        team2_gy = int(data.get('team2_gy'))
        team2_r = int(data.get('team2_r'))
        team1_total = int(data.get('team1_total'))
        team2_total = int(data.get('team2_total'))
        team1_pc = int(data.get('team1_pc'))
        team1_ps = int(data.get('team1_ps'))
        team2_pc = int(data.get('team2_pc'))
        team2_ps = int(data.get('team2_ps'))

        # Update or create the goal record
        card, created = Card.objects.update_or_create(
            match_number=match_number,
            defaults={
                'team1_name': data.get('team1'), 
                'team2_name': data.get('team2'),
                'team1_gy': team1_gy, 'team1_r': team1_r,
                'team2_gy': team2_gy, 'team2_r': team2_r,
                'team1_total': team1_total, 'team2_total': team2_total
            }
        )
        pc, created = PC.objects.update_or_create(
            match_number=match_number,
            defaults={
                'team1_name': data.get('team1'), 
                'team2_name': data.get('team2'),
                'team1_pc': team1_pc, 'team2_pc': team2_pc,
            }
        )
        ps, created = PS.objects.update_or_create(
            match_number=match_number,
            defaults={
                'team1_name': data.get('team1'), 
                'team2_name': data.get('team2'),
                'team1_ps': team1_ps, 'team2_ps': team2_ps,
            }
        )
        return JsonResponse({'status': 'success'})
    return JsonResponse({'error': 'Invalid request'}, status=400)
from django.views.decorators.http import require_http_methods

@csrf_exempt
@require_http_methods(["POST"])
def check_match_number1(request):
    match_number = int(request.POST.get('match_number', 0))
    exists = Card.objects.filter(match_number=match_number).exists()
    return JsonResponse({'exists': exists})

@csrf_exempt
@require_http_methods(["POST"])
def check_match_number2(request):
    match_number = int(request.POST.get('match_number', 0))
    exists = PossessionData.objects.filter(match_number=match_number).exists()
    return JsonResponse({'exists': exists})

from django.http import JsonResponse
from .models import Goal, PossessionData, Card, Circle, PC, PS, Shots

def api_goals(request):
    count = request.GET.get('count', 'all')
    data = Goal.objects.all().order_by('-match_number')
    if count != 'all':
        data = data[:int(count)]
    data = list(data.values('match_number', 'team1_name', 'team2_name', 'team1_FG', 'team1_PG', 'team2_FG', 'team2_PG'))
    return JsonResponse(data, safe=False)

def api_possession(request):
    count = request.GET.get('count', 'all')
    data = PossessionData.objects.all().order_by('-match_number')
    if count != 'all':
        data = data[:int(count)]
    data = list(data.values('match_number', 'team1_name', 'team2_name', 'team1_possession_percentage', 'team2_possession_percentage'))
    return JsonResponse(data, safe=False)

def api_cards(request):
    count = request.GET.get('count', 'all')
    data = Card.objects.all().order_by('-match_number')
    if count != 'all':
        data = data[:int(count)]
    data = list(data.values('match_number', 'team1_name', 'team2_name', 'team1_gy', 'team1_r', 'team2_gy', 'team2_r'))
    return JsonResponse(data, safe=False)

def api_circle(request):
    count = request.GET.get('count', 'all')
    data = Circle.objects.all().order_by('-match_number')
    if count != 'all':
        data = data[:int(count)]
    data = list(data.values('match_number', 'team1_name', 'team2_name', 'team1_circle', 'team2_circle'))
    return JsonResponse(data, safe=False)

def api_shots(request):
    count = request.GET.get('count', 'all')
    data = Shots.objects.all().order_by('-match_number')
    if count != 'all':
        data = data[:int(count)]
    data = list(data.values('match_number', 'team1_name', 'team2_name', 'team1_shots', 'team2_shots'))
    return JsonResponse(data, safe=False)

def api_penalty(request):
    count = request.GET.get('count', 'all')
    data = PC.objects.all().order_by('-match_number')
    if count != 'all':
        data = data[:int(count)]
    data = list(data.values('match_number', 'team1_name', 'team2_name', 'team1_pc', 'team2_pc'))
    ps_data = PS.objects.all().order_by('-match_number')
    if count != 'all':
        ps_data = ps_data[:int(count)]
    ps_data = list(ps_data.values('match_number', 'team1_name', 'team2_name', 'team1_ps', 'team2_ps'))
    for pc, ps in zip(data, ps_data):
        pc.update({
            'team1_ps': ps['team1_ps'],
            'team2_ps': ps['team2_ps']
        })
    return JsonResponse(data, safe=False)
from django.shortcuts import render
from .models import PossessionData, Goal, Circle, Shots, PC, PS, Card
from django.db import models
from django.http import JsonResponse

def matchspecs_view(request):
    return render(request, 'templates/matchspecs.html')


def get_max_match_number(request):
    max_match_numbers = [
        PossessionData.objects.aggregate(max_match_number=models.Max('match_number'))['max_match_number'],
        Goal.objects.aggregate(max_match_number=models.Max('match_number'))['max_match_number'],
        Circle.objects.aggregate(max_match_number=models.Max('match_number'))['max_match_number'],
        Shots.objects.aggregate(max_match_number=models.Max('match_number'))['max_match_number'],
        PC.objects.aggregate(max_match_number=models.Max('match_number'))['max_match_number'],
        PS.objects.aggregate(max_match_number=models.Max('match_number'))['max_match_number'],
        Card.objects.aggregate(max_match_number=models.Max('match_number'))['max_match_number']
    ]
    max_match_number = max(max_match_numbers) or 0  # Handle the case when max() returns None
    return JsonResponse({'max_match_number': max_match_number})


def get_goal_data(request, match_number):
    try:
        goals_data = Goal.objects.filter(match_number=match_number).values(
            'team1_name', 'team2_name', 'team1_FG', 'team1_PG', 'team2_FG', 'team2_PG', 'team1_total', 'team2_total'
        )
        goals_list = list(goals_data)
        return JsonResponse(goals_list, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_possession_data(request, match_number):
    try:
        possession_data = PossessionData.objects.get(match_number=match_number)
        data = {
            'team1_name': possession_data.team1_name,
            'team2_name': possession_data.team2_name,
            'team1_possession_percentage': float(possession_data.team1_possession_percentage),
            'team2_possession_percentage': float(possession_data.team2_possession_percentage)
        }
        return JsonResponse(data)
    except PossessionData.DoesNotExist:
        return JsonResponse({'error': 'Possession data not found for the specified match number'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

from django.http import JsonResponse
from .models import Circle, Shots, PC, PS, Card

def get_circle_data(request, match_number):
    try:
        circle_data = Circle.objects.get(match_number=match_number)
        data = {
            'team1_name': circle_data.team1_name,
            'team2_name': circle_data.team2_name,
            'team1_circle': circle_data.team1_circle,
            'team2_circle': circle_data.team2_circle
        }
        return JsonResponse(data)
    except Circle.DoesNotExist:
        return JsonResponse({'error': 'Circle data not found for the specified match number'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_pc_data(request, match_number):
    try:
        pc_data = PC.objects.get(match_number=match_number)
        data = {
            'team1_name': pc_data.team1_name,
            'team2_name': pc_data.team2_name,
            'team1_pc': pc_data.team1_pc,
            'team2_pc': pc_data.team2_pc
        }
        return JsonResponse(data)
    except PC.DoesNotExist:
        return JsonResponse({'error': 'PC data not found for the specified match number'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_shots_data(request, match_number):
    try:
        shots_data = Shots.objects.get(match_number=match_number)
        data = {
            'team1_name': shots_data.team1_name,
            'team2_name': shots_data.team2_name,
            'team1_shots': shots_data.team1_shots,
            'team2_shots': shots_data.team2_shots
        }
        return JsonResponse(data)
    except Shots.DoesNotExist:
        return JsonResponse({'error': 'Shots data not found for the specified match number'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_ps_data(request, match_number):
    try:
        ps_data = PS.objects.get(match_number=match_number)
        data = {
            'team1_name': ps_data.team1_name,
            'team2_name': ps_data.team2_name,
            'team1_ps': ps_data.team1_ps,
            'team2_ps': ps_data.team2_ps
        }
        return JsonResponse(data)
    except PS.DoesNotExist:
        return JsonResponse({'error': 'PS data not found for the specified match number'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_card_data(request, match_number):
    try:
        card_data = Card.objects.get(match_number=match_number)
        data = {
            'team1_name': card_data.team1_name,
            'team2_name': card_data.team2_name,
            'team1_gy': card_data.team1_gy,
            'team1_r': card_data.team1_r,
            'team2_gy': card_data.team2_gy,
            'team2_r': card_data.team2_r
        }
        return JsonResponse(data)
    except Card.DoesNotExist:
        return JsonResponse({'error': 'Card data not found for the specified match number'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
from django.shortcuts import render
from .models import Team, Goal

def standings(request):
    teams = Team.objects.all()
    teams_with_goals = []
    
    for team in teams:
        team_goals = Goal.objects.filter(team1_name=team.name).aggregate(total=models.Sum(models.F('team1_FG') + models.F('team1_PG')))['total'] or 0
        team_goals += Goal.objects.filter(team2_name=team.name).aggregate(total=models.Sum(models.F('team2_FG') + models.F('team2_PG')))['total'] or 0
        teams_with_goals.append({'team': team, 'total_goals': team_goals})
    
    teams_ranked = sorted(teams_with_goals, key=lambda x: x['total_goals'], reverse=True)
    return render(request, 'standings.html', {'teams_ranked': teams_ranked})

from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Injury
from .forms import InjuryForm
from django.db.models import Q, Count
import json
from datetime import date

def injury_dashboard(request):
    query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    form = InjuryForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('injury_dashboard')

    injuries_query = Injury.objects.all()

    if query:
        injuries_query = injuries_query.filter(player__name__icontains=query)
    
    if status_filter:
        injuries_query = injuries_query.filter(status=status_filter)
    
    paginator = Paginator(injuries_query, 5)  # Show 5 injuries per page.
    page_number = request.GET.get('page')
    injuries = paginator.get_page(page_number)

    injury_data = injuries.object_list.values('injury_type').annotate(total=Count('injury_type'))
    injury_data_json = json.dumps(list(injury_data))  # Prepare data for Chart.js
    current_date = date.today().isoformat()
    return render(request, 'injury_dashboard.html', {
        'form': form,
        'injuries': injuries,
        'injury_data': injury_data_json,
        'page_obj': injuries,  # Pass page object to the template for pagination controls
        'is_paginated': True if injuries.paginator.num_pages > 1 else False,
        'current_date': current_date
    })

def delete_injury(request, pk):
    injury = get_object_or_404(Injury, pk=pk)
    if request.method == 'POST':
        injury.delete()
        return redirect('injury_dashboard')

def edit_injury_status(request, pk):
    injury = get_object_or_404(Injury, pk=pk)
    if request.method == 'POST':
        status = request.POST.get('status')
        if status:
            injury.status = status
            injury.save()
        return redirect('injury_dashboard')
    return render(request, 'edit_injury_status_modal.html', {'injury': injury})

from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum, Q, F, When, Case, IntegerField, Value
from .models import Team, Goal, PossessionData, Circle, Shots, Card, PC, PS

def dashboard(request):
    teams = Team.objects.all()
    return render(request, 'dashboard.html', {'teams': teams})
from django.http import JsonResponse

def team_data(request, team_id):
    try:
        team = Team.objects.get(pk=team_id)

        # Get all teams and their total goals
        teams_with_goals = []
        teams = Team.objects.all()
        for t in teams:
            team_goals = Goal.objects.filter(team1_name=t.name).aggregate(
                total=Sum(F('team1_FG') + F('team1_PG'))
            )['total'] or 0
            team_goals += Goal.objects.filter(team2_name=t.name).aggregate(
                total=Sum(F('team2_FG') + F('team2_PG'))
            )['total'] or 0
            teams_with_goals.append({'team': t, 'total_goals': team_goals})

        # Sort teams by total goals in descending order to determine ranks
        teams_ranked = sorted(teams_with_goals, key=lambda x: x['total_goals'], reverse=True)

        # Find rank of the selected team
        team_rank = next((index for (index, d) in enumerate(teams_ranked, start=1) if d['team'].id == team.id), None)

        # Gather data for the selected team's charts
        goal_data = Goal.objects.filter(Q(team1_name=team.name) | Q(team2_name=team.name))
        goal_chart = {
            'labels': [f"Match {g.match_number}" for g in goal_data],
            'data': [g.team1_total if g.team1_name == team.name else g.team2_total for g in goal_data]
        }
            # Prepare Possession data
        possession_data = PossessionData.objects.filter(Q(team1_name=team.name) | Q(team2_name=team.name))
        possession_chart = {
            'labels': [f"Match {p.match_number}" for p in possession_data],
            'data': [p.team1_possession_percentage if p.team1_name == team.name else p.team2_possession_percentage for p in possession_data],
        }

            # Prepare Circle data
        circle_data = Circle.objects.filter(Q(team1_name=team.name) | Q(team2_name=team.name))
        circle_chart = {
            'labels': [f"Match {c.match_number}" for c in circle_data],
            'data': [c.team1_circle if c.team1_name == team.name else c.team2_circle for c in circle_data],
        }

            # Prepare Shots data
        shots_data = Shots.objects.filter(Q(team1_name=team.name) | Q(team2_name=team.name))
        shots_chart = {
            'labels': [f"Match {s.match_number}" for s in shots_data],
            'data': [s.team1_shots if s.team1_name == team.name else s.team2_shots for s in shots_data],
        }

            # Prepare Card data
        card_data = Card.objects.filter(Q(team1_name=team.name) | Q(team2_name=team.name))
        card_chart = {
            'labels': [f"Match {c.match_number}" for c in card_data],
            'data': [c.team1_total if c.team1_name == team.name else c.team2_total for c in card_data],
        }

            # Prepare PC data
        pc_data = PC.objects.filter(Q(team1_name=team.name) | Q(team2_name=team.name))
        pc_chart = {
            'labels': [f"Match {pc.match_number}" for pc in pc_data],
            'data': [pc.team1_pc if pc.team1_name == team.name else pc.team2_pc for pc in pc_data],
        }

            # Prepare PS data
        ps_data = PS.objects.filter(Q(team1_name=team.name) | Q(team2_name=team.name))
        ps_chart = {
            'labels': [f"Match {ps.match_number}" for ps in ps_data],
            'data': [ps.team1_ps if ps.team1_name == team.name else ps.team2_ps for ps in ps_data],
        }
        team_wins = goal_data.filter(
            Q(team1_name=team.name, team1_result=1) |
            Q(team2_name=team.name, team2_result=1)
        ).count()
        team_losses = goal_data.filter(
            Q(team1_name=team.name, team1_result=0) |
            Q(team2_name=team.name, team2_result=0)
        ).count()

        # Calculate rank
        team_win_counts = Goal.objects.values('team1_name', 'team2_name').annotate(
            win_count=Count(
                Case(
                    When(team1_result=1, then=Value(1)),
                    When(team2_result=1, then=Value(1)),
                    output_field=IntegerField()
                )
            )
        ).order_by('-win_count')

        data = {
            'team': {
                'name': team.name,
                'logo': team.logo.url if team.logo else None,
                'wins': team_wins,  # Calculate or retrieve similarly
                'losses': team_losses,  # Calculate or retrieve similarly
                'rank': team_rank,
            },
            'goal_chart': goal_chart,
            'possession_chart': possession_chart,  # Prepare similarly
            'circle_chart': circle_chart,  # Prepare similarly
            'shots_chart': shots_chart,  # Prepare similarly
            'card_chart': card_chart,  # Prepare similarly
            'pc_chart': pc_chart,  # Prepare similarly
            'ps_chart': ps_chart,  # Prepare similarly
        }

        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
from django.http import JsonResponse
from django.db.models import Sum
from .models import Team, Goal, Shots, Circle, PossessionData, PC, PS, Card

def stats_page(request):
    return render(request, 'templates/stats.html')

def calculate_average(data):
    total = sum(data.values())
    count = len(data)
    return total / count if count != 0 else 0

def get_stats(request):
    metric = request.GET.get('metric')
    teams = Team.objects.all()
    data = {}
    average_data = {}

    if metric == 'goals':
        for team in teams:
            goals = Goal.objects.filter(team1_name=team.name).aggregate(Sum('team1_total'))['team1_total__sum'] or 0
            goals += Goal.objects.filter(team2_name=team.name).aggregate(Sum('team2_total'))['team2_total__sum'] or 0
            data[team.name] = goals
        average_data['Average'] = calculate_average(data)

    elif metric == 'shots':
        for team in teams:
            shots = Shots.objects.filter(team1_name=team.name).aggregate(Sum('team1_shots'))['team1_shots__sum'] or 0
            shots += Shots.objects.filter(team2_name=team.name).aggregate(Sum('team2_shots'))['team2_shots__sum'] or 0
            data[team.name] = shots
        average_data['Average'] = calculate_average(data)

    elif metric == 'circles':
        for team in teams:
            circles = Circle.objects.filter(team1_name=team.name).aggregate(Sum('team1_circle'))['team1_circle__sum'] or 0
            circles += Circle.objects.filter(team2_name=team.name).aggregate(Sum('team2_circle'))['team2_circle__sum'] or 0
            data[team.name] = circles
        average_data['Average'] = calculate_average(data)

    elif metric == 'possession':
        for team in teams:
            possession = PossessionData.objects.filter(team1_name=team.name).aggregate(Sum('team1_possession_percentage'))['team1_possession_percentage__sum'] or 0
            possession += PossessionData.objects.filter(team2_name=team.name).aggregate(Sum('team2_possession_percentage'))['team2_possession_percentage__sum'] or 0
            data[team.name] = possession
        average_data['Average'] = calculate_average(data)

    elif metric == 'pc':
        for team in teams:
            pc = PC.objects.filter(team1_name=team.name).aggregate(Sum('team1_pc'))['team1_pc__sum'] or 0
            pc += PC.objects.filter(team2_name=team.name).aggregate(Sum('team2_pc'))['team2_pc__sum'] or 0
            data[team.name] = pc
        average_data['Average'] = calculate_average(data)

    elif metric == 'ps':
        for team in teams:
            ps = PS.objects.filter(team1_name=team.name).aggregate(Sum('team1_ps'))['team1_ps__sum'] or 0
            ps += PS.objects.filter(team2_name=team.name).aggregate(Sum('team2_ps'))['team2_ps__sum'] or 0
            data[team.name] = ps
        average_data['Average'] = calculate_average(data)

    elif metric == 'cards':
        for team in teams:
            cards = Card.objects.filter(team1_name=team.name).aggregate(Sum('team1_total'))['team1_total__sum'] or 0
            cards += Card.objects.filter(team2_name=team.name).aggregate(Sum('team2_total'))['team2_total__sum'] or 0
            data[team.name] = cards
        average_data['Average'] = calculate_average(data)

    return JsonResponse({**data, **average_data})

from django.shortcuts import render
from django.http import JsonResponse
from .models import Team, Goal, Shots, Circle, PossessionData
from django.db.models import Q, F, Case, When, Value, IntegerField
from django.core.exceptions import ObjectDoesNotExist

def game_metrics(request):
    teams = Team.objects.all()
    return render(request, 'game_metrics.html', {'teams': teams})

def fetch_game_data(request):
    team_id = request.GET.get('team_id')
    if not team_id:
        return JsonResponse({'error': 'Missing team ID'}, status=400)

    try:
        team = Team.objects.get(pk=team_id)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Team not found'}, status=404)

    # Fetch matches where the selected team was either team1 or team2
    matches = Goal.objects.filter(Q(team1_name=team.name) | Q(team2_name=team.name)).order_by('match_number').distinct()

    match_numbers = [match.match_number for match in matches]

    # Prepare data for Shots vs Goals chart
    shots = Shots.objects.filter(match_number__in=match_numbers)
    shots = shots.annotate(shots_value=Case(
        When(team1_name=team.name, then='team1_shots'),
        When(team2_name=team.name, then='team2_shots'),
        default=Value(0),
        output_field=IntegerField()))

    # Prepare data for Circle Entries vs Goals chart
    circles = Circle.objects.filter(match_number__in=match_numbers)
    circles = circles.annotate(circles_value=Case(
        When(team1_name=team.name, then='team1_circle'),
        When(team2_name=team.name, then='team2_circle'),
        default=Value(0),
        output_field=IntegerField()))

    # Prepare data for Possession Percentage vs Goals chart
    possessions = PossessionData.objects.filter(match_number__in=match_numbers)
    possessions = possessions.annotate(possession_value=Case(
        When(team1_name=team.name, then='team1_possession_percentage'),
        When(team2_name=team.name, then='team2_possession_percentage'),
        default=Value(0),
        output_field=IntegerField()))

    # Serialize data for charts
    data = {
        'matches': match_numbers,
        'shots': list(shots.values_list('shots_value', flat=True)),
        'goals': list(matches.values_list('team1_total' if team.name == matches.values('team1_name')[0] else 'team2_total', flat=True)),
        'circles': list(circles.values_list('circles_value', flat=True)),
        'possessions': list(possessions.values_list('possession_value', flat=True))
    }

    return JsonResponse(data)

# views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
import joblib
import os
import pandas as pd
def prediction(request):
    return render(request, 'templates/prediction.html')

def predict(request, team_name):
    context = {'team_name': team_name}
    return render(request, 'templates/predict.html', context)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import joblib
import os
import pandas as pd

@csrf_exempt  # For testing; remember to handle CSRF properly in production environments
def predict_result(request, team_name):
    if request.method == 'POST':
        try:
            team_name = team_name.lower() + 'data'
            model_path = os.path.join('models', f'{team_name}_model.pkl')
            model = joblib.load(model_path)

            # Safely parse input values, defaulting to 0 if conversion fails
            def get_float(value, default=0.0):
                try:
                    return float(value) if value else default
                except ValueError:
                    return default

            def get_int(value, default=0):
                try:
                    return int(value) if value else default
                except ValueError:
                    return default

            data = {
                'possession_percentage': get_float(request.POST.get('possession_percentage')),
                'circle_count': get_int(request.POST.get('circle_count')),
                'shots_count': get_int(request.POST.get('shots_count')),
                'field_goal': get_int(request.POST.get('field_goal')),
                'penalty_goal': get_int(request.POST.get('penalty_goal')),
                'penalty_corners': get_int(request.POST.get('penalty_corners')),
                'penalty_strokes': get_int(request.POST.get('penalty_strokes'))
            }

            df = pd.DataFrame([data])
            result = model.predict(df)[0]
            result_text = 'Win' if result == 1 else 'Loss'
            return JsonResponse({'predicted_result': result_text})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

