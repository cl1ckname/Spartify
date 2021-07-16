from django.conf import settings
from datetime import datetime

class Queue:
    count = 0

    def __init__(self, request):
        self.session = request.session
        queue = self.session.get(settings.QUEUE_SESSION_ID)
        if not queue:
            queue = self.session[settings.QUEUE_SESSION_ID] = {'links': [], 'times': [], 'users': []}
        self.queue = queue
    
    def add(self, link, user):
        self.count += 1
        cleared_link = link.split('track/')[1].split('?')[0]
        self.queue['links'].append(cleared_link)
        self.queue['times'].append(datetime.now().strftime('%H:%M'))
        self.queue['users'].append(user)
        self.save()
    
    def pop(self) -> str:
        self.count -= 1
        link = self.queue['links'][0]
        del self.queue['links'][0]
        self.save()
        return link

    def get_links(self) -> list:
        return self.queue['links']

    def get_times(self) -> list:
        return self.queue['times']

    def get_users(self) -> list:
        return self.queue['users']

    def get_elem(self, id) -> str:
        return self.queue['links'][id]

    def save(self):
        self.session.modified = True

    def clear(self):
        self.queue['links'] = []
        self.queue['times'] = []
        self.queue['users'] = []
        self.save()

    def remove(self, id):
        del self.queue['links'][id]
        self.save()

    def __len__(self) -> int:
        return self.count

    def __getitem__(self, key: int) -> tuple:
        return ()