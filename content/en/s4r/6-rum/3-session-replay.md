---
title: 3. Session Replay
weight: 3
---

In the **User Sessions** table the sessions, click on the top **Session ID** (it should be around 50 seconds, or longer). This will bring on the RUM Session view.

A session is a collection of traces that correspond to the actions a single user takes when interacting with an application over a period of time. By default, a session lasts until 15 minutes have passed from the last event captured in the session. The maximum session duration is 4 hours.

![RUM Session](../images/rum-session.png)

Towards the top of this view, you will see a button for RUM Session Replay {{% button icon="play" %}}Replay{{% /button %}}. RUM Session Replay allows you to replay the user session. This is a great way to see exactly what the user experienced. Click the button to start the replay.

![RUM Session](../images/rum-session-replay.png)

RUM Session Replay can redact information, by default text is redacted. You can also redact images (which has been done for this workshop example). This is useful if you are replaying a session that contains sensitive information. You can also change the playback speed and pause the replay.

When playing back the session, notice how the mouse movements are captured. This is useful to see where the user is focusing their attention.
