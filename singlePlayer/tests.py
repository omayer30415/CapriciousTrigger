from django.test import TestCase, Client
from .models import *
from .source import create_soldiers
import random
from django.core.exceptions import ObjectDoesNotExist
# Create your tests here.


class GameTestCase(TestCase):

    def setUp(self):
        t1 = Team.objects.create(
            name='Star', image_url='http://www.clipart.com/tree.png')
        t2 = Team.objects.create(
            name='Patriot', image_url='http://www.clipart.com/tree.png')
        t3 = Team.objects.create(
            name='Jungle Warriors', image_url='http://www.clipart.com/tree.png')
        t4 = Team.objects.create(
            name='Gangstars', image_url='http://www.clipart.com/tree.png')
        User.objects.create(
            username='omayer', email='omayer30415@gmail.com', password='8o56', team=t1)
        General.objects.create(
            name='Hashim', team=t1, cap_image_url='http://www.clipart.com/tree.png')
        General.objects.create(
            name='Hisham', team=t2, cap_image_url='http://www.clipart.com/tree.png')
        General.objects.create(
            name='Hasan', team=t3, cap_image_url='http://www.clipart.com/tree.png')
        General.objects.create(
            name='Habib', team=t4, cap_image_url='http://www.clipart.com/tree.png')

    def test_game(self):
        c = Client()
        response = c.get("/game")
        self.assertEqual(response.status_code, 302)

    def test_creating_duplicate_generals(self):
        """
        Test for creating duplicate Generals for Users
        """
        u1 = User.objects.get(username='omayer')
        team = u1.team
        generals = team.generals.all()
        for general in generals:
            user_general = General.objects.create(
                name=general.name, cap_image_url=general.cap_image_url, commander=u1)
            user_general.save()
        u_g = General.objects.get(commander=u1)
        t_g = General.objects.get(team=team)
        general_count = General.objects.all().count()
        self.assertEqual(u_g.pk, 5)
        self.assertNotEqual(u_g.team, u1.team)
        self.assertEqual(general_count, 5)
        self.assertAlmostEqual(u_g.name, 'Hashim')
        self.assertEqual(t_g.name, 'Hashim')
        self.assertEqual(t_g.pk, 1)

    def test_creating_soldiers(self):
        """
        Test for creating neccessary soldiers as expected  
        """
        user = User.objects.get(username='omayer')
        team = user.team
        soldiers = create_soldiers(
            team_name=team.name, amount=20)
        for soldier in soldiers:
            soldier.commander = user
            soldier.save()
        user_soldiers = Soldier.objects.filter(commander=user)
        self.assertEqual(user_soldiers.count(), 20)

    def test_opponent(self):
        """
        Test for creating opponent team
        """
        user = User.objects.get(username='omayer')
        team = user.team
        if team.name == 'Star' or 'Patriot':
            op_list = ['Jungle Warriors', 'Gangstars']
            op = random.choice(op_list)
        else:
            op = random.choice(
                [t.name for t in Team.objects.exclude(name=team.name)])
        op_team = Team.objects.get(name=op)
        user_generals = General.objects.filter(commander=user)
        user_soldiers = Soldier.objects.filter(commander=user)
        try:
            opponent = Opponent.objects.get(opposed_to=user)
        except Opponent.DoesNotExist:
            opponent = Opponent.objects.create(team=op_team, opposed_to=user)
        op_generals = opponent.generals.all()
        op_soldiers = opponent.soldiers.all()
        if op_generals.count() == 0:
            generals = General.objects.filter(team=opponent.team)
            for general in generals:
                op_general = General.objects.create(
                    name=general.name, as_opponent=opponent, cap_image_url=general.cap_image_url)
                op_general.save()
        opponent_soldiers = opponent.soldiers.all()
        if opponent_soldiers.count() == 0:
            opponent_soldiers = create_soldiers(opponent.team.name, 15)
        op_g = General.objects.get(as_opponent=opponent)
        op_t = opponent.team
        op_t_g = General.objects.get(team=op_t)
        self.assertEqual(opponent.pk, 1)
        self.assertNotEqual(op_g, op_t_g)

    def test_create_army(self):
        c = Client()
        response = c.get('/choose')
        self.assertEqual(response.status_code, 302)
