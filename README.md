# Travel Pal Alexa Skill

A Python Alexa custom skill built with the [Alexa Skills Kit SDK for Python](https://github.com/alexa/alexa-skills-kit-sdk-for-python). It creates a short voice-friendly itinerary from a destination, trip length, interest, and optional month.

## Local setup

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py -m pytest
```

The Lambda entry point is `travel_pal.lambda_function.handler`.

## Add it to Alexa

1. Create a Custom Alexa skill in the Alexa Developer Console.
2. Select **JSON Editor** under Interaction Model and paste `skill-package/interactionModels/custom/en-US.json`.
3. Build the model.
4. Deploy the Python package to AWS Lambda. Set the Lambda handler to `travel_pal.lambda_function.handler`.
5. Add the Lambda ARN as the skill's endpoint and enable testing for your developer account.
6. Say: `Alexa, open travel pal`, then ask for a trip.

For Lambda packaging, install dependencies into the deployment directory before creating the zip:

```powershell
py -m pip install -r requirements.txt -t build
Copy-Item -Recurse travel_pal build\travel_pal
Compress-Archive -Path build\* -DestinationPath travel-pal.zip -Force
```

## Connect your own travel agent

`travel_pal.travel_agent.TravelPlanner` is intentionally independent from Alexa. Replace its `plan` method with your API or agent call, or import the package from another Python application:

```python
from travel_pal import TravelPlanner
from travel_pal.travel_agent import TripRequest

planner = TravelPlanner()
result = planner.plan(TripRequest("Tokyo", 5, "food", "April"))
```

Keep the result as a list of short strings so Alexa can speak it naturally. Add API credentials as Lambda environment variables rather than committing them to this project.
