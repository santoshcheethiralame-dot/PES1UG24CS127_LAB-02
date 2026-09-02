"""Build the Lab 2 submission PDFs.

    Lab2_Deliverables.pdf   -- Epics, User Stories, story points, sprint results
                               and both burndown charts
    Lab2_Reflection.pdf     -- the four reflection answers, from REFLECTION.md

Chrome headless is used for HTML -> PDF; it refuses to write into the home
directory here, so the PDF is produced in a temp directory and copied back.
"""

import base64
import io
import os
import re
import shutil
import subprocess
import tempfile

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOTS = os.path.join(ROOT, "screenshots")
TMP = tempfile.mkdtemp(prefix="lab2_")

EPICS = [
    ("Epic 1: Slot Reservation & Availability", "FR-001",
     "Lets an authenticated student see live instrument availability and hold a slot of at "
     "most 2 hours, up to 7 days ahead, on an instrument whose calibration is valid.",
     [("1.1", "Real-Time Availability View", "student",
       "see live availability for every instrument across the next 7 days",
       "I can pick a free slot without walking to the lab", "High", 5),
      ("1.2", "Reserve a Slot", "student",
       "reserve a slot of up to 2 hours on a calibrated instrument",
       "the instrument is guaranteed free when I arrive", "High", 8),
      ("1.3", "Booking-Rule Enforcement", "lab administrator",
       "have requests over 120 minutes or more than 7 days ahead rejected",
       "no one hoards scarce hardware", "High", 3),
      ("1.4", "Reservation Token Issue", "student",
       "receive a unique reservation token on confirmation",
       "I can prove my booking at the issue counter", "High", 3)]),
    ("Epic 2: Calibration Governance", "FR-002",
     "Makes calibration state gate bookability rather than merely be displayed, so no "
     "reading is ever taken on an out-of-calibration instrument.",
     [("2.1", "Record Calibration Event", "lab technician",
       "record date performed, next-due date and certificate ID against an instrument",
       "every instrument's calibration state is on record", "High", 5),
      ("2.2", "Auto-Withdraw Expired Instruments", "faculty supervisor",
       "have an instrument leave the bookable inventory the moment its next-due date passes",
       "no reading is taken on an out-of-calibration instrument", "High", 8),
      ("2.3", "Notify Affected Reservation Holders", "student",
       "be told within 5 minutes if my future booking is voided by calibration expiry",
       "I can rebook on another instrument in time", "Medium", 5)]),
    ("Epic 3: Equipment Custody", "FR-003",
     "Ties physical custody of an instrument to the booking record through token validation "
     "and server-side check-out / check-in timestamps.",
     [("3.1", "Validate Token at Issue", "lab technician",
       "validate the student's reservation token before handing over an instrument",
       "only the rightful booker takes it", "High", 5),
      ("3.2", "Reject Invalid Tokens", "lab technician",
       "see expired, reused or wrong-instrument tokens rejected with a clear reason",
       "I can refuse issue confidently at the counter", "High", 3),
      ("3.3", "Server-Side Custody Timestamps", "auditor",
       "have check-out and check-in timestamps stored server-side against the reservation",
       "a late return can be proven from the record", "High", 5)]),
    ("Epic 4: Late-Return Penalties", "FR-004",
     "Implements the disciplinary rule: overdue computation, a 30-minute grace window, "
     "strikes, and suspension on the third strike inside a rolling 30 days.",
     [("4.1", "Compute Overdue at Check-In", "lab technician",
       "have overdue duration computed automatically at check-in",
       "I never have to judge lateness by hand", "High", 5),
      ("4.2", "Grace Window and Strike", "student",
       "have a 30-minute grace window before a strike is recorded",
       "a queue at the issue counter does not penalise me", "High", 5),
      ("4.3", "Third-Strike Suspension", "faculty supervisor",
       "have booking privileges suspended for 14 days on a third strike in 30 days",
       "repeat offenders stop blocking lab capacity", "High", 8),
      ("4.4", "Penalty Notifications", "student",
       "be notified within a minute of a strike or a suspension",
       "I am never surprised by a blocked booking", "Medium", 3)]),
    ("Epic 5: Cancellation & Waitlist", "FR-005",
     "Recovers scarce lab capacity from abandoned bookings instead of leaving instruments "
     "idle.",
     [("5.1", "Cancel a Reservation", "student",
       "cancel a reservation up to 2 hours before its start time",
       "I am not penalised when my plans change", "Medium", 3),
      ("5.2", "Join a Waitlist", "student",
       "join the waitlist for a fully booked instrument-slot",
       "I get a chance if someone cancels", "Medium", 5),
      ("5.3", "Sequential Waitlist Offer", "waitlisted student",
       "be offered a released slot in waitlist order with 30 minutes to accept",
       "the offer is fair and does not stall on one person", "Medium", 8),
      ("5.4", "No-Show Marking", "faculty supervisor",
       "see unused, uncancelled reservations marked NO_SHOW",
       "ghost bookings are visible in utilisation data", "Low", 3)]),
    ("Epic 6: Access Control, Audit & Concurrency", "NFR-001, NFR-002",
     "Platform integrity: role-based access, an append-only evidence trail, and correct "
     "isolation on the contended reservation write.",
     [("6.1", "Role-Based Access Control", "lab technician",
       "have calibration and penalty actions restricted to my role",
       "students cannot alter their own records", "High", 5),
      ("6.2", "Append-Only Audit Log", "auditor",
       "have every reservation, calibration, custody and penalty event logged immutably "
       "with actor, action, timestamp and before/after state",
       "a suspension can be contested with evidence", "High", 8),
      ("6.3", "Twelve-Month Audit Export", "lab technician",
       "export 12 months of the audit log as CSV",
       "I can answer an external audit without developer help", "Low", 3),
      ("6.4", "Race-Free Concurrent Booking", "student",
       "have exactly one of many simultaneous requests for the same slot succeed, "
       "within 200 ms",
       "double-booking is impossible rather than merely unlikely", "High", 13)]),
    ("Epic 7: Lab Utilisation Reporting", "UC-13",
     "Gives the Faculty Supervisor visibility of how lab capacity is actually used.",
     [("7.1", "Utilisation Report", "faculty supervisor",
       "see booked versus actually used hours per instrument",
       "I can find where lab capacity is being wasted", "Medium", 5),
      ("7.2", "Filter Utilisation by Period", "faculty supervisor",
       "filter utilisation by date range and department",
       "I can justify new equipment purchases with evidence", "Low", 3)]),
]

