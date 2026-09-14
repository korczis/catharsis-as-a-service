+++
title = "Catharsis as a Service™"
description = "A festival poster that sells euphoria at first glance and diagnoses it at second: repetition, synchronization, discharge, temporary relief."
date = 2026-09-14
weight = 1

[extra]
title_lines = ["Catharsis", "as a Service™"]
kicker = "Human Systems Diagnostics"
subtitle = "Emotional State Transition Endpoint"
endpoint = "POST /v1/catharsis"
status = "200 OK"
poster = "assets/catharsis-as-a-service.png"
poster_alt = "Catharsis as a Service poster showing a monumental red-lit industrial rave stage, a dense crowd and a central anonymous figure beneath diagnostic telemetry."
sidebar_left = ["Observe", "Connect", "Reason", "Act", "Repeat"]
sidebar_right = ["Curiosity", "Evidence", "Context", "Perspective", "Better questions"]
raw = '''
{
  "endpoint": "/v1/catharsis",
  "method": "POST",
  "input": {
    "emotional_state": "unresolved"
  },
  "process": [
    "repetition",
    "synchronization",
    "discharge"
  ],
  "output": {
    "relief": "temporary"
  },
  "status": 200,
  "problem_solved": false
}'''

[extra.diagnostic]
label = "State transition"
heading = ["The endpoint works.", "The problem remains."]
input_label = "Input"
input = "unresolved emotional state"
process_label = "Process"
process = ["repetition", "synchronization", "discharge"]
output_label = "Output"
output = "temporary relief"
problem_solved = false
status_cells = [
  { label = "HTTP status", value = "200 OK", alert = false },
  { label = "State transition", value = "Complete", alert = false },
  { label = "Relief", value = "Temporary", alert = false },
  { label = "Problem status", value = "Unresolved", alert = true },
]

[extra.crowd]
label = "Crowd as system"
heading = "A crowd does not solve the unresolved state."
sequence = ["Individual signals", "Synchronization", "Collective oscillation", "Discharge", "Temporary equilibrium"]
body = ["It synchronizes it.", "For a brief interval, individual noise becomes collective rhythm."]

[extra.observability]
label = "Observability"
heading = "More data. Fewer illusions."
disclaimer = "Conceptual metrics. These are artistic values, not biometric measurements. Nothing on this page measures anyone."
metrics = [
  { label = "Input state", value = "unresolved", level = 100, alert = true },
  { label = "Coherence", value = "rising", level = 64, alert = false },
  { label = "Synchronization", value = "high", level = 88, alert = false },
  { label = "Amplitude", value = "high", level = 94, alert = false },
  { label = "Discharge", value = "detected", level = 100, alert = false },
  { label = "Relief", value = "temporary", level = 36, alert = false },
  { label = "Root cause", value = "unchanged", level = 100, alert = true },
]

[extra.terminal]
label = "Endpoint"
heading = "Same people. Different patterns."
command = '''$ curl -X POST /v1/catharsis \
    -d emotional_state=unresolved'''
response = '''HTTP/1.1 200 OK

{
  "relief": "temporary",
  "problem_solved": false
}'''
mantra = ["Rave.", "Release.", "Reset.", "Repeat."]
closing = ["Some problems can't be solved.", "They can only be danced through."]
+++

A festival poster that sells euphoria at first glance and diagnoses it at second.

Industrial rave photography, brutalist type and a Prismatic telemetry overlay share one surface. The crowd gets its release, the system logs a successful response, and the underlying condition stays exactly where it was.
