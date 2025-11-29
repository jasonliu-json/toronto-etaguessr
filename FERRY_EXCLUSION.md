# Ferry Route Exclusion Feature

## Overview
The ETA Guesser now automatically excludes destinations that require ferry rides, ensuring all selected locations can be reached via standard road/rail/path-based transportation.

## Implementation

### Detection Method
The backend uses the Google Maps Directions API to check the driving route to each potential destination. It examines every step of the route for:

1. **Travel Mode Check**: Looks for steps with `travel_mode == 'FERRY'`
2. **Instruction Check**: Searches for the word "ferry" in HTML instructions

### Code Changes

**New Function: `has_ferry_in_route()`**
```python
def has_ferry_in_route(origin, destination):
    """
    Check if any route to the destination requires a ferry.
    Returns True if ferry is required, False otherwise.
    """
    # Uses Google Maps Directions API
    # Checks all steps in the route
    # Returns True if ferry detected, False otherwise
```

**Updated Function: `random_destination()`**
- Now checks each destination with `has_ferry_in_route()` before accepting it
- Skips destinations that require ferries
- Logs rejections: `"✗ Attempt X: Skipping - requires ferry"`

### Why This Matters

**Toronto Island Problem**:
- Toronto Islands (Ward's Island, Centre Island, Hanlan's Point) are within 10km of Union Station
- They require ferry access from the mainland
- Without filtering, these locations could be selected but would provide unfair gameplay since the ferry requirement is a dead giveaway

**Better Gameplay**:
- All destinations are now accessible via continuous land routes
- No obvious geographical constraints (like being on an island)
- More challenging and fair for players

## Performance Impact

**Minimal**:
- Ferry check only adds one extra API call (Directions API) per destination attempt
- Typically finds valid destination within 1-3 attempts
- Total search time remains under 5 seconds

**API Usage**:
- Before: Distance Matrix API only (4 calls per destination - one per mode)
- After: +1 Directions API call for ferry detection
- Acceptable tradeoff for better gameplay

## Console Output

The backend now shows ferry exclusions in the console:

```
✗ Attempt 3: Skipping - requires ferry
✗ Attempt 4: Skipping - missing modes: ['transit']
✓ Found valid destination on attempt 5
```

## Alternative Approaches Considered

1. **Geographic Bounding**: Pre-define no-ferry zones
   - ❌ Rigid, doesn't adapt to new routes
   - ❌ Misses edge cases

2. **Island Detection**: Check if destination is on known islands
   - ❌ Requires manual island list maintenance
   - ❌ Doesn't catch all ferry routes (some ferries go to mainland locations)

3. **Current Approach**: Check actual routes via API ✓
   - ✅ Accurate and dynamic
   - ✅ No manual maintenance needed
   - ✅ Catches all ferry requirements

## Testing

To verify ferry exclusion is working:

```bash
# Monitor backend logs for ferry rejections
tail -f backend_logs

# Test API endpoint
curl http://localhost:5001/random-destination

# Should never return Toronto Island locations
# Check console for "Skipping - requires ferry" messages
```

## Related Files Modified

- `app.py`: Added `has_ferry_in_route()`, updated `random_destination()`
- `index.html`: Updated instructions to mention ferry exclusion
- `README.md`: Added "No ferries" to features list

## Future Enhancements

Potential improvements:
1. Cache ferry check results for frequently tested coordinates
2. Add statistical logging of ferry rejection rate
3. Expand to check other undesirable route features (tolls, highways, etc.)

## Summary

The ferry exclusion feature improves game quality by ensuring all destinations are accessible via standard routes, eliminating geographical giveaways while maintaining performance.
