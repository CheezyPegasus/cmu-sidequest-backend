import os
import random

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

# For the MVP, allow requests from anywhere so GitHub Pages can talk to Render.
# Tonight, you can tighten this by setting FRONTEND_ORIGIN on Render.
frontend_origin = os.getenv("FRONTEND_ORIGIN", "*")
CORS(app, resources={r"/*": {"origins": frontend_origin}})

SIDEQUESTS = [
    {
        "title": "Schenley Park Walk",
        "category": "outdoors",
        "description": "Take a low-cost reset with a walk through Schenley Park near campus.",
        "address": "Schenley Park, Pittsburgh, PA",
        "recommended_for": ["solo", "friends", "group"],
        "difficulty": "Easy",
        "cost": "free",
        "distance_miles": 1.0,
        "time_hours": 1.0,
        "uniqueness": 3,
        "niche": 2,
        "accessibility": 5,
        "isolation": 3,
    },
    {
        "title": "Phipps Conservatory",
        "category": "museum",
        "description": "Explore botanical rooms and seasonal exhibits next to Schenley Park.",
        "address": "1 Schenley Dr, Pittsburgh, PA 15213",
        "recommended_for": ["solo", "friends", "group"],
        "difficulty": "Easy",
        "cost": "paid",
        "distance_miles": 1.2,
        "time_hours": 2.0,
        "uniqueness": 4,
        "niche": 3,
        "accessibility": 5,
        "isolation": 2,
    },
    {
        "title": "Carnegie Museum of Art + Natural History",
        "category": "museum",
        "description": "Spend a few hours exploring art, dinosaurs, minerals, architecture, and more.",
        "address": "4400 Forbes Ave, Pittsburgh, PA 15213",
        "recommended_for": ["solo", "friends", "group"],
        "difficulty": "Easy",
        "cost": "paid",
        "distance_miles": 0.5,
        "time_hours": 3.0,
        "uniqueness": 4,
        "niche": 3,
        "accessibility": 5,
        "isolation": 1,
    },
    {
        "title": "Cathedral of Learning Exploration",
        "category": "architecture",
        "description": "Walk through the Cathedral of Learning and explore its dramatic Gothic interior.",
        "address": "4200 Fifth Ave, Pittsburgh, PA 15260",
        "recommended_for": ["solo", "friends"],
        "difficulty": "Easy",
        "cost": "free",
        "distance_miles": 0.8,
        "time_hours": 1.0,
        "uniqueness": 4,
        "niche": 3,
        "accessibility": 4,
        "isolation": 2,
    },
    {
        "title": "Mount Washington Overlook",
        "category": "view",
        "description": "Head to Mount Washington for one of the classic skyline views of Pittsburgh.",
        "address": "Grandview Ave, Pittsburgh, PA",
        "recommended_for": ["solo", "friends", "group"],
        "difficulty": "Easy",
        "cost": "free",
        "distance_miles": 5.0,
        "time_hours": 2.0,
        "uniqueness": 4,
        "niche": 2,
        "accessibility": 4,
        "isolation": 2,
    },
    {
        "title": "Duquesne Incline",
        "category": "transit",
        "description": "Ride a historic incline and pair it with the Mount Washington overlook.",
        "address": "1197 W Carson St, Pittsburgh, PA 15219",
        "recommended_for": ["solo", "friends", "group"],
        "difficulty": "Easy",
        "cost": "paid",
        "distance_miles": 5.0,
        "time_hours": 2.0,
        "uniqueness": 5,
        "niche": 3,
        "accessibility": 4,
        "isolation": 1,
    },
    {
        "title": "Point State Park",
        "category": "outdoors",
        "description": "Visit the point where Pittsburgh's three rivers meet and walk the riverfront.",
        "address": "601 Commonwealth Pl, Pittsburgh, PA 15222",
        "recommended_for": ["solo", "friends", "group"],
        "difficulty": "Easy",
        "cost": "free",
        "distance_miles": 4.0,
        "time_hours": 2.0,
        "uniqueness": 4,
        "niche": 2,
        "accessibility": 5,
        "isolation": 2,
    },
    {
        "title": "Andy Warhol Museum",
        "category": "museum",
        "description": "Explore a museum dedicated to Pittsburgh-born artist Andy Warhol.",
        "address": "117 Sandusky St, Pittsburgh, PA 15212",
        "recommended_for": ["solo", "friends"],
        "difficulty": "Easy",
        "cost": "paid",
        "distance_miles": 4.0,
        "time_hours": 2.5,
        "uniqueness": 5,
        "niche": 4,
        "accessibility": 5,
        "isolation": 2,
    },
    {
        "title": "Strip District Food Crawl",
        "category": "food",
        "description": "Walk through the Strip District and pick a few inexpensive snacks or meals.",
        "address": "Penn Ave, Strip District, Pittsburgh, PA",
        "recommended_for": ["solo", "friends", "group"],
        "difficulty": "Easy",
        "cost": "paid",
        "distance_miles": 3.5,
        "time_hours": 3.0,
        "uniqueness": 4,
        "niche": 3,
        "accessibility": 4,
        "isolation": 1,
    },
    {
        "title": "Frick Park Hike",
        "category": "outdoors",
        "description": "Get farther from campus and spend a few hours on wooded trails in Frick Park.",
        "address": "Frick Park, Pittsburgh, PA",
        "recommended_for": ["solo", "friends"],
        "difficulty": "Moderate",
        "cost": "free",
        "distance_miles": 4.0,
        "time_hours": 3.0,
        "uniqueness": 3,
        "niche": 3,
        "accessibility": 3,
        "isolation": 5,
    },
]


@app.get("/")
def index():
    return jsonify(
        {
            "service": "CMU Sidequest Randomizer Backend",
            "message": "POST JSON to /recommend or visit /health.",
        }
    )


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


def validate_payload(data):
    if not isinstance(data, dict):
        return "Request body must be JSON."

    required = ["time", "distance", "budget", "group"]
    missing = [field for field in required if field not in data]
    if missing:
        return f"Missing field(s): {', '.join(missing)}"

    try:
        time_hours = float(data["time"])
        distance_miles = float(data["distance"])
    except (TypeError, ValueError):
        return "time and distance must be numbers."

    if not 0.5 <= time_hours <= 16:
        return "time must be between 0.5 and 16 hours."

    if not 0 <= distance_miles <= 150:
        return "distance must be between 0 and 150 miles."

    if data["budget"] not in {"free", "paid"}:
        return "budget must be either 'free' or 'paid'."

    if data["group"] not in {"solo", "friends", "group"}:
        return "group must be 'solo', 'friends', or 'group'."

    return None


@app.post("/recommend")
def recommend():
    data = request.get_json(silent=True)
    error = validate_payload(data)

    if error:
        return jsonify({"error": error}), 400

    time_hours = float(data["time"])
    distance_miles = float(data["distance"])
    budget = data["budget"]
    group = data["group"]

    matches = [
        item
        for item in SIDEQUESTS
        if item["time_hours"] <= time_hours
        and item["distance_miles"] <= distance_miles
        and group in item["recommended_for"]
        and (budget == "paid" or item["cost"] == "free")
    ]

    if not matches:
        return (
            jsonify(
                {
                    "error": "No sidequest matches those filters yet. Try increasing time/distance or allowing paid activities."
                }
            ),
            404,
        )

    # Random among valid results to keep the "randomizer" feel.
    choice = random.choice(matches)

    return jsonify(
        {
            "sidequest": choice,
            "filters": {
                "time": time_hours,
                "distance": distance_miles,
                "budget": budget,
                "group": group,
            },
            "match_count": len(matches),
        }
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
