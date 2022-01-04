from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem

from ticktick.api import TickTickClient
from ticktick.oauth2 import OAuth2


class TickTickTasks(Extension):
    TICKTICK = None

    def __init__(self):
        super(TickTickTasks, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = []

        data = {
            'note': event.get_argument(),
        }
        items.append(ExtensionResultItem(icon='images/icon.png',
                                         name='%s' % data['note'],
                                         description='Create Task: %s' % data['note'],
                                         on_enter=ExtensionCustomAction(data))
                     )
        return RenderResultListAction(items)


class ItemEnterEventListener(EventListener):

    def on_event(self, event, extension):
        auth_client = OAuth2(client_id=extension.preferences.get("ticktick_client_id"),
                             client_secret=extension.preferences.get("ticktick_client_secret"),
                             redirect_uri='http://127.0.0.1:8080/')

        client = TickTickClient(username=extension.preferences.get("ticktick_email"),
                                password=extension.preferences.get("ticktick_password"),
                                oauth=auth_client)

        data = event.get_data()
        name = data['note']
        local_task = client.task.builder(name)
        return RenderResultListAction([ExtensionResultItem(on_enter=client.task.create(local_task))])


if __name__ == '__main__':
    TickTickTasks().run()
