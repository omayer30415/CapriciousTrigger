import random
from .models import Soldier, Team, General


def enemy_choosing(team_name):
    if (team_name == 'Star') or (team_name == 'Patriot'):
        op_list = ['Jungle Warriors', 'Gangstars']
        op = random.choice(op_list)
    else:
        op = random.choice(
            [t.name for t in Team.objects.exclude(name=team_name)])
    return op


def c(user):
    generals = General.objects.filter(commander=user)
    generals.delete()
    soldiers = Soldier.objects.filter(commander=user)
    soldiers.delete()
    user.team = None
    user.money = 10000
    user.levels = 0
    user.experience = 0
    user.save()


def create_soldiers(team_name, amount):
    soldiers = []
    if team_name == 'Star':
        for s in range(amount):
            team = Team.objects.get(name=team_name)
            soldier = Soldier.objects.create(
                team=team, helmet_image_url='http://clipart-library.com/img1/1198114.jpg')
            soldiers.append(soldier)
        return soldiers
    if team_name == 'Patriot':
        for s in range(amount):
            team = Team.objects.get(name=team_name)
            soldier = Soldier.objects.create(
                team=team, helmet_image_url='http://clipart-library.com/img/1822058.jpg')
            soldiers.append(soldier)
        return soldiers
    if team_name == 'Jungle Warriors':
        for s in range(1, amount):
            team = Team.objects.get(name=team_name)
            soldier = Soldier.objects.create(
                team=team, helmet_image_url='http://clipart-library.com/img/1207060.gif')
            soldiers.append(soldier)
        return soldiers
    if team_name == 'Gangstars':
        for s in range(amount):
            team = Team.objects.get(name=team_name)
            soldier = Soldier.objects.create(
                team=team, helmet_image_url='http://clipart-library.com/data_images/37079.jpg')
            soldiers.append(soldier)
        return soldiers
    else:
        for s in range(amount):
            team = Team.objects.get(name=team_name)
            soldier = Soldier.objects.create(
                team=team, helmet_image_url='http://clipart-library.com/data_images/37079.jpg')
            soldiers.append(soldier)
        return soldiers


def dependent_double_event(percentage):
    y = random.randrange(100)
    if y <= percentage:
        return True
    else:
        return False


def dependant_triple_event(event1, event1_percentage, event2, event2_percentage, event3, event3_percentage):
    y = random.randrange(100)
    if y <= event1_percentage:
        return event1
    elif y <= (event1_percentage+event2_percentage):
        return event2
    elif y <= (event1_percentage+event2_percentage+event3_percentage):
        return event3
    else:
        return False


def auction_intelligence(money_amounts, opponent_amount, price):
    plan = dependant_triple_event("General", 95, "Medium", 3, "Idiot", 1)
    if plan == "General":
        if price >= 400000:
            return 0
        amounts1 = [i for i in money_amounts if opponent_amount +
                    1000 <= i <= opponent_amount+20000]
        amounts2 = [i for i in money_amounts if opponent_amount +
                    20000 <= i <= opponent_amount+40000 or i == 0]
        amounts3 = [i for i in money_amounts if opponent_amount +
                    40000 <= i <= opponent_amount+50000 or i == 0]
        selected_amount = dependant_triple_event(
            random.choice(amounts1), 80, random.choice(amounts2), 15, random.choice(amounts3), 5)
        return selected_amount

    elif plan == "Medium":
        if price >= 1500000:
            return 0
        amounts1 = [i for i in money_amounts if opponent_amount +
                    50000 <= i <= opponent_amount+100000]
        amounts2 = [i for i in money_amounts if opponent_amount+100000 <=
                    i <= opponent_amount+300000 or i == 0]
        amounts3 = [i for i in money_amounts if opponent_amount+300000 <=
                    i <= opponent_amount+500000 or i == 0]
        selected_amount = dependant_triple_event(random.choice(
            amounts3), 80, random.choice(amounts2), 15, random.choice(amounts3), 5)
        return selected_amount

    elif plan == "Idiot":
        if price >= 3000000:
            return 0
        amounts1 = [i for i in money_amounts if opponent_amount +
                    500000 <= i <= opponent_amount+700000]
        amounts2 = [i for i in money_amounts if opponent_amount+700000 <=
                    i <= opponent_amount+800000 or i == 0]
        amounts3 = [i for i in money_amounts if opponent_amount+800000 <=
                    i <= opponent_amount+1000000 or i == 0]
        selected_amount = dependant_triple_event(random.choice(
            amounts3), 80, random.choice(amounts2), 15, random.choice(amounts3), 5)
        return selected_amount

    else:
        money_amounts = [i for i in money_amounts if (
            opponent_amount+1000000) < i and i == 0]
        event = random.choice(money_amounts)
        return event


commanders = [

    {"name": "Russell", "cost": 0},
    {"name": "Rony", "cost": 0},
    {"name": "Zaman", "cost": 0},
    {"name": "A.Salam", "cost": 0},
    {"name": "Abdullah", "cost": 0},
    {"name": "Naeem", "cost": 0},
    {"name": "Kader", "cost": 0},
    {"name": "Shahid", "cost": 0},
    {"name": "Habib", "cost": 0},
    {"name": "Faisal", "cost": 0},
    {"name": "Sayed", "cost": 0},
    {"name": "Mehedi", "cost": 0},
    {"name": "Bashir", "cost": 0},
    {"name": "Toufiq", "cost": 0},
    {"name": "Mahmud", "cost": 0},
    {"name": "Hasan", "cost": 0}
]

user1 = {
    "commanders": [],
    "money": 10000000,
    "bid": 0,
    "withdraw": False
}

user2 = {
    "commanders": [],
    "money": 10000000,
    "bid": 0,
    "withdraw": False
}


def commander_auction(user1, user2, commanders):
    for commander in commanders:
        print(f"Now {commander['name']}'s auction has started.")
        user2["withdraw"] = False
        user1['withdraw'] = False
        while not user2["withdraw"] and not user1['withdraw']:
            user1['bid'] = int(input("Place bid: "))

            if user1['bid'] == 0:
                user1['withdraw'] = True
                user2['commanders'].append(commander)
                user2['money'] = user2['money'] - commander['cost']
                print(
                    f"{commander['name']} is added to user2's commanders list.")
                user2['bid'] = 0
                break
            elif user1['bid'] > user1['money']:
                print(f"You do not have {user1['bid']} amount of money")
            elif user1['bid'] > commander['cost']:
                commander['cost'] = user1['bid']
            else:
                print("bid must be bigger than cost")

            while user2['bid'] < commander['cost']:
                money_amounts = [i for i in range(0, user2["money"], 1000)]
                user2['bid'] = auction_intelligence(
                    money_amounts=money_amounts, opponent_amount=user1['bid'], price=commander['cost'])

                if user2['bid'] == 0:
                    user2['withdraw'] = True
                    user1['commanders'].append(commander)
                    print(
                        f"{commander['name']} is added to user1's commander list")
                    user1['money'] = user1['money'] - commander['cost']
                    user1['bid'] = 0
                    break
                elif user2['bid'] > commander['cost']:
                    commander['cost'] = user2['bid']
                    print(f"Now the cost is {commander['cost']}")
                else:
                    pass
