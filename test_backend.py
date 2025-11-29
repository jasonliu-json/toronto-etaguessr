#!/usr/bin/env python3
"""
Test script to validate the ETA Guesser backend functionality.
"""
import requests
import json
import math

BACKEND_URL = "http://localhost:5001"
UNION_STATION = {'lat': 43.6452, 'lng': -79.3806}
MAX_RADIUS_MILES = 30
MAX_RADIUS_KM = MAX_RADIUS_MILES * 1.60934


def calculate_distance(lat1, lng1, lat2, lng2):
    """Calculate distance between two points using Haversine formula."""
    R = 6371  # Earth's radius in km

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)

    a = (math.sin(dlat / 2) ** 2 +
         math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def test_api_connection():
    """Test if the API is accessible."""
    print("Testing API connection...")
    try:
        response = requests.get(f"{BACKEND_URL}/", timeout=5)
        if response.status_code == 200:
            print("✓ API is accessible")
            return True
        else:
            print(f"✗ API returned status code {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Failed to connect to API: {e}")
        return False


def test_random_destination():
    """Test the random destination endpoint."""
    print("\nTesting random destination endpoint...")

    try:
        response = requests.get(f"{BACKEND_URL}/random-destination", timeout=30)

        if response.status_code != 200:
            print(f"✗ API returned status code {response.status_code}")
            return False

        data = response.json()
        print("✓ API returned valid JSON")

        # Check required fields
        required_fields = ['origin', 'destination', 'destination_address', 'etas']
        for field in required_fields:
            if field not in data:
                print(f"✗ Missing required field: {field}")
                return False
        print("✓ All required fields present")

        # Validate origin
        if (data['origin']['lat'] != UNION_STATION['lat'] or
            data['origin']['lng'] != UNION_STATION['lng']):
            print("✗ Origin is not Union Station")
            return False
        print("✓ Origin is Union Station")

        # Validate destination is within radius
        dest = data['destination']
        distance_km = calculate_distance(
            UNION_STATION['lat'], UNION_STATION['lng'],
            dest['lat'], dest['lng']
        )

        print(f"  Distance from Union Station: {distance_km:.2f} km ({distance_km * 0.621371:.2f} miles)")

        if distance_km > MAX_RADIUS_KM:
            print(f"✗ Destination is too far ({distance_km:.2f} km > {MAX_RADIUS_KM:.2f} km)")
            return False
        print(f"✓ Destination is within {MAX_RADIUS_MILES} mile radius")

        # Validate ETAs
        expected_modes = ['driving', 'transit', 'bicycling', 'walking']
        for mode in expected_modes:
            if mode not in data['etas']:
                print(f"✗ Missing ETA for mode: {mode}")
                return False

            eta = data['etas'][mode]
            if 'error' not in eta:
                if 'duration' not in eta or 'distance' not in eta:
                    print(f"✗ Missing duration or distance for mode: {mode}")
                    return False

        print("✓ All travel modes have ETAs")

        # Print sample result
        print("\n  Sample destination:")
        print(f"  Address: {data['destination_address']}")
        print(f"  Coordinates: ({dest['lat']:.4f}, {dest['lng']:.4f})")
        print(f"\n  Travel Times:")
        for mode in expected_modes:
            eta = data['etas'][mode]
            if 'error' not in eta:
                print(f"    {mode.capitalize():12} - {eta['duration']:15} ({eta['distance']})")
            else:
                print(f"    {mode.capitalize():12} - N/A")

        return True

    except Exception as e:
        print(f"✗ Error during test: {e}")
        return False


def test_multiple_destinations():
    """Test that multiple requests return different destinations."""
    print("\nTesting randomness (3 consecutive requests)...")

    destinations = []
    for i in range(3):
        try:
            response = requests.get(f"{BACKEND_URL}/random-destination", timeout=30)
            if response.status_code == 200:
                data = response.json()
                dest = (data['destination']['lat'], data['destination']['lng'])
                destinations.append(dest)
                print(f"  Request {i+1}: ({dest[0]:.4f}, {dest[1]:.4f})")
            else:
                print(f"✗ Request {i+1} failed")
                return False
        except Exception as e:
            print(f"✗ Request {i+1} error: {e}")
            return False

    # Check if destinations are different
    if len(set(destinations)) == 1:
        print("⚠ Warning: All 3 destinations were the same (unlikely but possible)")
    else:
        print(f"✓ Received {len(set(destinations))} unique destinations")

    return True


def main():
    """Run all tests."""
    print("="*60)
    print("ETA Guesser Backend Test Suite")
    print("="*60)

    results = []

    # Run tests
    results.append(("API Connection", test_api_connection()))
    results.append(("Random Destination", test_random_destination()))
    results.append(("Multiple Requests", test_multiple_destinations()))

    # Print summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)

    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name:25} {status}")

    total_passed = sum(1 for _, passed in results if passed)
    total_tests = len(results)

    print("="*60)
    print(f"Total: {total_passed}/{total_tests} tests passed")
    print("="*60)

    return total_passed == total_tests


if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)
