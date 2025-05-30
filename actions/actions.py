from typing import Any, Dict, List, Text
import requests

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher


class fetch_relationship(Action):
    def name(self) -> Text:
        return "action_fetch_relationship"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        response = requests.get(f"https://devapex22.quotevineapp.com/qvine/quotevine/api/v2/relationships/{tracker.get_slot('relationship_id')}",
                                headers={'api-key': '3D31C45E81885027632AE1BDCF325D81DF9B2867'})
        
        json = response.json()

        return [SlotSet("relationship_name", json['display_name']),
                SlotSet("relationship_account_manager", json['account_manager_name']),
                SlotSet("relationship_last_update_date", json['last_update_date'])]

class fetch_opportunity(Action):
    def name(self) -> Text:
        return "action_fetch_opportunity"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        response = requests.get(f"https://devapex22.quotevineapp.com/qvine/quotevine/api/v2/opportunities/{tracker.get_slot('opportunity_id')}/",
                                headers={'api-key': '3D31C45E81885027632AE1BDCF325D81DF9B2867'})
        
        json = response.json()

        return [SlotSet("opportunity_relationship_id", json['relationship_id']),
                SlotSet("opportunity_account_manager", json['account_manager']),
                SlotSet("opportunity_status", json['opportunity_status']),
                SlotSet("opportunity_type", json['opportunity_type'])
                ]


class fetch_quote(Action):
    def name(self) -> Text:
        return "action_fetch_quote"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        response = requests.get(f"https://devapex22.quotevineapp.com/qvine/quotevine/api/v2/relationships/{tracker.get_slot('quote_relationship_id')}/opportunities/{tracker.get_slot('quote_opportunity_id')}/quotes/{tracker.get_slot('quote_id')}",
                                headers={'api-key': '3D31C45E81885027632AE1BDCF325D81DF9B2867'})
        
        json = response.json()

        vehicle = f"{json['manufacturer']} {json['range']} {json['model']} {json['derivative']}"

        return [SlotSet("quote_vehicle", vehicle)]


class reset_slots(Action):
    def name(self) -> Text:
        return 'action_reset_slots'
    
    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[bool]:
        return [AllSlotsReset()]
        