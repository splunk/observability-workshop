## Summary of this lab:
* Learn how to configure how to mute Alerts
---
## Step 1: learn how to configure muting your alerts
There are times when you, for a period of time, don't want to be disturbed by notifications for some non ## critical alerts. For that you can use muting rules in SignalFx. Let's create one!

1. Hover over ALERTS in the menu and click on Detectors

![](https://github.com/signalfx/app-dev-workshop/blob/master/screenshots/M1-l3-1.png) 

2. If you created an alert detector in "Working with Detectors" you can click on the three dots (...) on the far right and click on Create Muting Rule...

![](https://github.com/signalfx/app-dev-workshop/blob/master/screenshots/M1-l3-2.png) 

3. In the Muting Rule window check Mute Indefinitely. This will mute the rule permanently, let's say for maintenance windows, until you come back here and uncheck this box.

![](https://github.com/signalfx/app-dev-workshop/blob/master/screenshots/M1-l3-3.png) 

4. Click Next and in the new window read the muting rule setup

![](https://github.com/signalfx/app-dev-workshop/blob/master/screenshots/M1-l3-4.png) 

5. Click on Mute Indefinitely to confirm. You won't be receiving any email notifications from you alert detector until you resume notifications again.

![](https://github.com/signalfx/app-dev-workshop/blob/master/screenshots/M1-l3-5.png) 

6. To Resume notifications, hover over ALERTS in the top menu and click on Muting Rules. You will see the name of the detector you muted notifications for under Detector.

![](https://github.com/signalfx/app-dev-workshop/blob/master/screenshots/M1-l3-6.png) 
![](https://github.com/signalfx/app-dev-workshop/blob/master/screenshots/M1-l3-7.png) 

7. Click on the thee dots (...) on the far right 

8. Click on Resume Notifications

![](https://github.com/signalfx/app-dev-workshop/blob/master/screenshots/M1-l3-8.png) 

9. Click on Resume to confirm and resume notifications for this detector

![](https://github.com/signalfx/app-dev-workshop/blob/master/screenshots/M1-l3-9.png) 

10. **Congratulations!** You have now resumed your alert notifications!

![](https://github.com/signalfx/app-dev-workshop/blob/master/screenshots/M1-l3-10.png) 

Continue the workshop with [Running the SmartAgent in Kubernetes](https://github.com/signalfx/app-dev-workshop/wiki/1.4-Running-the-SmartAgent-in-Kubernetes-using-K3s)
