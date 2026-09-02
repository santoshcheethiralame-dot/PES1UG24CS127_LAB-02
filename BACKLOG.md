# Lab 2 — Agile Backlog

**Smart Lab Equipment & Slot Reservation Portal**
PES University — Dept. of CSE · Problem Statement #01
*Lab 2: Agile Backlog Creation & Sprint Simulation in Jira*

Source: the 5 functional and 2 nonfunctional requirements from Lab 1, plus UC-13
(View Lab Utilisation Report) from the Lab 1 use-case diagram.

Jira project: **Smart Lab Portal**, key **SLP**, Scrum, company-managed.

## Requirement-to-Epic traceability

| Lab 1 requirement | Epic |
|---|---|
| FR-001 Reserve slot on a calibrated instrument | Epic 1 — Slot Reservation & Availability |
| FR-002 Calibration events gate bookability | Epic 2 — Calibration Governance |
| FR-003 Token validation, check-out / check-in | Epic 3 — Equipment Custody |
| FR-004 Late strikes and third-strike suspension | Epic 4 — Late-Return Penalties |
| FR-005 Cancellation and waitlist recovery | Epic 5 — Cancellation & Waitlist |
| NFR-001 Race-free concurrent booking | Epic 6 — Access Control, Audit & Concurrency |
| NFR-002 RBAC and append-only audit log | Epic 6 — Access Control, Audit & Concurrency |
| UC-13 View Lab Utilisation Report | Epic 7 — Lab Utilisation Reporting |

## Epic 1: Slot Reservation & Availability

**Description:** Lets an authenticated student see live instrument availability and hold a
slot of at most 2 hours, up to 7 days ahead, on an instrument whose calibration is valid.

| Story | As a | I want to | So that | Priority | Points |
|---|---|---|---|---|---|
| **1.1** Real-Time Availability View | student | see live availability for every instrument across the next 7 days | I can pick a free slot without walking to the lab | High | 5 |
| **1.2** Reserve a Slot | student | reserve a slot of up to 2 hours on a calibrated instrument | the instrument is guaranteed free when I arrive | High | 8 |
| **1.3** Booking-Rule Enforcement | lab administrator | have requests over 120 minutes or more than 7 days ahead rejected | no one hoards scarce hardware | High | 3 |
| **1.4** Reservation Token Issue | student | receive a unique reservation token on confirmation | I can prove my booking at the issue counter | High | 3 |

## Epic 2: Calibration Governance

**Description:** Makes calibration state gate bookability rather than merely be displayed,
so no reading is ever taken on an out-of-calibration instrument.

| Story | As a | I want to | So that | Priority | Points |
|---|---|---|---|---|---|
| **2.1** Record Calibration Event | lab technician | record date performed, next-due date and certificate ID against an instrument | every instrument's calibration state is on record | High | 5 |
| **2.2** Auto-Withdraw Expired Instruments | faculty supervisor | have an instrument leave the bookable inventory the moment its next-due date passes | no reading is taken on an out-of-calibration instrument | High | 8 |
| **2.3** Notify Affected Reservation Holders | student | be told within 5 minutes if my future booking is voided by calibration expiry | I can rebook on another instrument in time | Medium | 5 |

## Epic 3: Equipment Custody

**Description:** Ties physical custody of an instrument to the booking record through token
validation and server-side check-out / check-in timestamps.

| Story | As a | I want to | So that | Priority | Points |
|---|---|---|---|---|---|
| **3.1** Validate Token at Issue | lab technician | validate the student's reservation token before handing over an instrument | only the rightful booker takes it | High | 5 |
| **3.2** Reject Invalid Tokens | lab technician | see expired, reused or wrong-instrument tokens rejected with a clear reason | I can refuse issue confidently at the counter | High | 3 |
| **3.3** Server-Side Custody Timestamps | auditor | have check-out and check-in timestamps stored server-side against the reservation | a late return can be proven from the record | High | 5 |

## Epic 4: Late-Return Penalties

**Description:** Implements the disciplinary rule — overdue computation, a 30-minute grace
window, strikes, and suspension on the third strike inside a rolling 30 days.

| Story | As a | I want to | So that | Priority | Points |
|---|---|---|---|---|---|
| **4.1** Compute Overdue at Check-In | lab technician | have overdue duration computed automatically at check-in | I never have to judge lateness by hand | High | 5 |
| **4.2** Grace Window and Strike | student | have a 30-minute grace window before a strike is recorded | a queue at the issue counter does not penalise me | High | 5 |
| **4.3** Third-Strike Suspension | faculty supervisor | have booking privileges suspended for 14 days on a third strike in 30 days | repeat offenders stop blocking lab capacity | High | 8 |
| **4.4** Penalty Notifications | student | be notified within a minute of a strike or a suspension | I am never surprised by a blocked booking | Medium | 3 |

