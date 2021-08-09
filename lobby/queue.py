from django.conf import settings
from datetime import datetime

class Queue:
    count = 0

    def __init__(self, request):
        self.session = request.session
        queue = self.session.get(settings.QUEUE_SESSION_ID)
        if not queue:
            queue = self.session[settings.QUEUE_SESSION_ID] = {'names': [], 'times': [], 'users': []}
        self.queue = queue
    
    def add(self, name, user):
        self.count += 1
        self.queue['names'] = [name] + self.queue['names']
        self.queue['times'] = [datetime.now().strftime('%H:%M')] + self.queue['times']
        self.queue['users'] = [user] + self.queue['users']
        self.save()
    
    def pop(self) -> str:
        self.count -= 1
        link = self.queue['names'][0]
        del self.queue['names'][0]
        self.save()
        return link

    def get_names(self) -> list:
        return self.queue['names']

    def get_times(self) -> list:
        return self.queue['times']

    def get_users(self) -> list:
        return self.queue['users']

    def get_elem(self, id) -> str:
        return self.queue['names'][id]

    def save(self):
        self.session.modified = True

    def clear(self):
        self.queue['names'] = []
        self.queue['times'] = []
        self.queue['users'] = []
        self.save()

    def remove(self, id):
        del self.queue['names'][id]
        self.save()

    def __len__(self) -> int:
        return self.count

    def __getitem__(self, key: int) -> tuple:
        return ()