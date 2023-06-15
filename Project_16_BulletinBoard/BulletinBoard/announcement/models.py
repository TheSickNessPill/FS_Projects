from django.db import models
from accounts.models import *
from django.urls import reverse
from django.contrib.auth.models import User


class AnnouncementCategory(models.Model):
    TK = 'TK'
    HL = 'HL'
    DD = 'DD'
    TD = 'TD'
    GM = 'GM'
    QG = 'QG'
    SM = 'SM'
    TN = 'TN'
    PM = 'PM'
    SM = 'SM'

    CATEGORYS = [
        (TK, 'Tank'),
        (HL, 'Heal'),
        (DD, 'Damage Dealer'),
        (TD, 'Treader'),
        (GM, 'GuuldMaster'),
        (QG, 'Quest Giver'),
        (SM, 'Smith'),
        (TN, 'Tanner'),
        (PM, 'Poison Master'),
        (SM, 'Spell Master'),
    ]

    category = models.CharField(max_length=100, choices=CATEGORYS, blank=False, null=True, editable=True)

    def __str__(self):
        return self.category


class Announcement(models.Model):
    title = models.CharField(max_length=150, blank=False, null=True, editable=True)
    text = models.TextField(blank=False, null=True, editable=True)
    attachment = models.ImageField(upload_to="images/", blank=True, null=True)
    category = models.ForeignKey(AnnouncementCategory, on_delete=models.CASCADE, related_name='anouncement')
    by_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title[:30]} - {self.category} - {self.by_user} - {self.text[:30]}"

    def get_absolute_url(self):
        return reverse('announsement', args=[str(self.id)])


class AnnouncementResponse(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, blank=False, null=False)
    text = models.TextField(blank=False, null=True, editable=True)
    create_time = models.DateTimeField(auto_now_add=True, blank=False, null=True)
    by_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True, related_name='responce')
    is_accepted = models.BooleanField(blank=True, null=True, default=False)

    def __str__(self):
        return f"{self.announcement.title[:30]} - {self.text[:30]}"

    def get_absolute_url(self):
        return reverse('responsetome', args=[str(self.id)])


class AnnouncementSubscription(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to=AnnouncementCategory,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
