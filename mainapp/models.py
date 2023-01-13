from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime,date
import enum


PLAYER_ROLE = (
    ("Bowler","Bowler"),
    ("Batsman","Batsman"),
    ("All Rounder","All Rounder"),

)

PLAYER_STATUS = (
    ("Sold","Sold"),
    ("Not Sold","Not Sold"),

)


class Batch(models.Model):
    name = models.CharField(max_length=50)
    session = models.CharField(max_length=50)
    batchNumber = models.IntegerField()

    def total_player(self):
        return Player.objects.filter(batch=self).count

    def __str__(self):
        return "CSE-"+ str(self.batchNumber)+" "+ self.name


class Tournament(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField()

    def __str__(self):
        return self.name + " " + str(self.year)


class Team(models.Model):
    name = models.CharField(max_length=50)
    tournament = models.ForeignKey(Tournament,on_delete=models.DO_NOTHING,null=True,blank=True)

    def total_player(self):
        return Player.objects.filter(team=self).count

    def players(self):
        return Player.objects.filter(team=self)

    def committee_members(self):
        return Player.objects.filter(team=self)

    def __str__(self):
        return self.name + ' - ' + str(self.tournament)


class TeamCommitteeMember(models.Model):
    name = models.CharField(max_length=50)
    batch = models.ForeignKey(Batch, on_delete= models.DO_NOTHING,null=True,blank=True)
    classId = models.IntegerField()
    role = models.CharField(max_length=50)
    bio = models.CharField(max_length=500,null=True,blank=True)
    team = models.ForeignKey(Team,on_delete=models.DO_NOTHING,null=True,blank=True)

    def __str__(self):
        return self.name + ' - ' + str(self.role) + ' - ' + str(self.team)


class Player(models.Model):
    name = models.CharField(max_length=50)
    batch = models.ForeignKey(Batch, on_delete= models.DO_NOTHING,null=True,blank=True)
    classId = models.IntegerField()
    role = models.CharField(max_length=50,choices = PLAYER_ROLE,default="Batsman")
    status = models.CharField(max_length=50,choices = PLAYER_STATUS,default="Not Sold")
    basePrice = models.IntegerField(default=0)
    soldPrice = models.IntegerField(default=0)
    bio = models.CharField(max_length=500,null=True,blank=True)
    team = models.ForeignKey(Team,on_delete=models.DO_NOTHING,null=True,blank=True)
    
    def __str__(self):
        return self.name + ' - ' + str(self.batch) + ' - ' + str(self.classId)

class TeamAccount(models.Model):
    team = models.ForeignKey(Team,on_delete=models.DO_NOTHING)
    coins = models.IntegerField(default=0)
    dueCoins = models.IntegerField()

    def __str__(self):
        return str(self.team)


class PlayerCategoryForAuction(models.Model):
    name = models.CharField(max_length=100)
    tournament = models.ForeignKey(Tournament,on_delete=models.DO_NOTHING,null=True,blank=True)
    players = models.ManyToManyField(Player, related_name="Player_Category")

    def __str__(self):
        return self.name




