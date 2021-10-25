from django.db.models import QuerySet


class ChatQuerySet(QuerySet):
    def create_chat(self, data):
        try:
            chat = self.get(chat_id=data['id'])
            chat.active = True
            chat.save()

        except self.model.DoesNotExist:
            username = data['username'] if 'username' in data else None
            first_name = data['first_name'] if 'first_name' in data else None
            chat = self.create(chat_id=data['id'], type=data['type'], username=username, first_name=first_name)

        return chat

    def active(self):
        return self.filter(stopped_at=None)
