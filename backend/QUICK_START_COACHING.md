# Quick Start: Coaching System

## What Was Built

A backend intelligence system that provides **strategic coaching guidance** instead of exact scripts to read.

## Key Differences

### OLD (Suggestion Mode)
```json
{
  "primary_suggestion": {
    "text": "Say this exact thing right now...",
    "reasoning": "Why to say it"
  }
}
```

### NEW (Coaching Mode)
```json
{
  "stage": {"current": "discovery", "confidence": 85},
  "focus": {
    "what": "Understand their pain points",
    "why": "Need to qualify before pitching"
  },
  "guidance": {
    "direction": "Ask about their challenges",
    "key_questions": [
      "What's your biggest phone challenge?",
      "How many calls per day?",
      "What happens when you miss a call?"
    ],
    "talking_points": ["Listen actively", "Ask open-ended questions"]
  },
  "objectives": {
    "completed": [{"id": "rapport", "text": "Build rapport"}],
    "remaining": [{"id": "identify_pain", "text": "Identify pain point"}]
  }
}
```

## How to Enable

1. **Edit `.env`:**
   ```bash
   COACHING_MODE=guidance  # Change from 'suggestions'
   ```

2. **Restart backend:**
   ```bash
   python app.py
   ```

3. **Done!** Both events are now emitted:
   - `coaching_guidance` - New format
   - `suggestion` - Legacy format (backward compat)

## Files Modified

| File | What Changed |
|------|--------------|
| `config.py` | Added COACHING_SYSTEM_PROMPT, CALL_OBJECTIVES, COACHING_MODE |
| `services/claude_service.py` | Added 6 new methods for coaching guidance |
| `app.py` | Updated get_ai_suggestion(), added feature-flags endpoint |
| `.env` | Added COACHING_MODE=suggestions |

## New Methods

### claude_service.py
- `get_coaching_guidance()` - Main coaching method
- `_detect_call_stage()` - Detects opening/discovery/pitch/objection/close
- `_track_objectives()` - Tracks completed vs remaining objectives
- `_get_fallback_guidance()` - Returns safe defaults on errors

### app.py
- `convert_guidance_to_suggestion()` - Legacy format converter
- `get_feature_flags()` - API endpoint for feature flags

## Stage Detection

Automatically detects:
1. **Opening** - Initial contact ("hello", "calling from")
2. **Discovery** - Questions ("what", "how many", "challenge")
3. **Pitch** - Presenting ("we offer", "solution", "helps you")
4. **Objection** - Concerns ("expensive", "not interested")
5. **Close** - Commitment ("trial", "demo", "schedule")

## Objective Tracking

Tracks completion via keywords:
- ✅ **Completed** - Keywords found in conversation
- ⏳ **Remaining** - Keywords not yet mentioned

Example (Discovery stage):
- Qualify call volume
- Identify pain point
- Understand current solution

## Testing

Run the test suite:
```bash
python3 test_simple.py
```

Expected output:
```
✅ ALL TESTS PASSED
```

## API Endpoints

**Check current mode:**
```bash
curl http://localhost:5001/api/feature-flags
```

Response:
```json
{
  "coaching_mode": "suggestions",
  "guidance_version": "v1"
}
```

## Error Handling

All failures return **fallback guidance**:
- Generic direction based on detected stage
- Safe default questions
- Basic talking points
- No crashes, always returns valid data

## Performance

- Stage detection: **Instant** (local algorithm)
- Objective tracking: **Instant** (keyword matching)
- Claude API: **~1-2 seconds** (same as before)
- Fallback: **Instant** (no API call)

## Backward Compatibility

✅ **100% backward compatible**
- Old `get_suggestion()` method unchanged
- Dual event emission maintains existing frontend
- Feature flag allows instant rollback
- No breaking changes

## Next Steps

1. Frontend needs to listen for `coaching_guidance` events
2. Build new UI components for stage/objectives
3. Add toggle in settings for coaching mode
4. Test with real calls

## Questions?

- See `COACHING_IMPLEMENTATION.md` for full details
- Check `test_simple.py` for test cases
- Review `services/claude_service.py` for implementation
