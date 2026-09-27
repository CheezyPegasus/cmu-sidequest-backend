# Prompt Log

## Tools used

- ChatGPT (GPT-5.6 Sol)

## Key prompts / decisions

1. Asked for help identifying a small backend feature that could be deployed on Render and connected to an existing GitHub Pages portfolio / CMU Sidequest Randomizer.
2. Decided to use a Flask backend with a `POST /recommend` endpoint and a `GET /health` endpoint.
3. Asked for an MVP that could be launched quickly before the assignment deadline and modified afterward.
4. Chose a small server-side Pittsburgh sidequest catalog for the first deploy so the frontend/backend integration can be tested independently of third-party API availability.
5. Added server-side validation, JSON error responses, CORS support, Render configuration, README documentation, and a minimal frontend demo.

## AI-generated code review

Before submitting, I reviewed the generated code and verified that I understand:

- how Flask routes map URLs to Python functions
- how `request.get_json()` reads the frontend request
- how the server validates the input
- how the recommendation is selected
- how Flask returns JSON to the browser
- how the frontend uses `fetch()` to call the Render backend
- why CORS is needed when GitHub Pages and Render use different origins
