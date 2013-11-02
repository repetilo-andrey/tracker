from django.utils import unittest
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from .models import Ticket, TimePeriod, Project

from datetime import datetime, timedelta


from jsonrpc.proxy import ServiceProxy


class TimingTest(unittest.TestCase):

    def test_create_ticket_and_project(self):

        s = ServiceProxy('http://localhost:9999/timing/rpc/')
       # s.timing.create_ticket('project', 'ticket', 0)

        print s
        '''
        ticket_simple = Ticket.objects.create(
            name='Ticket name',
            status='Doing',
            trello_description='description')
        self.assertEqual(Ticket.objects.count(), 1)
        ticket_simple.delete()

        client = Client()
        ticket_data = {'trello_id': '123qwe',
                       'trello_ticket_name': 'Trello ticket name',
                       'trello_label': 'label',
                       'trello_description': 'description',
                       'trello_status': 'Doing',
                       'trello_user': '321ewq',
                       'trello_url': 'url'}
        kwargs = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        response = client.post(reverse('create-ticket'), ticket_data, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Ticket.objects.count(), 1)

        ticket = Ticket.objects.get(id=1)
        TimePeriod.objects.create(
            ticket=ticket,
            time_start=datetime.now(),
            time_end=datetime.now() + timedelta(minutes=1))
        self.assertNotEqual(ticket.time_logged, None)
        '''
'''

class ProjectsTest(WebTest):

    def test_get_request(self):
        """Check projects info page"""

        # Check page content
        project = Project.objects.create(
            trello_id='1q',
            name='Name'
        )
        projects = Project.objects.all()
        response = self.app.get(reverse('projects'))

        self.assertContains(response, project.name[0])

        # Check total_time counting
        ticket1 = Ticket.objects.create(
            trello_id='123qwe',
            trello_ticket_name='Trello ticket name',
            trello_label='label',
            trello_status='Doing',
            trello_description='description',
            project_id='1q')
        ticket2 = Ticket.objects.create(
            trello_id='321asd',
            trello_ticket_name='Trello ticket name2',
            trello_label='label2',
            trello_status='Doing',
            trello_description='description2',
            project_id='1q')
        time_period1 = TimePeriod.objects.create(
            ticket=ticket1,
            time_start=datetime.now(),
            time_end=datetime.now() + timedelta(minutes=1))
        time_period2 = TimePeriod.objects.create(
            ticket=ticket2,
            time_start=datetime.now() + timedelta(minutes=2),
            time_end=datetime.now() + timedelta(minutes=3))

        #self.assertNotEqual(project.total_time, None)
        self.assertEqual(Project.objects.count(), 1)
'''