SPRINT1 = ["1.1", "1.2", "1.3", "1.4", "2.1", "2.2", "6.1"]
SPRINT2 = ["3.1", "3.2", "3.3", "4.1", "4.2", "4.3", "6.2"]

CSS = """
@page { size: A4; margin: 16mm 14mm; }
body { font: 10.5pt/1.45 Georgia, 'Times New Roman', serif; color: #1a1a1a; }
h1 { font-size: 19pt; margin: 0 0 2pt; color: #12365c; }
h2 { font-size: 13pt; margin: 22pt 0 6pt; color: #12365c;
     border-bottom: 1px solid #c8d4e0; padding-bottom: 3pt; }
h3 { font-size: 11pt; margin: 14pt 0 4pt; color: #12365c; }
.sub { color: #555; font-size: 9.5pt; margin: 0 0 4pt; }
.desc { font-style: italic; color: #333; margin: 2pt 0 6pt; }
table { border-collapse: collapse; width: 100%; font-size: 8.8pt; margin-bottom: 4pt; }
th { background: #eef3f8; text-align: left; }
th, td { border: 1px solid #b9c7d6; padding: 3.5pt 5pt; vertical-align: top; }
td.n, th.n { text-align: center; white-space: nowrap; }
.tot { font-size: 9pt; color: #444; margin: 0 0 10pt; }
img { width: 100%; border: 1px solid #b9c7d6; margin-top: 4pt; }
.pb { page-break-before: always; }
.chart { page-break-inside: avoid; }
.goal { background: #f4f7fa; border-left: 3px solid #12365c;
        padding: 5pt 8pt; margin: 5pt 0 8pt; font-size: 9.5pt; }
"""


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def img_tag(name):
    with open(os.path.join(SHOTS, name), "rb") as fh:
        b64 = base64.b64encode(fh.read()).decode()
    return '<img src="data:image/png;base64,%s">' % b64


def epic_section(epic):
    title, trace, desc, stories = epic
    rows = []
    for sid, name, actor, want, benefit, prio, pts in stories:
        sprint = "Sprint 1" if sid in SPRINT1 else "Sprint 2" if sid in SPRINT2 else "Backlog"
        rows.append(
            "<tr><td><b>%s</b> %s</td><td>As a %s, I want to %s, so that %s.</td>"
            "<td class='n'>%s</td><td class='n'>%s</td><td class='n'>%s</td></tr>"
            % (sid, esc(name), esc(actor), esc(want), esc(benefit), prio, pts, sprint))
    total = sum(s[6] for s in stories)
    return (
        "<h3>%s</h3><p class='sub'>Traces to %s</p><p class='desc'>%s</p>"
        "<table><tr><th>Story</th><th>User story</th><th class='n'>Priority</th>"
        "<th class='n'>Points</th><th class='n'>Sprint</th></tr>%s</table>"
        "<p class='tot'>%d stories, %d story points.</p>"
        % (esc(title), trace, esc(desc), "".join(rows), len(stories), total))


