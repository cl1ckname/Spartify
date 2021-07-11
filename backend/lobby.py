from django.conf import settings

class Queue:
    count = 0

    def __init__(self, request):
        self.session = request.session
        queue = self.session.get(settings.QUEUE_SESSION_ID)
        if not queue:
            queue = self.session[settings.QUEUE_SESSION_ID] = {'links': []}
        self.queue = queue
    
    def add(self, link):
        self.count += 1
        cleared_link = link.split('track/')[1].split('?')[0]
        self.queue['links'].append(cleared_link)
        self.save()
    
    def pop(self) -> str:
        self.count -= 1
        link = self.queue['links'][0]
        del self.queue['links'][0]
        self.save()
        return link

    def get_array(self) -> list:
        return self.queue['links']

    def get_elem(self, id) -> str:
        return self.queue['links'][id]

    def save(self):
        self.session.modified = True

    def remove(self, id):
        del self.queue['links'][id]

    def __len__(self) -> int:
        return self.count

