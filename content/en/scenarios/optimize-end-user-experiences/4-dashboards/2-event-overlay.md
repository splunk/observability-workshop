---
title: Events in context with chart data
linkTitle: 2. Event overlay
weight: 2
hidden: false
---
Seeing the visualization of our KPIs is great. What's better? KPIs in context with events! [Overlaying events on a dashboard](https://docs.splunk.com/observability/en/data-visualization/dashboards/dashboards-add.html#overlay-event-markers-on-charts-in-a-dashboard) can help us more quickly understand if an event like a deployment caused a change in metrics, for better or worse.

1. Your instructor will push a condition change to the workshop application. Click the event marker on any of your dashboard charts to see more details.
![condition change event](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-04-02/d2dac271-0a85-46b9-b46d-e13e4e759f60/user_cropped_screenshot.jpeg?tl_px=0,0&br_px=1385,827&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=921,460)

1. In the dimensions, we can see more details about this specific event. If we click the event record, we can mark for deletion if needed.
![event record](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-04-02/55a9d0dc-5a44-496d-b44f-60f681b5576b/ascreenshot.jpeg?tl_px=692,626&br_px=2412,1587&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=524,277)
![event details](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-04-02/ee20c9d9-9ea4-4302-af4a-73c8c24df029/user_cropped_screenshot.jpeg?tl_px=13,12&br_px=1733,974&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=832,324)

1. We can also see a history of events in the event feed by clicking the icon on the top right of the screen, and selecting Event feed.
![event feed](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-04-02/7e7317f6-04b4-404e-8e17-78cf3e319ef9/user_cropped_screenshot.jpeg?tl_px=0,0&br_px=1471,785&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=1056,84)

1. Again, we can see details about recent events in this feed.
![event details](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-04-02/66c575d0-da25-4e4d-bd3b-78b6ce777ef4/user_cropped_screenshot.jpeg?tl_px=41,0&br_px=1760,877&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=815,346)

1. We can also add new events in the GUI or [via API](https://dev.splunk.com/observability/reference/api/ingest_data/latest#endpoint-send-events). To add a new event in the GUI, click the New event button.
![GUI add event button](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-04-02/f6707f30-af0e-4aa0-aa60-8272a601c0f7/user_cropped_screenshot.jpeg?tl_px=50,0&br_px=1770,852&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=895,179)

1. Name your event with your team name, initials, and what kind of event it is (deployment, campaign start, etc). Choose a timestamp, or leave as-is to use the current time, and click "Create".
![create event form](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-04-02/1280542f-4446-4b9d-8a46-d524e0319572/user_cropped_screenshot.jpeg?tl_px=0,125&br_px=1567,1087&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=858,513)

1. Now, we need to make sure our new event is overlaid in this dashboard. Wait a minute or so (refresh the page if needed) and then search for the event in the Event overlay field.
![overlay event](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-04-02/ca2b0b08-a369-473d-ad32-3926bfca934c/user_cropped_screenshot.jpeg?tl_px=0,0&br_px=1601,810&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=408,229)

1. If your event is within the dashboard time window, you should now see it overlaid in your charts. Click "Save" to make sure your event overlay is saved to your dashboard!
![save dashboard](https://ajeuwbhvhr.cloudimg.io/colony-recorder.s3.amazonaws.com/files/2024-04-02/21dc9ffa-4b33-46b1-81e2-6204924b7ec5/user_cropped_screenshot.jpeg?tl_px=0,0&br_px=1432,732&force_format=png&width=1120.0&wat=1&wat_opacity=0.7&wat_gravity=northwest&wat_url=https://colony-recorder.s3.us-west-1.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=868,67)

{{% notice title="Keep in mind" style="primary"  icon="lightbulb" %}}
Want to add context to that bug ticket, or show your manager how your change improved app performance? Seeing observability data in context with events not only helps with troubleshooting, but also helps us communicate with other teams. 
{{% /notice %}}
