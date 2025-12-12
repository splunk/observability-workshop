#!/usr/bin/env python3
# Copyright The OpenTelemetry Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
HTTP Client for Travel Planner

This client connects to the travel planner Flask server and sends requests
with random destinations/origins and custom poison configurations.
"""

import json
import os
import random
import sys
from typing import Optional
from pprint import pprint

import requests


# Available cities for random selection
ORIGINS = ["Seattle", "New York", "San Francisco", "London", "Boston", "Chicago"]
DESTINATIONS = ["Paris", "Tokyo", "Rome", "Barcelona", "Sydney", "Dubai"]

# Poison type options
POISON_TYPES = [
    "hallucination",
    "bias",
    "irrelevance",
    "negative_sentiment",
    "toxicity",
]


def generate_random_poison_config() -> dict:
    """Generate a random poison configuration for testing."""
    # Random probability between 0.5 and 1.0
    prob = round(random.uniform(0.5, 1.0), 2)

    # Random subset of poison types
    num_types = random.randint(1, len(POISON_TYPES))
    types = random.sample(POISON_TYPES, num_types)

    # Random max snippets
    max_snippets = random.randint(1, 3)

    return {
        "prob": prob,
        "types": types,
        "max": max_snippets,
        "seed": str(random.randint(1000, 9999)),
    }


def generate_travel_request(origin: str, destination: str) -> str:
    """Generate a natural language travel request."""
    templates = [
        f"We're planning a romantic week-long trip to {destination} from {origin}. "
        "Looking for boutique hotel, business-class flights and unique experiences.",
        f"Need help planning a family vacation to {destination} departing from {origin}. "
        "Want comfortable accommodations, convenient flights, and fun activities.",
        f"Solo traveler here! Planning an adventure to {destination} from {origin}. "
        "Interested in budget-friendly options but premium experiences.",
        f"Planning a corporate retreat to {destination} from {origin}. "
        "Need elegant hotel, flexible flights, and team-building activities.",
    ]
    return random.choice(templates)


def run_client(
    use_poison: bool = True,
    custom_origin: Optional[str] = None,
    custom_destination: Optional[str] = None,
):
    """Run the HTTP client to request travel planning."""
    # Select random or custom cities
    origin = custom_origin or random.choice(ORIGINS)
    destination = custom_destination or random.choice(DESTINATIONS)

    print("🌍 Travel Planner HTTP Client")
    print("=" * 60)
    print(f"📍 Origin: {origin}")
    print(f"🎯 Destination: {destination}")

    # Generate poison config if requested
    poison_config = None
    if use_poison:
        poison_config = generate_random_poison_config()
        print("\n💉 Poison Configuration:")
        print(f"  Probability: {poison_config['prob']}")
        print(f"  Types: {', '.join(poison_config['types'])}")
        print(f"  Max snippets: {poison_config['max']}")
        print(f"  Seed: {poison_config['seed']}")

    # Generate user request
    user_request = generate_travel_request(origin, destination)
    print("\n✉️  User Request:")
    print(f"  {user_request}")

    # Get server URL from environment or default to localhost
    server_url = os.getenv("SERVER_URL", "http://localhost:8080")

    print("\n🔌 Connecting to Flask server...")
    print(f"  URL: {server_url}")

    # Prepare request data
    data = {
        "origin": origin,
        "destination": destination,
        "user_request": user_request,
        "travellers": random.randint(1, 4),
    }

    if poison_config:
        data["poison_config"] = poison_config

    print("\n📤 Sending request to server...")

    try:
        # Make HTTP POST request to /travel/plan endpoint
        response = requests.post(
            f"{server_url}/travel/plan",
            json=data,
            timeout=300,  # 5 minutes timeout for long-running travel planning
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()

        result = response.json()

        print("\n✅ Received response from server!")
        print("=" * 60)

        # Display the result
        print(f"\n📋 Session ID: {result['session_id']}")
        print(f"📅 Travel Dates: {result['departure']} → {result['return_date']}")
        print(f"👥 Travellers: {result['travellers']}")

        if result.get("poison_events"):
            print("\n💉 Poison Events Triggered:")
            for event in result["poison_events"]:
                print(f"  - {event}")

        print("\n✈️  Flight Summary:")
        print(f"  {result['flight_summary']}")

        print("\n🏨 Hotel Summary:")
        print(f"  {result['hotel_summary']}")

        print("\n🎭 Activities Summary:")
        print(f"  {result['activities_summary']}")

        print("\n🎉 Final Itinerary:")
        print("─" * 60)
        print(result["final_itinerary"])
        print("─" * 60)

        if result.get("agent_steps"):
            print("\n🤖 Agent Steps:")
            for step in result["agent_steps"]:
                print(f"  - {step['agent']}: {step['status']}")

    except requests.exceptions.Timeout:
        print("\n❌ Error: Request timed out after 5 minutes")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error: Failed to connect to server: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"\n❌ Error: Invalid JSON response: {e}")
        print(f"Response text: {response.text}")
        sys.exit(1)
    except KeyError as e:
        print(f"\n❌ Error: Missing key in response: {e}")
        print("Response:")
        pprint(result)
        sys.exit(1)


def main():
    """Main entry point for the client."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Travel Planner MCP Client - Request travel itineraries with optional quality evaluation"
    )
    parser.add_argument(
        "--no-poison",
        action="store_true",
        help="Disable poison configuration (no quality degradation testing)",
    )
    parser.add_argument(
        "--origin",
        type=str,
        help=f"Origin city (default: random from {ORIGINS})",
    )
    parser.add_argument(
        "--destination",
        type=str,
        help=f"Destination city (default: random from {DESTINATIONS})",
    )

    args = parser.parse_args()

    try:
        run_client(
            use_poison=not args.no_poison,
            custom_origin=args.origin,
            custom_destination=args.destination,
        )
    except KeyboardInterrupt:
        print("\n\n❌ Client interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
