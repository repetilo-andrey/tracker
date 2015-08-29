from datetime import date, datetime
from datetime import timedelta

from django.db.models import signals
from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    total_time = models.CharField(max_length=255, blank=True, null=True)
    users = models.ManyToManyField(User, blank=True, null=True)

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __unicode__(self):
        return self.name


class Ticket(models.Model):
    STATUS = (
        ('Doing', 'Doing'),
        ('Done', 'Done'),)

    name = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=STATUS)
    time_logged = models.TimeField(blank=True, null=True)
    project = models.ForeignKey(Project, blank=True, null=True)
    date_closed = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True)

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'

    def __unicode__(self):
        return self.name[:100]


class TimePeriod(models.Model):
    ticket = models.ForeignKey(Ticket)
    user = models.ForeignKey(User, blank=True, null=True)
    time_start = models.DateTimeField(blank=True, null=True)
    time_end = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Time Period'
        verbose_name_plural = 'Time Periods'

    def __unicode__(self):
        return self.ticket.name


class DayStatistic(models.Model):
    day_time = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True)
    day = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = 'Day Statistic'
        verbose_name_plural = 'Day Statistics'


def post_save_time_period(sender, instance, **kwargs):
    if instance.time_end:
        spent_time = instance.time_end - instance.time_start
        ticket = instance.ticket
        if ticket.time_logged:
            if type(ticket.time_logged) == datetime:
                time_logged = datetime.time(ticket.time_logged)
            else:
                time_logged = ticket.time_logged
            ticket.time_logged = datetime.combine(date.today(), time_logged) + spent_time
        else:
            ticket.time_logged = str(spent_time)
        ticket.save()


def post_save_ticket(sender, instance, **kwargs):
    if instance.time_logged:
        try:
            project = Project.objects.get(id=instance.project.id)
            tickets = Ticket.objects.filter(project=project.id)
            time_logged_list = []
            for ticket in tickets:
                if ticket.time_logged:
                    hours = ticket.time_logged.hour
                    minutes = ticket.time_logged.minute
                    seconds = ticket.time_logged.second
                    time = timedelta(
                        hours=hours,
                        minutes=minutes,
                        seconds=seconds)
                    time_logged_list.append(time)
                    total_time = sum(time_logged_list, timedelta())
                    project.total_time = str(total_time)
                    project.save()
        except Project.DoesNotExist:
            pass


signals.post_save.connect(post_save_time_period, TimePeriod, dispatch_uid="path.to.post_save_time_period.TimePeriod")
signals.post_save.connect(post_save_ticket, Ticket, dispatch_uid="path.to.post_save_ticket.Ticket")
