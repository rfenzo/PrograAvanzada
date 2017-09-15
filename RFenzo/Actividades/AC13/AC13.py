import json
import pickle
from datetime import datetime as dt
from os import listdir


class Usuario:

    def __init__(self, name, contacts, phone_number):
        self.name = name
        self.contacts = contacts
        self.phone_number = phone_number


class UserEncoder(json.JSONEncoder):

    def default(self, obj):

        if isinstance(obj, Usuario):
            return {'name': obj.name,
                    'contacts': obj.contacts,
                    'phone_number': obj.phone_number}

        return super().default(obj)


class Mensaje:

    def __init__(self, send_by, last_view_date, date, content, send_to):
        self.send_by = send_by
        self.last_view_date = last_view_date
        self.date = date
        self.content = content
        self.send_to = send_to

    def __getstate__(self):
        nueva = self.__dict__.copy()
        n = self.send_by
        alf = list('abcdefghijklmnopqrstuvwxyz')
        text = ''
        for char in self.content:
            if char.isalpha():
                pos = (ord(char)+n-97) % 26
                text += alf[pos]
            else:
                text += char
        nueva.update({"content": text})
        return nueva

    def __setstate__(self, state):
        state.update({"last_view_date": dt.now()})
        self.__dict__ = state

# SERIALIZACION


def get_users():
    usuarios = []
    for file_name in listdir('db/usr'):
        with open('db/usr/{}'.format(file_name)) as f:
            usuarios.append(json.load(f, object_hook=lambda x: Usuario(**x)))
    return usuarios


def get_msgs():
    mensajes = []
    for file_name in listdir('db/msg/'):
        with open('db/msg/{}'.format(file_name)) as f:
            mensajes.append(json.load(f, object_hook=lambda x: Mensaje(**x)))
    return mensajes

msgs = get_msgs()
users = get_users()

for user in users:
    for msg in msgs:
        if user.phone_number == msg.send_by:
            user.contacts.append(msg.send_to)

# ENCRIPTACION

for file_name in listdir('db/usr'):
    with open('secure_db/usr/{}.json'.format(file_name), 'w') as f:
        json.dump(users, f, cls=UserEncoder)

for file_name in listdir('db/msg'):
    with open('secure_db/msg/{}'.format(file_name), 'wb') as f:
        pickle.dump(msgs, f)
