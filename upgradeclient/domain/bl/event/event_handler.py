#! -*- coding: utf-8 -*-


from upgradeclient.domain.model.event.event import Event
from upgradeclient.domain.model.event.event_type import EventType


class EventHandler(object):
    @staticmethod
    def create_event(event_name=EventType.CHECKING, **kwargs):
        event = Event(name=event_name, **kwargs)

        return event

