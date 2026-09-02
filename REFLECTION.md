# Lab 2 — Reflection

**Smart Lab Equipment & Slot Reservation Portal**
PES University — Dept. of CSE · Problem Statement #01

Sprint 1 ran from 02/Sep/26 12:11 PM, 7 work items, 37 story points, all completed.
Sprint 2 ran from 02/Sep/26 12:24 PM, 7 work items, 39 story points, all completed.
Both sprints were configured with a one-week time box ending 09/Sep/26. 10 work items and
51 story points remain in the backlog.

## 1. Did your estimations reflect the actual effort?

Partly, and the places where they did not are the informative ones. The estimates that held
were the 3s and 5s — work like recording a calibration event or rejecting an over-length
booking, where the shape of the task was obvious before it started. The estimates that were
least trustworthy were the 8s and the single 13.

Story 6.4 (race-free concurrent booking) was sized at 13 precisely because nobody could
describe how it would be done, only what it had to achieve: exactly one winner out of 200
concurrent requests, p95 under 200 ms. That is uncertainty, not volume, and the Fibonacci
gap between 8 and 13 is where a team is meant to record it. Story 4.3 (third-strike
suspension) looked like an 8 for the same reason — the rolling 30-day window, the 14-day
block and two notifications are three separate pieces of state that all have to agree.

In this simulation the "actual effort" is a transition on a board rather than work done, so
the honest answer is that the estimates were never tested against real implementation. What
the exercise did test was whether the relative ordering was defensible, and it was: the
stories we called 8s are the ones we would still be least confident committing to.

## 2. Was your backlog well-prioritized?

Yes, and the test is dependency rather than desire. Every High-priority story is one that
something else is blocked on:

- Nothing can be checked out until a reservation exists, so Epic 1 comes first.
- A reservation on an uncalibrated instrument is worthless, so Epic 2 must land alongside it.
- The late-return rule in Epic 4 has no evidence to act on without the custody timestamps in
  Epic 3, which is why Epic 4 could not be pulled forward however visible the feature is.
- Role-based access control (6.1) was pulled into Sprint 1 rather than left with the rest of
  Epic 6, because letting students write calibration records even once during development is
  the kind of thing that quietly stays broken.

The Medium and Low items are genuine capacity recovery and reporting — Epics 5 and 7. They
improve how well the lab is used; they are not what makes the portal correct. Story 5.4
(NO_SHOW marking) and 6.3 (audit export) are Low because a human can do either by hand for
a term without anyone suffering.

The one item priority does not capture well is 6.4. It is High and it is a 13, and it sits
outside both sprints — which is uncomfortable, and correct. It is the largest technical risk
in the project and it should be attacked with a spike before being committed to a sprint.

## 3. How did your simulated sprint align with your plan?

Sprint 1 was planned at 37 points across 7 stories and Sprint 2 at 39 points across 7, out
of a 127-point backlog. Both sprints closed with every committed story in Done — Jira's
completion dialog reported "7 completed work items. That's all of them" for each — so on
paper the plan was met exactly, 76 of 76 committed points delivered.

That alignment is an artefact of the simulation, not a result. Moving a card from To Do to
In Progress to Done in the same session removes everything that normally causes a sprint to
miss: a dependency discovered late, an estimate that was wrong by a factor of two, a story
that turns out to need a decision nobody has authority to make. A real Sprint 1 on this
backlog would most likely have carried 2.2 (auto-withdraw expired instruments) into Sprint 2,
because it is the first story that touches both the scheduler and the inventory view.

What the plan did get right is the shape: two sprints did not clear the backlog and were
never scoped to. 51 points remain after Sprint 2. How many further sprints that represents
is not something this exercise can answer, for the reason set out in answer 4 — no real
velocity was measured, so any figure quoted here would be invented.

## 4. What insights did the burndown chart give about your team's capacity?

Both charts have the same shape, and it is not the shape a healthy sprint produces. The red
Remaining Values line falls vertically from 37 points (Sprint 1) and 39 points (Sprint 2) to
zero within minutes of the sprint starting, then runs flat along the zero axis for the rest
of the one-week time box while the grey guideline descends slowly to meet it on 09/Sep. The
line is not below the guideline because the team was fast; it is below the guideline because
seven days of planned work were transacted in about ten minutes of wall-clock time.

The first honest insight is therefore about the instrument rather than the team: a burndown
chart measures work against elapsed time, so it says nothing at all when the elapsed time is
fake. Neither chart supports a velocity claim. The 76 points delivered here are not evidence
that this team can deliver 38 points a week, and using them to forecast the remaining 51
points in the backlog would be a fabricated number dressed up as a measurement.

What the charts do show correctly is the relationship between commitment and time box. Both
sprints were committed at roughly half the backlog's weekly capacity and both emptied
immediately, which in a real sprint would read as severe under-commitment — the signature
Atlassian describes as a team that consistently finishes early and is not taking on enough
work. The corrective in a real team would be to raise the commitment until the remaining
line tracks the guideline instead of collapsing away from it.

The charts also make scope honest in a way an issue count does not. Because the axis is
story points rather than work items, closing three 3-point stories moves the line less than
closing one 8-point story, so a sprint can look busy on the board and still be behind on the
chart. That divergence is the thing the burndown exists to expose, and it is the reason the
estimation statistic must be set to Story Points rather than Issue Count before the chart is
read at all.