def html():
    epics = "".join(epic_section(e) for e in EPICS)
    return """<!doctype html><meta charset="utf-8"><style>%s</style>
<h1>Lab 2 &mdash; Agile Backlog &amp; Sprint Simulation</h1>
<p class="sub">Smart Lab Equipment &amp; Slot Reservation Portal &middot;
PES University, Dept. of CSE &middot; Problem Statement #01</p>
<p class="sub">Jira project <b>Smart Lab Portal</b> (key SLP), Scrum, company-managed.
Backlog derived from the Lab 1 requirements table.</p>

<h2>1. Epics and User Stories</h2>
<p>Seven Epics covering the five functional requirements, both nonfunctional requirements
and use case UC-13 from Lab 1. Twenty-four User Stories, 127 story points, estimated on the
Fibonacci scale.</p>
%s

<h2 class="pb">2. Sprint results</h2>
<table>
<tr><th>Sprint</th><th>Started</th><th class="n">Items</th><th class="n">Points</th>
<th class="n">Completed</th></tr>
<tr><td>SLP Sprint 1</td><td>02/Sep/26 12:11 PM</td><td class="n">7</td>
<td class="n">37</td><td class="n">7 of 7</td></tr>
<tr><td>SLP Sprint 2</td><td>02/Sep/26 12:24 PM</td><td class="n">7</td>
<td class="n">39</td><td class="n">7 of 7</td></tr>
<tr><td>Remaining backlog</td><td>&mdash;</td><td class="n">10</td>
<td class="n">51</td><td class="n">&mdash;</td></tr>
</table>
<div class="goal"><b>Sprint 1 goal.</b> A student can find and hold a slot on an instrument
that is provably in calibration, and only a technician can change calibration data.</div>
<div class="goal"><b>Sprint 2 goal.</b> An instrument can only be issued against a valid
token, and a late return produces a strike that is defensible from the audit log.</div>
<p>Both sprints were time-boxed to one week ending 09/Sep/26. Epics 1&ndash;4 closed
completely, Epic 6 partially (13 of 29 points), Epics 5 and 7 untouched.</p>
%s

<h2 class="pb">3. Burndown charts</h2>
<p>In both charts the Remaining Values line falls from the committed total to zero within
minutes of the sprint starting and then runs flat along the zero axis for the rest of the
one-week time box, while the guideline descends slowly to meet it on 09/Sep. The line sits
below the guideline not because the team was fast but because seven days of planned work
were transacted in about ten minutes of elapsed time, so neither chart supports a velocity
claim. Read as a real sprint, the shape is the signature of severe under-commitment.</p>
<div class="chart"><h3>SLP Sprint 1 &mdash; 37 story points</h3>%s</div>
<div class="chart"><h3>SLP Sprint 2 &mdash; 39 story points</h3>%s</div>
""" % (CSS, epics, img_tag("08-epic-progress.png"),
       img_tag("06-burndown-sprint1.png"), img_tag("07-burndown-sprint2.png"))


def inline(t):
    t = esc(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    return t


def reflection_html():
    """Render REFLECTION.md: h1, h2, paragraphs and bullet lists, which is
    everything that file uses."""
    raw = io.open(os.path.join(ROOT, "REFLECTION.md"), encoding="utf-8").read()
    blocks, buf = [], []
    for line in raw.splitlines():
        if line.strip():
            buf.append(line)
        elif buf:
            blocks.append(buf)
            buf = []
    if buf:
        blocks.append(buf)

    out = []
    for block in blocks:
        if block[0].startswith("# "):
            out.append("<h1>%s</h1>" % inline(block[0][2:]))
            for extra in block[1:]:
                out.append("<p class='sub'>%s</p>" % inline(extra))
        elif block[0].startswith("## "):
            out.append("<h2>%s</h2>" % inline(block[0][3:]))
        elif block[0].startswith("- "):
            items, cur = [], []
            for line in block:
                if line.startswith("- "):
                    if cur:
                        items.append(" ".join(cur))
                    cur = [line[2:].strip()]
                else:
                    cur.append(line.strip())
            if cur:
                items.append(" ".join(cur))
            out.append("<ul>%s</ul>"
                       % "".join("<li>%s</li>" % inline(i) for i in items))
        else:
            out.append("<p>%s</p>" % inline(" ".join(l.strip() for l in block)))

    extra_css = "li { margin-bottom: 4pt; } ul { margin: 4pt 0 8pt; padding-left: 16pt; }"
    return ('<!doctype html><meta charset="utf-8"><style>%s %s</style>%s'
            % (CSS, extra_css, "".join(out)))


def to_pdf(page_html, name):
    src = os.path.join(TMP, name.replace(".pdf", ".html"))
    dst = os.path.join(TMP, name)
    with open(src, "w", encoding="utf-8") as fh:
        fh.write(page_html)
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    "--print-to-pdf=" + dst,
                    "file:///" + src.replace("\\", "/").replace(" ", "%20")],
                   check=False, capture_output=True)
    if not os.path.exists(dst):
        raise SystemExit("Chrome failed to write " + name)
    out = os.path.join(ROOT, name)
    shutil.copy(dst, out)
    print("wrote", out, os.path.getsize(out), "bytes")


def main():
    to_pdf(html(), "Lab2_Deliverables.pdf")
    to_pdf(reflection_html(), "Lab2_Reflection.pdf")


if __name__ == "__main__":
    main()
