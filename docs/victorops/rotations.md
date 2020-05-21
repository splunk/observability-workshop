# Configure Rotations

Navigate to the `Rotations` tab on the `Teams` sub menu, you should have no existing Rotations so we need to create some. The 1st Rotation you will create is for a follow the sun support pattern where the members of each shift provide cover during their normal working hours within their time zone.  The 2nd will be a Rotation used to provide escalation support by more experienced senior members of the team, based on a 24/7, 1 week shift pattern.

## Follow the Sun Support - Business Hours

* Click `Add Rotation`
* Enter a name of "*Follow the Sun Support - Business Hours*"
* Select `Partial day` from the three available shift templates
  * Enter a Shift name of "*Asia*"
    * Time Zone set to "*Asia/Tokyo*"
    * Each user is on duty from "*Monday through Friday from 9.00am to 5.00pm*"
    * Handoff happens every "*7 days*"
    * The next handoff happens - Select the next Monday using the calendar
    * Click `Save Rotation`
* Now add an 2nd shift for Europe by clicking `+Add a shift` - `Partial Day`
  * Enter a Shift name of "*Europe*"
    * Time Zone set to "*Europe/London*"
    * Each user is on duty from "*Monday through Friday from 9.00am to 5.00pm*"
    * Handoff happens every "*7 days*"
    * The next handoff happens - Select the next Monday using the calendar
    * Click `Save Shift`
* Now add a 3rd shift for West Coast USA by clicking `+Add a shift` - `Partial Day`
  * Enter a Shift name of "*West Coast*"
    * Time Zone set to "*US/Pacific*"
    * Each user is on duty from "*Monday through Friday from 9.00am to 5.00pm*"
    * Handoff happens every "*7 days*"
    * The next handoff happens - Select the next Monday using the calendar
    * Click `Save Shift`
* You new need to add the users into their allocated shift patterns using either the table above, or the list of users provided to you separately
  * For each Shift, click on the `Manage Members` icon which is the left of the three icons and resembles the image of three heads
    * Add the users to each Shift (note how you have to use their Username and not their real names)
    * The first user added will be the 'current' user for that shift
    * You can re-order the shifts by simply dragging the users up and down, and you can change the current user by clicking `Set Current` on an alternate user

You will now have three different Shift patterns, that provide cover 24hr hours, Mon - Fri, but with no cover at weekends.

We will now add the 2nd Rotation for our Senior SRE Escalation cover.

## Senior SRE Escalation

* Click `Add Rotation`
* Enter a name of "*Senior SRE Escalation*"
* Select `24/7` from the three available shift templates
  * Enter a Shift name of "*Senior SRE Escalation*"
    * Time Zone set to "*Asia/Tokyo*"
    * Handoff happens every "*7 days at 9.00am*"
    * The next handoff happens [select the next Monday from the date picker]
    * Click `Save Rotation`
* Add the users who are allocated the 24/7 shift

That completes the configuration of the Rotations, we now need to configure the Escalation Policies and Routing Keys.
