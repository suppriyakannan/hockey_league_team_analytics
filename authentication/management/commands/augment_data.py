import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from authentication.models import WhiteWarriorszData, BlueBlazerzData, GreenGriffinzData, RedRufiianzData, VioletWhalezData, YellowYakzData

class Command(BaseCommand):
    help = 'Augments existing game data by creating variations'

    def handle(self, *args, **options):
        # List of all model classes
        team_data_models = [
            WhiteWarriorszData, BlueBlazerzData, GreenGriffinzData,
            RedRufiianzData, VioletWhalezData, YellowYakzData
        ]

        for model in team_data_models:
            self.stdout.write(f"Processing {model.__name__}...")
            for instance in model.objects.all():
                for _ in range(5):  # Create 5 new entries for each existing entry
                    new_instance = model(
                        match_number=instance.match_number,
                        possession_percentage=max(
                            Decimal('10.00'),
                            min(
                                Decimal('100.00'),
                                instance.possession_percentage + Decimal(str(random.uniform(-5.0, 5.0)))
                            )
                        ),
                        circle_count=max(0, min(10, instance.circle_count + random.randint(-2, 2))),
                        shots_count=max(0, min(10, instance.shots_count + random.randint(-2, 2))),
                        field_goal=max(0, min(10, instance.field_goal + random.randint(-1, 1))),
                        penalty_goal=max(0, min(10, instance.penalty_goal + random.randint(-1, 1))),
                        penalty_corners=max(0, min(5, instance.penalty_corners + random.randint(-1, 1))),
                        penalty_strokes=max(0, min(5, instance.penalty_strokes + random.randint(-1, 1))),
                        result=random.randint(0, 1)  # Assuming binary outcome
                    )
                    new_instance.save()
                    self.stdout.write(f"Created augmented data for {model.__name__} with ID {new_instance.id}")

        self.stdout.write(self.style.SUCCESS('Data augmentation complete.'))
