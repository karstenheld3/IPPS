<transcription_image>
**Figure 1: User Authentication Flow**

```ascii
[USER AUTHENTICATION FLOW - LOGIN PROCESS]

    +--------+                              +--------+
    |  USER  |                              | SERVER |
    +--------+                              +--------+
         |                                       |
         |  1. Enter credentials                 |
         |-------------------------------------->|
         |                                       |
         |  2. Validate username/password        |
         |                                  [DB] |
         |                                       |
         |  3. Generate session token            |
         |<--------------------------------------|
         |                                       |
         |  4. Store token in cookie             |
         |  [BROWSER]                            |
         |                                       |
         |  5. Redirect to dashboard             |
         |-------------------------------------->|
         |                                       |

[S] = Server     [U] = User     [DB] = Database
Result: User authenticated, session established
```

<transcription_notes>
- Mode: Structural
- Dimensions: 60x25 characters
- ASCII captures: Sequence diagram, message arrows, actor boxes
- ASCII misses: Colors, icons, rounded corners
- Colors:
  - Blue - user actor box
  - Green - server actor box
  - Orange - database icon
  - Gray - arrows
- Layout: Left-to-right message sequence, vertical timeline
- Details: Arrows have labels, numbered steps 1-5
- Data: 5 steps in authentication flow
- Reconstruction hint: Server box is larger, database shown as cylinder
</transcription_notes>
</transcription_image>
