from travel_pal.travel_agent import TripRequest, TravelPlanner, format_itinerary


def test_planner_creates_one_entry_per_day():
    itinerary = TravelPlanner().plan(
        TripRequest(destination="Lisbon", days=3, interest="food")
    )

    assert len(itinerary) == 3
    assert itinerary[0] == "Day 1: a local food market in Lisbon."


def test_unknown_interest_falls_back_to_mixed():
    response = format_itinerary(
        TripRequest(destination="Oslo", days=1, interest="photography"),
        TravelPlanner(),
    )

    assert "city highlights tour" in response
    assert "Oslo" in response
