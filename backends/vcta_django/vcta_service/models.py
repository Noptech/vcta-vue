from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


class Hero(models.Model):
    """
    Represents a Hero.
    """
    name = models.TextField()

    def __str__(self):
        return self.name


class User(AbstractUser):
    """
    Extends built-in user model.
    """
    full_name = models.CharField(max_length=30)
    team = models.ForeignKey('Team', null=True, blank=True, related_name="members", on_delete=models.SET_NULL)

    def __str__(self):
        return self.username


@receiver(pre_save, sender=User, dispatch_uid="Ensure captains can not leave their team")
def captain_must_stay_in_team(sender, instance, **kwargs):
    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        pass # Object is new
    else:
        if old_instance.team is None:
            # user has been added to a team
            return
        else:
            # user removed from a team
            if old_instance.team.captain == old_instance and instance.team != old_instance.team:
                raise ValidationError("Team captain {0} is not allowed to leave team {1}"
                                      .format(instance, old_instance.team))


class Trip(models.Model):
    """
    Represents a Trip.
    """
    user = models.ForeignKey(User, related_name="trips")
    date = models.DateField()
    distance = models.DecimalField(decimal_places=2, max_digits=5,
                                   validators=[MinValueValidator(0.01), MaxValueValidator(300)])
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + " " + str(self.date) + " " + str(self.distance)


class Team(models.Model):
    """
    Represents a Team.
    """
    name = models.CharField(max_length=30)
    captain = models.ForeignKey(User, null=False, related_name="captain")

    def __str__(self):
        return self.name


@receiver(post_save, sender=Team, dispatch_uid="Ensure captains are members of their team")
def captain_must_be_member(sender, instance, **kwargs):
    captain = instance.captain
    if captain.team != instance:
        captain.team = instance
        captain.save()


class TeamJoinRequest(models.Model):
    """
    Represents a request by a user to join a team
    """
    team = models.ForeignKey(Team, related_name="membership_requests")
    sender = models.ForeignKey(User, related_name="team_requests")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(blank=False, null=False, default="PENDING", max_length=10)


def validate_only_one_instance(obj):
    model = obj.__class__
    if (model.objects.count() > 0 and
                obj.id != model.objects.get().id):
        raise ValidationError("Can only create 1 %s instance" % model.__name__)


class Config(models.Model):
    """
    Store settings (admin use). Will contain only a single row.
    It would be more elegant to use constance or similar package for storing editable settings in django -
    but this is the simplest way to have the settings available through Django-rest-framework.
    """
    team_management_enabled = models.BooleanField(default=True, null=False,
                                                  help_text="Allow team management - creating teams, sending "
                                                            "invitations, accepting invitations.")
    trip_management_enabled = models.BooleanField(default=True, null=False,
                                                  help_text="Allow adding/deleting of trips")
    flash_message = models.TextField(default=None, blank=True, null=True,
                                     help_text="Message to show at the top of every page")
    welcome_message = models.TextField(default=None, blank=True, null=True,
                                       help_text="Additional welcome message on login page")

    def clean(self):
        """
        Don't allow saving more than 1 config row
        """
        validate_only_one_instance(self)
