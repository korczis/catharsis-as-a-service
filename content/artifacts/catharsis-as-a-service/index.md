+++
title = "Catharsis as a Service™"
description = "A visual study of collective catharsis modelled as a service transaction: repetition, synchronization and discharge produce temporary relief while the underlying condition stays unchanged."
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

A visual study that presents collective euphoria at first glance and a diagnosis of it at second.

Photography of an industrial rave, brutalist typography and a Prismatic telemetry overlay share one surface. The crowd gets its release, the system logs a successful response, and the underlying condition stays exactly where it was.

## First glance, second glance

Seen from across a street, it is a campaign: a red-lit stage, a sea of raised hands, a headline big enough to promise something. That reading is intended and it is not a trap. The night it advertises is real, and so is the relief.

Seen up close, the poster starts filing a report. The overlay names an input, a process and an output. The status line reads as a success: `200 OK`. Underneath it, one field refuses to cooperate: `problem_solved: false`.

## Why an API

Service language is how we describe things meant to be consumed on demand, repeatably, with a guaranteed response. Putting catharsis behind an endpoint makes one uncomfortable property visible: the transaction can succeed completely without the request ever being resolved. The endpoint does exactly what it promises. The promise was just smaller than the need.

## Relief is not resolution

The artifact does not argue that dancing is useless or that collective release is fake. Repetition, synchronization and discharge are old and effective human technology. The claim is narrower: a temporary state transition and a removed root cause are different outcomes, and it is worth being able to tell which one you received.

## Why the telemetry is conceptual

Every metric on this page is an artistic value. Nothing is measured, collected or inferred about anyone who visits, and there is no analytics script to contradict that. A piece about instrumenting people should not quietly instrument its own audience.

## How to use it

- **As a mirror:** after the next night that felt like it fixed something, ask which field it actually changed.
- **As a conversation starter:** the raw response is short enough to quote and specific enough to disagree with.
- **As a design reference:** euphoria and diagnosis on one surface, with neither cancelling the other.
