# KABOB Example 01: IndustryFeatureArticle

Industry feature article written `using KABOB as SECTOR-COLUMNIST`. The company, people, association, survey, and all figures are fictional.

## Context

An industry newsletter wants a 900-word feature on why mid-sized manufacturers struggle to benefit from predictive maintenance sensors. Readers are plant managers and operations directors who read voluntarily and want a useful mental model, not a vendor pitch.

## Document

```markdown
# The Pump That Warned Nobody: Why Sensors Alone Do Not Prevent Downtime

At 06:40 on a Tuesday in March, the main coolant pump at Nordtal Pumps stopped turning. Jane Smith, the plant manager, had installed vibration sensors on that pump eleven months earlier. The sensor had recorded rising vibration for nine days.

Nobody had looked at the data. The dashboard sat on a laptop in the maintenance office, and the alert threshold was still set to the vendor's default. The line stood still for 14 hours; replacement parts and lost output cost 61,000 EUR.

Smith told us she spent the afternoon asking one question: what had she actually bought?

Her plant is a typical member of the regional manufacturers' association: 140 employees, machines between 8 and 25 years old, one maintenance team of six. In the association's 2026 survey of 312 such plants, 58% had installed condition sensors, but only 23% said the sensors had reduced unplanned stops. The gap between buying sensors and avoiding downtime is the subject of this article.

## Sensors are cheap; interpreting their data is not

A vibration sensor for a pump costs between 200 and 600 EUR. The cost that plants underestimate is attention. An engineer at the association's technical committee explained that each machine needs its own alert threshold, because a 20-year-old pump vibrates differently from a new one. Setting thresholds for 80 machines takes roughly three weeks of a senior technician's time.

Smith's plant had budgeted for hardware, not for those three weeks. In the survey, plants that assigned a named person to review sensor alerts weekly were three times more likely to report fewer stops.

## The data has to reach the person holding the wrench

Industrial history has seen this pattern before. Early electric motors spent decades driving factories still laid out for steam engines, and productivity rose only after the floors were redesigned around them. Sensors repeat the lesson: the value appears only when the alert lands on the phone of the technician on shift, not in a dashboard on an office laptop.

At Nordtal, Smith moved alerts to the shift supervisors' phones and cut the alert list from 340 messages a week to 25 by tuning thresholds machine by machine.

## Not every plant should start now

The survey also shows the limit. Sites with fewer than 20 rotating machines rarely recovered the sensor and tuning cost within three years. For them, scheduled inspections with a handheld vibration meter remain cheaper.

Last month, the same coolant pump at Nordtal began to vibrate again. This time the alert reached the supervisor's phone nine days before the predicted failure, and the bearing was changed during a planned Saturday shift. The pump, Smith says, had been warning them all along; now somebody is listening.
```

## Key Decisions

- Anecdote of 3 paragraphs ending at Smith's question: the tension is open when the nut graf explains the trend (KABOB-ST-01)
- Nut graf in paragraph 4 with representativeness ("a typical member") and survey numbers (KABOB-ST-02, KABOB-EV-01, KABOB-CT-02)
- Body alternates evidence types: cost data, expert explanation, survey comparison, historical parallel, return to the case (KABOB-CT-03)
- Counterpoint section for small plants: prevents the feature from reading as a sensor sales pitch (KABOB-EV-03)
- Kicker returns to the same pump and shows the changed outcome, without a new argument (KABOB-ST-03, KABOB-CT-04)
- Persona `SECTOR-COLUMNIST` (Narrative 6, Humor 4): one trait, One-Sentence Historical Parallel (electric motors and factory layout), placed alone in its paragraph; the anecdote contains no invented weather, thoughts, or dialogue
