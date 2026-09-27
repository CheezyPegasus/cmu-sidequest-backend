# CMU Sidequest Randomizer Backend

A small Flask backend for the CMU Sidequest Randomizer frontend.

The service accepts a user's available time, maximum distance, budget, and group size, filters a small Pittsburgh sidequest catalog on the server, and returns one matching recommendation as JSON.

## Live endpoints

Once deployed to Render:

- `GET /` — API information
- `GET /health` — simple health check
- `POST /recommend` — accepts filters and returns a sidequest

## POST /recommend

Example request:

```json
{
  "time": 3,
  "distance": 10,
  "budget": "free",
  "group": "friends"
}
```

Fields:

- `time`: number of hours, from 0.5 to 16
- `distance`: maximum distance in miles, from 0 to 150
- `budget`: `"free"` or `"paid"`
- `group`: `"solo"`, `"friends"`, or `"group"`

Example response:

```json
{
  "sidequest": {
    "title": "Mount Washington Overlook",
    "category": "view",
    "description": "Head to Mount Washington for one of the classic skyline views of Pittsburgh.",
    "address": "Grandview Ave, Pittsburgh, PA",
    "difficulty": "Easy",
    "cost": "free",
    "distance_miles": 5.0,
    "time_hours": 2.0,
    "uniqueness": 4,
    "niche": 2,
    "accessibility": 4,
    "isolation": 2
  },
  "filters": {
    "time": 3,
    "distance": 10,
    "budget": "free",
    "group": "friends"
  },
  "match_count": 3
}
```

Invalid requests return JSON errors with an appropriate status code.

## How the frontend communicates with the backend

The GitHub Pages frontend calls `POST /recommend` with `fetch()` whenever the user presses the recommendation button.

The frontend sends the current slider/dropdown values as JSON, waits for the backend response, and then places the returned `sidequest` fields into the recommendation card. If the backend returns an error, the frontend displays the error message instead.

A minimal example frontend is included in `frontend-demo/`.

## Run locally

1. Create and activate a virtual environment.

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Run Flask.

```bash
python app.py
```

The backend will be available at:

```text
http://127.0.0.1:5000
```

Test the health endpoint:

```bash
curl http://127.0.0.1:5000/health
```

Test a recommendation:

```bash
curl -X POST http://127.0.0.1:5000/recommend \
  -H "Content-Type: application/json" \
  -d '{"time":3,"distance":10,"budget":"free","group":"friends"}'
```

## Environment variables / secrets

This MVP does not require an API key.

`FRONTEND_ORIGIN` is optional. It controls which website is permitted by CORS to call the backend.

For quick testing it defaults to:

```text
*
```

For deployment, it can be set on Render to the GitHub Pages origin, for example:

```text
https://cheezypegasus.github.io
```

If a third-party API such as NVIDIA is added later, its API key should be stored only as a Render environment variable (and in a local `.env` file that is ignored by Git), never in frontend JavaScript or committed to GitHub.

## Deploy to Render

1. Push this repository to GitHub.
2. In Render, choose **New → Web Service**.
3. Connect the GitHub repository.
4. Use:
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
5. Deploy.
6. Visit `/health` on the Render URL.
7. Replace `BACKEND_URL` in your frontend with the Render URL.

The included `render.yaml` contains the same basic configuration.

## Error handling

The server validates:

- missing JSON fields
- invalid time/distance types
- out-of-range time or distance
- invalid budget or group choices
- requests where no sidequests match the supplied filters

Errors are returned as JSON so the frontend can display them cleanly.
