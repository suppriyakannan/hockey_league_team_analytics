
# Create your models here.
# models.py (authentication app)

from django.db import models


from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Add any additional fields if needed
    pass

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

# Define related names for user_permissions and groups
CustomUser.groups.field.related_name = 'custom_user_groups'
CustomUser.user_permissions.field.related_name = 'custom_user_permissions'

from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='team_logos/', blank=True, null=True)

    def __str__(self):
        return self.name

from django.db import models

class PossessionData(models.Model):
    match_number = models.IntegerField()
    team1_name = models.CharField(max_length=100)
    team2_name = models.CharField(max_length=100)
    team1_possession_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    team2_possession_percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Match {self.match_number}: {self.team1_name} vs {self.team2_name}"

# models.py
from django.db import models

# models.py
from django.db import models

class Goal(models.Model):
    match_number = models.IntegerField(unique=True)
    team1_name = models.CharField(max_length=100)
    team2_name = models.CharField(max_length=100)
    team1_FG = models.IntegerField(default=0)
    team1_PG = models.IntegerField(default=0)
    team2_FG = models.IntegerField(default=0)
    team2_PG = models.IntegerField(default=0)
    team1_total = models.IntegerField(default=0)
    team2_total = models.IntegerField(default=0)
    team1_result = models.IntegerField(default=0)  # New field
    team2_result = models.IntegerField(default=0)  # New field

    def save(self, *args, **kwargs):
        self.team1_total = self.team1_FG + self.team1_PG
        self.team2_total = self.team2_FG + self.team2_PG
        # Calculate results based on totals
        if self.team1_total > self.team2_total:
            self.team1_result = 1
            self.team2_result = 0
        elif self.team1_total < self.team2_total:
            self.team1_result = 0
            self.team2_result = 1
        else:  # they are equal
            self.team1_result = 1
            self.team2_result = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Match {self.match_number}: {self.team1_name} vs {self.team2_name}"


class Circle(models.Model):
    match_number = models.IntegerField(unique=True)
    team1_name = models.CharField(max_length=100)
    team2_name = models.CharField(max_length=100)
    team1_circle = models.IntegerField(default=0)
    team2_circle = models.IntegerField(default=0)

    def __str__(self):
        return f"Match {self.match_number}: {self.team1_name} vs {self.team2_name}"

class Shots(models.Model):
    match_number = models.IntegerField(unique=True)
    team1_name = models.CharField(max_length=100)
    team2_name = models.CharField(max_length=100)
    team1_shots = models.IntegerField(default=0)
    team2_shots = models.IntegerField(default=0)

    def __str__(self):
        return f"Match {self.match_number}: {self.team1_name} vs {self.team2_name}"

class Card(models.Model):
    match_number = models.IntegerField(unique=True)
    team1_name = models.CharField(max_length=100)
    team2_name = models.CharField(max_length=100)
    team1_gy = models.IntegerField(default=0)
    team1_r = models.IntegerField(default=0)
    team2_gy = models.IntegerField(default=0)
    team2_r = models.IntegerField(default=0)
    team1_total = models.IntegerField(default=0)
    team2_total = models.IntegerField(default=0)

    def __str__(self):
        return f"Match {self.match_number}: {self.team1_name} vs {self.team2_name}"

    def save(self, *args, **kwargs):
        self.team1_total = self.team1_gy + self.team1_r
        self.team2_total = self.team2_gy + self.team2_r
        super().save(*args, **kwargs)
# models.py


class PC(models.Model):
    match_number = models.IntegerField(unique=True)
    team1_name = models.CharField(max_length=100)
    team2_name = models.CharField(max_length=100)
    team1_pc = models.IntegerField(default=0)
    team2_pc = models.IntegerField(default=0)

    def __str__(self):
        return f"Match {self.match_number}: {self.team1_name} vs {self.team2_name}"

class PS(models.Model):
    match_number = models.IntegerField(unique=True)
    team1_name = models.CharField(max_length=100)
    team2_name = models.CharField(max_length=100)
    team1_ps = models.IntegerField(default=0)
    team2_ps = models.IntegerField(default=0)

    def __str__(self):
        return f"Match {self.match_number}: {self.team1_name} vs {self.team2_name}"

from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=100)
    team = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Injury(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    injury_type = models.CharField(max_length=100)
    injury_details = models.TextField()
    body_part = models.CharField(max_length=100)
    status = models.CharField(max_length=100)  # e.g., active, recovering, cleared
    date_reported = models.DateField()

    def __str__(self):
        return f"{self.injury_type} - {self.player.name}"

class Treatment(models.Model):
    injury = models.ForeignKey(Injury, on_delete=models.CASCADE)
    treatment_type = models.CharField(max_length=100)
    treatment_date = models.DateField()
    notes = models.TextField()

    def __str__(self):
        return self.treatment_type




# models.py continued

class TeamGameData(models.Model):
    match_number = models.IntegerField()
    possession_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    circle_count = models.IntegerField()
    shots_count = models.IntegerField()
    field_goal = models.IntegerField()
    penalty_goal = models.IntegerField()
    penalty_corners = models.IntegerField()
    penalty_strokes = models.IntegerField()
    result = models.IntegerField(blank=True, null=True)  # Store as integer

    class Meta:
        abstract = True

class WhiteWarriorszData(TeamGameData):
    pass

class BlueBlazerzData(TeamGameData):
    pass

class GreenGriffinzData(TeamGameData):
    pass

class RedRufiianzData(TeamGameData):
    pass

class VioletWhalezData(TeamGameData):
    pass

class YellowYakzData(TeamGameData):
    pass
