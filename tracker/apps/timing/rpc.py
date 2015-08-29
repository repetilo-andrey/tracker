# -*- coding: utf-8 -*_
import datetime as dt
from datetime import datetime, timedelta

from jsonrpc import jsonrpc_method

from .models import Ticket, TimePeriod, Project, DayStatistic


@jsonrpc_method('timing.close_open_ticket(ticket_id=Number)->Array', validate=True)
def close_open_ticket(request, ticket_id):
    """Update ticket status"""
    ticket = Ticket.objects.get(id=ticket_id)
    if ticket.status == 'Doing':
        ticket.status = 'Done'
    else:
        ticket.status = 'Doing'
    ticket.save()
    return {'success': 'ticket status has been changed'}


@jsonrpc_method('timing.get_projects()')
def get_projects(request):
    """ Get list of projects """
    projects = {}
    for project in Project.objects.filter(users=request.user.id):
        projects[project.id] = project.name
    return {'projects': projects}


@jsonrpc_method('timing.get_tickets()', validate=True)
def get_tickets(request):
    """ Get list of tickets """
    tickets = Ticket.objects.filter(status='Doing', user=request.user)
    tickets_list = []
    for ticket in tickets:
        tickets_dict = {}
        tickets_dict['id'] = ticket.id
        tickets_dict['name'] = ticket.name
        tickets_dict['project'] = ticket.project.name
        tickets_dict['time'] = ticket.time_logged.strftime("%H:%M:%S") if ticket.time_logged else '00:00:00'
        tickets_list.append(tickets_dict)
    return {'tickets': tickets_list}


@jsonrpc_method('timing.get_archived_tickets()', validate=True)
def get_archived_tickets(request):
    """ Get list of archived tickets """
    projects = Project.objects.filter(ticket__status='Done',
                                      users=request.user.id).distinct()
    projects_dict = {}
    for project in projects:
        tickets = Ticket.objects.filter(status='Done', project=project)
        tickets_list = []
        for ticket in tickets:
            tickets_dict = {}
            tickets_dict['id'] = ticket.id
            tickets_dict['name'] = ticket.name
            tickets_dict['time'] = ticket.time_logged.strftime("%H:%M:%S") if ticket.time_logged else '00:00:00'
            tickets_list.append(tickets_dict)
        projects_dict[project.id] = {'id': project.id,
                                     'name': project.name,
                                     'total_time': project.total_time,
                                     'tickets': tickets_list}
    return {'projects': projects_dict}


@jsonrpc_method('timing.create_ticket(project_name=String, name=String, new_project=Number)->Array', validate=True)
def create_ticket(request, project_name, name, new_project):
    """Create ticket"""
    if new_project:
        try:
            Project.objects.get(name=project_name)
            return {'project_error': 'Project with the same name already exists'}
        except Project.DoesNotExist:
            project = Project.objects.create(name=project_name)
            project.users.add(request.user)
    else:
        project = Project.objects.get(name=project_name)
    try:
        Ticket.objects.get(name=name, project=project)
        return {'ticket_error': 'Ticket with this name already exists in project'}
    except Ticket.DoesNotExist:
        ticket = Ticket.objects.create(name=name, project=project, status='Doing',
                                       user=request.user)
    ticket_data = {}
    ticket_data['id'] = ticket.id
    ticket_data['name'] = ticket.name
    ticket_data['project'] = ticket.project.name
    ticket_data['time'] = ticket.time_logged.strftime("%H:%M:%S") if ticket.time_logged else '00:00:00'
    return {'success': 'ticket created', 'ticket_data': ticket_data}


@jsonrpc_method('timing.create_time_period(ticket_id=Number, time_end=Number)->Array', validate=True)
def create_time_period(request, ticket_id, time_end):
    """ Create the beginning and the end of time periods"""
    ticket = Ticket.objects.get(id=ticket_id)
    if time_end:
        time_period = TimePeriod.objects.filter(
            ticket=ticket).latest('time_start')
        if not time_period.time_end:
            time_period.time_end = datetime.now()
        date = dt.date.today()
        try:
            DayStatistic.objects.get(day=date, user=request.user)
        except DayStatistic.DoesNotExist:
            DayStatistic.objects.create(day=date, user=request.user)
    else:
        time_period = TimePeriod(ticket=ticket)
        time_period.time_start = datetime.now()
    time_period.save()
    return {'success': 'time period created'}


