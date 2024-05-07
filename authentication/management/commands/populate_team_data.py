# management/commands/populate_team_data.py

from django.core.management.base import BaseCommand
from authentication.models import (PossessionData, Goal, Circle, Shots, PC, PS,
                                   WhiteWarriorszData, BlueBlazerzData, GreenGriffinzData, 
                                   RedRufiianzData, VioletWhalezData, YellowYakzData)

class Command(BaseCommand):
    help = 'Populates team-specific game data tables from match data'

    def handle(self, *args, **options):
        self.populate_team_data()

    def populate_team_data(self):
        model_map = {
            'White Warriorz': WhiteWarriorszData,
            'Blue Blazerz': BlueBlazerzData,
            'Green Griffinz': GreenGriffinzData,
            'Red Ruffianz': RedRufiianzData,
            'Violet Whalez': VioletWhalezData,
            'Yellow Yakz': YellowYakzData
        }

        for goal in Goal.objects.all():
            teams = [(goal.team1_name, 'team1'), (goal.team2_name, 'team2')]
            for team_name, team_pos in teams:
                if team_name in model_map:
                    team_model = model_map[team_name]
                    possession = PossessionData.objects.get(match_number=goal.match_number)
                    circle = Circle.objects.get(match_number=goal.match_number)
                    shots = Shots.objects.get(match_number=goal.match_number)
                    pc = PC.objects.get(match_number=goal.match_number)
                    ps = PS.objects.get(match_number=goal.match_number)
                    result = getattr(goal, f"{team_pos}_result")

                    team_data = team_model(
                        match_number=goal.match_number,
                        possession_percentage=getattr(possession, f'{team_pos}_possession_percentage'),
                        circle_count=getattr(circle, f'{team_pos}_circle'),
                        shots_count=getattr(shots, f'{team_pos}_shots'),
                        field_goal=getattr(goal, f'{team_pos}_FG'),
                        penalty_goal=getattr(goal, f'{team_pos}_PG'),
                        penalty_corners=getattr(pc, f'{team_pos}_pc'),
                        penalty_strokes=getattr(ps, f'{team_pos}_ps'),
                        result=result
                    )
                    team_data.save()
                    self.stdout.write(self.style.SUCCESS(f'Data populated for {team_name} in match {goal.match_number}'))
