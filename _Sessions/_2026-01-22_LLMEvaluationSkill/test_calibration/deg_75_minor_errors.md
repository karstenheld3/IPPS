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
         |  2. Validate login                    |
         |                                  [DB] |
         |                                       |
         |  3. Create token                      |
         |<--------------------------------------|
         |                                       |
         |  4. Save token                        |
         |  [BROWSER]                            |
         |                                       |
         |  5. Go to dashboard                   |
         |-------------------------------------->|
         |                                       |

[S] = Server     [U] = User     [DB] = Database
Result: Login complete
```

<transcription_notes>
- Mode: Structural
- Dimensions: 60x25 characters
- ASCII captures: Sequence diagram, arrows, boxes
- ASCII misses: Colors, icons
- Colors:
  - Blue - user box
  - Green - server box
  - Yellow - database
  - Gray - arrows
- Layout: Left-to-right sequence
- Details: Numbered steps
- Data: 5 steps
- Reconstruction hint: Server is larger
</transcription_notes>
</transcription_image>