@jsonrpc_method('timing.show_logged_time(logged_time=String)->Array', validate=True)
def show_logged_time(request, logged_time):
    """Update showing logged_time value every minute"""
    time_tuple = datetime.strptime(logged_time, "%H:%M:%S")
    time_logged = time_tuple + timedelta(minutes=1)
    time_logged = time_logged.strftime("%H:%M:%S")
    return {'html': time_logged}


@jsonrpc_method('timing.get_month_and_years()', validate=True)
def get_month_and_years(request):
    """ Get current month & year"""
    month = dt.date.today().month
    current_year = dt.date.today().year
    days = DayStatistic.objects.filter(user=request.user)
    year = 0
    if len(days) == 0:
        years = [{'id': year, 'value': dt.date.today().year}]
    else:
        years_list = list(set([i.year for i in days.values_list('day', flat=True)]))
        if current_year not in years_list:
            years_list.append(current_year)
        years = []
        for i, y in enumerate(sorted(years_list)):
            years.append({'id': i, 'value': y})
            if y == current_year:
                year = i
    return {'month': month, 'year': year, 'years': years}


@jsonrpc_method('timing.get_day_stat(month=Number, year=Number)', validate=True)
def get_day_stat(request, month, year):
    """ Get stat_by_day & stat_by_ticket """
    stat_by_day = {}
    month_time = dt.timedelta(0)
    for day in DayStatistic.objects.filter(user=request.user):

        if day.day.year == year and day.day.month == month:
            day_number = day.day.day
            time_periods_list = []
            total_time = dt.timedelta(0)
            for ticket in Ticket.objects.filter(user=request.user):
                time_periods = ticket.timeperiod_set.filter(time_end__day=day_number, time_end__month=month)
                if len(time_periods) > 0:
                    times_start = time_periods.values_list('time_start')
                    times_end = time_periods.values_list('time_end')
                    time_logged_list = [times_end[i][0] - times_start[i][0] for i, v in enumerate(times_end)]
                    time = sum(time_logged_list, timedelta(milliseconds=0))
                    total_time += time
                    time_periods_list.append([ticket.project.name, ticket.name, str(time).split('.')[0]])
            current_month = dt.date.today().month
            month_time += total_time
            stat_by_day[day_number] = {'day_number': day_number,
                                       'current_month': current_month,
                                       'total_time': str(total_time).split('.')[0],
                                       'items': time_periods_list}

    stat_by_ticket = {}
    for tp in TimePeriod.objects.filter(ticket__user=request.user):
        total_time = dt.timedelta(0)
        if tp.time_end and tp.time_end.month == month and tp.ticket.id not in stat_by_ticket.keys():
            time_periods = tp.ticket.timeperiod_set.filter(time_end__month=month)
            if len(time_periods) > 0:
                times_start = time_periods.values_list('time_start')
                times_end = time_periods.values_list('time_end')
                time_logged_list = [times_end[i][0] - times_start[i][0] for i, v in enumerate(times_end)]
                time = sum(time_logged_list, timedelta(milliseconds=0))
                total_time += time
            stat_by_ticket[tp.ticket.id] = {'project': tp.ticket.project.name,
                                            'ticket': tp.ticket.name, 'time': str(total_time).split('.')[0]}

    return {'stat_by_day': stat_by_day,
            'month_time': str(month_time).split('.')[0],
            'stat_by_ticket': stat_by_ticket}


MONTHS_IN_YEAR = (
    (1, 'January'),
    (2, 'February'),
    (3, 'March'),
    (4, 'April'),
    (5, 'May'),
    (6, 'June'),
    (7, 'July'),
    (8, 'August'),
    (9, 'September'),
    (10, 'October'),
    (11, 'November'),
    (12, 'December')
)
