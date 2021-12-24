from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import IntegrityError
from django import forms
from .models import *
from .serializers import *
from django.http import HttpResponse
from django.http import JsonResponse, HttpResponse,  Http404, HttpRequest
from rest_framework.views import APIView
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view,  permission_classes
from rest_framework import permissions
from .source import create_soldiers, dependent_double_event
from django.core.exceptions import ObjectDoesNotExist
import json
import random
from itertools import chain


class UserForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20)
    email = forms.EmailField(label='E-mail')
    password = forms.CharField(widget=forms.PasswordInput())
    confirmation = forms.CharField(widget=forms.PasswordInput())


def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data['email']
            password = form.cleaned_data["password"]
            confirmation = form.cleaned_data["confirmation"]
            if password != confirmation:
                messages.error(request,  "Passwords must match.")
                return render(request, "singlePlayer/register.html")
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
            except IntegrityError:
                messages.error(request, 'Username already taken.')
                return render(request, "singlePlayer/register.html", {
                    'form': UserForm()
                })
            login(request, user)
            return redirect('index')
    else:
        form = UserForm()
        return render(request, "singlePlayer/register.html", {
            'form': form
        })


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, message="Error occurs")
            return render(request, 'singlePlayer/login.html')
    else:
        return render(request, 'singlePlayer/login.html')


def logout_user(request):
    logout(request)
    return redirect('index')


def index(request):
    return render(request, 'singlePlayer/index.html')


@login_required
def choose(request):
    user = User.objects.get(username=request.user)
    generals = General.objects.filter(commander=user)
    generals.delete()
    soldiers = Soldier.objects.filter(commander=user)
    soldiers.delete()
    user.team = None
    user.money = 10000
    user.levels = 0
    user.experience = 0
    user.save()
    teams = Team.objects.all()
    generals = General.objects.all()
    return render(request, 'singlePlayer/choose.html', {
        "teams": teams,
        "generals": generals
    })


@csrf_protect
@login_required
def new_choose(request, team_id):
    user = User.objects.get(username=request.user)
    user.team = Team.objects.get(pk=team_id)
    user.save()
    generals = General.objects.filter(team=team_id)
    for general in generals:
        user_general = General.objects.create(
            name=general.name, cap_image_url=general.cap_image_url, commander=user)
        user_general.save()
    soldiers = create_soldiers(team_name=user.team.name, amount=20)
    for soldier in soldiers:
        soldier.commander = user
        soldier.save()
    user_soldiers = Soldier.objects.filter(commander=user)
    return redirect('cabinet')


@login_required
def cabinet(request):
    user = User.objects.get(username=request.user)
    user_generals = General.objects.filter(commander=user)
    user_soldiers = Soldier.objects.filter(commander=user)
    soldiers = []
    for soldier in user_soldiers:
        if soldier.killed_units >= 5:
            soldiers.append(soldier)
    if user_generals.count() == 0:
        return redirect('choose')
    else:
        try:
            opponent = Opponent.objects.get(opposed_to=user)
            return render(request, 'game/cabinet.html', {
                "generals": user_generals,
                "soldiers": soldiers,
                "opponent": opponent
            })
        except Opponent.DoesNotExist:
            return render(request, 'game/cabinet.html', {
                "generals": user_generals,
                "soldiers": soldiers
            })