## Epic 5: Cancellation & Waitlist

**Description:** Recovers scarce lab capacity from abandoned bookings instead of leaving
instruments idle.

| Story | As a | I want to | So that | Priority | Points |
|---|---|---|---|---|---|
| **5.1** Cancel a Reservation | student | cancel a reservation up to 2 hours before its start time | I am not penalised when my plans change | Medium | 3 |
| **5.2** Join a Waitlist | student | join the waitlist for a fully booked instrument-slot | I get a chance if someone cancels | Medium | 5 |
| **5.3** Sequential Waitlist Offer | waitlisted student | be offered a released slot in waitlist order with 30 minutes to accept | the offer is fair and does not stall on one person | Medium | 8 |
| **5.4** No-Show Marking | faculty supervisor | see unused, uncancelled reservations marked NO_SHOW | ghost bookings are visible in utilisation data | Low | 3 |

## Epic 6: Access Control, Audit & Concurrency

**Description:** The platform-integrity work behind NFR-001 and NFR-002 — role-based access,
an append-only evidence trail, and correct isolation on the contended reservation write.

| Story | As a | I want to | So that | Priority | Points |
|---|---|---|---|---|---|
| **6.1** Role-Based Access Control | lab technician | have calibration and penalty actions restricted to my role | students cannot alter their own records | High | 5 |
| **6.2** Append-Only Audit Log | auditor | have every reservation, calibration, custody and penalty event logged immutably with actor, action, timestamp and before/after state | a suspension can be contested with evidence | High | 8 |
| **6.3** Twelve-Month Audit Export | lab technician | export 12 months of the audit log as CSV | I can answer an external audit without developer help | Low | 3 |
| **6.4** Race-Free Concurrent Booking | student | have exactly one of many simultaneous requests for the same slot succeed, within 200 ms | double-booking is impossible rather than merely unlikely | High | 13 |

## Epic 7: Lab Utilisation Reporting

**Description:** Gives the Faculty Supervisor visibility of how lab capacity is actually used.

| Story | As a | I want to | So that | Priority | Points |
|---|---|---|---|---|---|
| **7.1** Utilisation Report | faculty supervisor | see booked versus actually used hours per instrument | I can find where lab capacity is being wasted | Medium | 5 |
| **7.2** Filter Utilisation by Period | faculty supervisor | filter utilisation by date range and department | I can justify new equipment purchases with evidence | Low | 3 |

## Sprint plan

Total backlog: **24 stories, 127 points**. Two one-week sprints do not consume a 127-point
backlog, and pretending otherwise is the mistake the burndown chart exists to expose. The
sprints below are sized to a nominal velocity of roughly 40 points per week.

### Sprint 1 — "Book a calibrated instrument end to end" (37 points)

| Story | Priority | Points |
|---|---|---|
| 1.1 Real-Time Availability View | High | 5 |
| 1.2 Reserve a Slot | High | 8 |
| 1.3 Booking-Rule Enforcement | High | 3 |
| 1.4 Reservation Token Issue | High | 3 |
| 2.1 Record Calibration Event | High | 5 |
| 2.2 Auto-Withdraw Expired Instruments | High | 8 |
| 6.1 Role-Based Access Control | High | 5 |

**Sprint goal:** a student can find and hold a slot on an instrument that is provably in
calibration, and only a technician can change calibration data.

### Sprint 2 — "Custody and consequences" (39 points)

| Story | Priority | Points |
|---|---|---|
| 3.1 Validate Token at Issue | High | 5 |
| 3.2 Reject Invalid Tokens | High | 3 |
| 3.3 Server-Side Custody Timestamps | High | 5 |
| 4.1 Compute Overdue at Check-In | High | 5 |
| 4.2 Grace Window and Strike | High | 5 |
| 4.3 Third-Strike Suspension | High | 8 |
| 6.2 Append-Only Audit Log | High | 8 |

**Sprint goal:** an instrument can only be issued against a valid token, and a late return
produces a strike that is defensible from the audit log.

### Remaining backlog after Sprint 2 (51 points)

2.3 (5), 4.4 (3), 5.1 (3), 5.2 (5), 5.3 (8), 5.4 (3), 6.3 (3), 6.4 (13), 7.1 (5), 7.2 (3).

## Why these story points

Fibonacci values track complexity, effort and uncertainty together, and the widening gaps
stop the team arguing over a distinction it cannot really make.

| Points | Meaning here | Example |
|---|---|---|
| 3 | A rule or a form over data that already exists. | 1.3 rejecting an over-length booking |
| 5 | One screen or one service, well understood. | 2.1 recording a calibration event |
| 8 | Touches several components, or has real state to get right. | 4.3 rolling 30-day strike window |
| 13 | Carries genuine technical risk and needs load evidence. | 6.4 serialisable isolation under 200 concurrent requests |
