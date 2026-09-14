"""AWS Lambda entry point for the Travel Pal Alexa skill."""

from typing import Any, Dict

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_intent_name, is_request_type
from ask_sdk_model import Response

from .travel_agent import TripRequest, TravelPlanner, format_itinerary


planner = TravelPlanner()


class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        speech = (
            "Welcome to Travel Pal. Tell me where you want to go, how many days "
            "you have, and what you enjoy."
        )
        return handler_input.response_builder.speak(speech).ask(speech).response


class PlanTripIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_intent_name("PlanTripIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        slots = handler_input.request_envelope.request.intent.slots
        destination = _slot_value(slots, "destination")
        days = _slot_value(slots, "days")
        interest = _slot_value(slots, "interest") or "mixed"
        month = _slot_value(slots, "month")

        if not destination:
            return handler_input.response_builder.speak(
                "Where would you like to travel?"
            ).ask("Where would you like to travel?").response
        if not days:
            return handler_input.response_builder.speak(
                "How many days will you be traveling?"
            ).ask("How many days will you be traveling?").response

        try:
            day_count = max(1, min(int(days), 14))
        except ValueError:
            return handler_input.response_builder.speak(
                "Please tell me the number of days, from one to fourteen."
            ).ask("How many days will you be traveling?").response

        request = TripRequest(
            destination=destination,
            days=day_count,
            interest=interest,
            month=month,
        )
        speech = format_itinerary(request, planner)
        return handler_input.response_builder.speak(speech).response


class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        speech = "Say, plan a trip to Rome for five days focused on food."
        return handler_input.response_builder.speak(speech).ask(speech).response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_intent_name("AMAZON.CancelIntent")(handler_input) or is_intent_name(
            "AMAZON.StopIntent"
        )(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        return handler_input.response_builder.speak("Safe travels!").set_should_end_session(
            True
        ).response


class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input: HandlerInput) -> bool:
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input: HandlerInput) -> Response:
        return handler_input.response_builder.response


def _slot_value(slots: Dict[str, Any], name: str) -> str:
    slot = slots.get(name)
    return slot.value.strip() if slot and slot.value else ""


sb = SkillBuilder()
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(PlanTripIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

handler = sb.lambda_handler()
