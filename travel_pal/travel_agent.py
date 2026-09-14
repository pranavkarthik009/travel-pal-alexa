"""Travel planning logic kept independent from Alexa request handling."""

from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class TripRequest:
    destination: str
    days: int
    interest: str = "mixed"
    month: Optional[str] = None


class TravelPlanner:
    """Small deterministic planner that can be replaced by an API or AI agent."""

    def plan(self, request: TripRequest) -> List[str]:
        destination = request.destination.strip()
        interest = request.interest.lower().strip() or "mixed"
        activities = self._activities_for(interest)
        return [
            f"Day {day}: {activities[(day - 1) % len(activities)]} in {destination}."
            for day in range(1, request.days + 1)
        ]

    @staticmethod
    def _activities_for(interest: str) -> List[str]:
        options = {
            "food": ["a local food market", "a neighborhood restaurant tour"],
            "history": ["a historic district walk", "a museum and heritage site"],
            "nature": ["a scenic park or nature trail", "a nearby viewpoint"],
            "shopping": ["a central shopping district", "a local craft market"],
            "mixed": ["a city highlights tour", "a relaxed local experience"],
        }
        return options.get(interest, options["mixed"])


def format_itinerary(request: TripRequest, planner: TravelPlanner) -> str:
    """Return a concise voice-friendly itinerary."""
    lines = planner.plan(request)
    month_text = f" in {request.month}" if request.month else ""
    return (
        f"Here is a {request.days}-day{month_text} plan for {request.destination}. "
        + " ".join(lines)
        + " Would you like to change the interests or destination?"
    )