@csrf_protect
@login_required
def promote(request, soldier_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('soldier_name', '')
        cap_image_url = data.get('cap_image_url', '')
        user = User.objects.get(username=data.get('user', ''))
        killed_units = data.get('killed_units', '')
        general = General(name=name,
                          commander=user, cap_image_url=cap_image_url, killed_units=killed_units)
        general.save()
        soldier = Soldier.objects.get(id=soldier_id, commander=user)
        soldier.delete()
        serializer = GeneralSerializer(general)
        return serializer.data
    else:
        return JsonResponse({'message': 'POST request needed'})


@login_required
def game(request):
    user = User.objects.get(username=request.user)
    team = user.team
    user_generals = General.objects.filter(commander=user)
    user_soldiers = Soldier.objects.filter(commander=user)
    try:
        opponent = Opponent.objects.get(opposed_to=user)
    except Opponent.DoesNotExist:
        if team.name == 'Star' or 'Patriot':
            op_list = ['Jungle Warriors', 'Gangstars']
            op = random.choice(op_list)
        else:
            op = random.choice(
                [t.name for t in Team.objects.exclude(name=team.name)])
        op_team = Team.objects.get(name=op)
        opponent = Opponent.objects.create(team=op_team, opposed_to=user)
    op_generals = opponent.generals.all()
    if op_generals.count() == 0:
        generals = General.objects.filter(team=opponent.team)
        for general in generals:
            op_general = General.objects.create(
                name=general.name, as_opponent=opponent, cap_image_url=general.cap_image_url,)
            op_general.save()
    opponent_soldiers = opponent.soldiers.all()
    if opponent_soldiers.count() == 0:
        opponent_soldiers = create_soldiers(opponent.team.name, 15)
        for soldier in opponent_soldiers:
            soldier.as_opponent = opponent
            soldier.save()
    op_generals = General.objects.filter(as_opponent=opponent)
    op_soldiers = Soldier.objects.filter(as_opponent=opponent)
    try:
        score = Score.objects.get(user=user, opponent=opponent)
    except Score.DoesNotExist:
        score = Score.objects.create(user=user, opponent=opponent)
    return render(request, 'game/game.html', {
        'op_army': opponent,
        'op_generals': op_generals,
        'op_soldiers': op_soldiers,
        'user_generals': user_generals,
        'user_soldiers': user_soldiers,
        'count': range(27),
        'user_score': score.user_score,
        'op_score': score.opponent_score,

    })


@login_required
def con(request):
    user = User.objects.get(username=request.user)
    opponent = Opponent.objects.get(opposed_to=user)
    score = Score.objects.get(user=user, opponent=opponent)
    return render(request, 'game/game.html', {
        'op_army': opponent,
        'op_generals': opponent.generals.all(),
        'op_soldiers': opponent.soldiers.all(),
        'user_generals': user.generals.all(),
        'user_soldiers': user.soldiers.all(),
        'count': range(27),
        'user_score': score.user_score,
        'op_score': score.opponent_score,

    })


def fav(request):
    return HttpResponse('Favicon.ico is not added')


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@permission_classes((permissions.IsAdminUser,))
class UserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ('username',)


@permission_classes((permissions.IsAdminUser,))
class GeneralView(generics.ListAPIView):
    queryset = General.objects.all()
    serializer_class = GeneralSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ('team', 'commander')


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((permissions.IsAuthenticated,))
def general_detail(request, pk):
    try:
        general = General.objects.get(pk=pk, commander=request.user)
    except General.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GeneralSerializer(general)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = GeneralSerializer(general, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        general.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((permissions.IsAuthenticated,))
def soldier_detail(request, pk):
    try:
        soldier = Soldier.objects.get(pk=pk, commander=request.user)
    except Soldier.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SoldierSerializer(soldier)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SoldierSerializer(soldier, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        soldier.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_protect
@login_required
def general_vs_soldier(request, general_id, soldier_id):
    if request.method == 'PUT':
        score = Score.objects.get(user=request.user)
        general = General.objects.get(pk=general_id)
        soldier = Soldier.objects.get(pk=soldier_id)
        percentage = general.attack - soldier.defense
        success = dependent_double_event(percentage)
        if success:
            soldier.life -= 1
            soldier.save()
            if soldier.life == 0:
                general.on_battle_k_u += 1
                general.save()
                score.user_score += 20
                score.save()
                return JsonResponse({
                    'message': 'Killed',
                    'score_i': 'user',
                    'score': score.user_score
                })
            else:
                return JsonResponse({'message': 'Success'})
        else:
            return JsonResponse({'message': 'Miss'})
    else:
        return JsonResponse({"message": "'PUT' method required"})


@csrf_protect
@login_required
def general_vs_general(request, general_id, g_id):
    if request.method == 'PUT':
        score = Score.objects.get(user=request.user)
        general1 = General.objects.get(pk=general_id)
        general2 = General.objects.get(pk=g_id)
        percentage = general1.attack - general2.defense
        success = dependent_double_event(percentage)
        if success:
            general2.life -= 1
            general2.save()
            if general2.life == 0:
                general1.on_battle_k_u += 1
                general1.save()
                score.user_score += 50
                score.save()
                return JsonResponse({
                    'message': 'Killed',
                    'score_i': 'user',
                    'score': score.user_score
                })
            else:
                message = Message("Success")
        else:
            message = Message("Miss")
        serializer = MessageSerializer(message)
        return JsonResponse(serializer.data)
    else:
        return JsonResponse({"message": "'PUT' method required"})


@csrf_protect
@login_required
def soldier_vs_soldier(request, soldier_id, s_id):
    if request.method == 'PUT':
        score = Score.objects.get(user=request.user)
        soldier1 = Soldier.objects.get(pk=soldier_id)
        soldier2 = Soldier.objects.get(pk=s_id)
        percentage = soldier1.attack - soldier2.defense
        success = dependent_double_event(percentage)
        if success:
            soldier2.life -= 1
            soldier2.save()
            if soldier2.life == 0:
                soldier1.on_battle_k_u += 1
                soldier1.save()
                score.user_score += 20
                score.save()
                return JsonResponse({
                    'message': 'Killed',
                    'score_i': 'user',
                    'score': score.user_score
                })
            else:
                return JsonResponse({'message': 'Success'})
        else:
            return JsonResponse({'message': 'Miss'})
    else:
        return JsonResponse({"message": "'PUT' method required"})


@csrf_protect
@login_required
def soldier_vs_general(request, soldier_id, general_id):
    if request.method == 'PUT':
        score = Score.objects.get(user=request.user)
        general = General.objects.get(pk=general_id)
        soldier = Soldier.objects.get(pk=soldier_id)
        percentage = soldier.attack - general.defense
        success = dependent_double_event(percentage)
        if success:
            general.life -= 1
            general.save()
            if general.life == 0:
                soldier.on_battle_k_u += 1
                soldier.save()
                score.user_score += 50
                score.save()
                return JsonResponse({
                    'message': 'Killed',
                    'score_i': 'user',
                    'score': score.user_score
                })
            else:
                return JsonResponse({'message': 'Success'})
        else:
            return JsonResponse({'message': 'Miss'})
    else:
        return JsonResponse({"message": "'PUT' method required"})


@csrf_protect
@login_required
def random_attack(request):
    if request.method == 'PUT':
        score = Score.objects.get(user=request.user)
        user = User.objects.get(username=request.user)
        opponent = Opponent.objects.get(opposed_to=user)
        user_generals = user.generals.all()
        user_soldiers = user.soldiers.all()
        op_generals = opponent.generals.all()
        op_soldiers = opponent.soldiers.all()
        uss = list(chain(user_generals, user_soldiers))
        ops = list(chain(op_generals, op_soldiers))
        attacker = random.choice(ops)
        defender = random.choice(uss)
        percentage = attacker.attack - defender.defense
        success = dependent_double_event(percentage)
        if success:
            defender.life -= 1
            defender.save()
            if defender.life == 0:
                attacker.on_battle_k_u += 1
                attacker.save()
                if defender in user.generals.all():
                    score.opponent_score += 50
                    score.save()
                else:
                    score.opponent_score += 20
                    score.save()
                return JsonResponse({
                    'attacker_id': attacker.id,
                    'defender_id': defender.id,
                    'message': 'Killed',
                    'score_i': 'opponent',
                    'score': score.opponent_score
                })
            else:
                return JsonResponse({
                    'attacker_id': attacker.id,
                    'defender_id': defender.id,
                    'message': 'Success'
                })
        else:
            return JsonResponse({
                'attacker_id': attacker.id,
                'defender_id': defender.id,
                'message': 'Miss'
            })


def restart(request):
    user = User.objects.get(username=request.user)
    op = Opponent.objects.get(opposed_to=user)
    for u_general in user.generals.all():
        u_general.life = u_general.max_life
        u_general.on_battle_k_u = 0
        u_general.save()
    for u_soldier in user.soldiers.all():
        u_soldier.life = u_soldier.max_life
        u_soldier.on_battle_k_u = 0
        u_soldier.save()
    for o_general in op.generals.all():
        o_general.life = o_general.max_life
        o_general.on_battle_k_u = 0
        o_general.save()
    for o_soldier in op.soldiers.all():
        o_soldier.life = u_soldier.max_life
        o_soldier.on_battle_k_u = 0
        o_soldier.save()
    score = Score.objects.get(user=user, opponent=op)
    score.user_score = 0
    score.opponent_score = 0
    score.save()
    return redirect('game')


@login_required
def win_or_lose(request):
    user = User.objects.get(username=request.user)
    op = Opponent.objects.get(opposed_to=user)
    u_generals = len(General.objects.filter(commander=user, life=0))
    total_u_generals = len(General.objects.filter(commander=user))
    u_soldiers = len(Soldier.objects.filter(commander=user, life=0))
    total_u_soldiers = len(Soldier.objects.filter(commander=user))
    total_soldiers = len(Soldier.objects.filter(commander=user))
    o_generals = len(General.objects.filter(as_opponent=op, life=0))
    total_o_generals = len(General.objects.filter(as_opponent=op))
    o_soldiers = len(Soldier.objects.filter(as_opponent=op, life=0))
    total_o_soldiers = len(Soldier.objects.filter(as_opponent=op))
    if (o_generals >= (0.80 * total_o_generals)) or (o_soldiers >= (0.80 * total_o_soldiers)):
        print(f"o_generals:{o_generals},o_soldiers{o_soldiers}")
        return JsonResponse({'message': "YOU WIN"})
    elif (u_generals >= (0.80 * total_u_generals)) or (u_soldiers >= (0.80 * total_u_soldiers)):
        return JsonResponse({'message': 'YOU LOSE'})
    else:
        return JsonResponse({'message': 'Continue'})


def progress(request):
    user = User.objects.get(username=request.user)
    op = Opponent.objects.get(opposed_to=user)
    for u_general in user.generals.all():
        u_general.killed_units = u_general.on_battle_k_u
        u_general.save()
        if u_general.life == 0:
            u_general.delete()
    for u_soldier in user.soldiers.all():
        u_soldier.killed_units = u_soldier.on_battle_k_u
        u_soldier.save()
        if u_soldier.life == 0:
            u_soldier.delete()
    score = Score.objects.get(user=user, opponent=op)
    user.experience = (score.user_score * 10) + score.opponent_score
    user.levels = user.experience // 1000
    user.money += user.experience
    user.save()
    score.delete()
    op.delete()
    return redirect('cabinet')


def shop(request):
    products = Product.objects.all()
    return render(request, 'game/shop.html', {
        "products": products,
    })


@login_required
def cap_buy(request, cap_id):
    user = User.objects.get(username=request.user)
    product = Product.objects.get(pk=cap_id)
    for general in user.generals.all():
        general.cap_image_url = product.image_url
        general.defense += product.power
        general.save()
        user.money -= product.price
        user.save()
        print('generals')
    return redirect('cabinet')


@login_required
def helmet_buy(request, helmet_id):
    user = User.objects.get(username=request.user)
    product = Product.objects.get(pk=helmet_id)
    for soldier in user.soldiers.all():
        soldier.helmet_image_url = product.image_url
        soldier.defense += product.power
        soldier.save()
        user.money -= product.price
        user.save()
        print('soldiers')
    return redirect('cabinet')


def show_credits(request):
    return render(request, 'singlePlayer/credits.html')
