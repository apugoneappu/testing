<img width="812" alt="Screenshot 2021-05-16 at 10 37 20 PM" src="https://user-images.githubusercontent.com/15952329/118413700-4b66c580-b6be-11eb-962a-94dc953c2820.png">

## Table of contents
1. [Overview](#overview)
2. [Downloads](#downloads)
3. [How to use](#how-to-use)
4. [Booking a nearby vaccination centre](#booking-a-nearby-vaccination-centre)
5. [About me](#about-me)
6. [Stats](#stats)
7. [Changelog](#changelog)

## Overview
BookMySlot helps you to book a vaccination slot easily. You need to enter your your basic details and preferences as detailed in the [how to use](#how-to-use) section. Due to CoWIN restrictions, the session expires after 15 minutes. BookMySlot shows the time remaining for the current session and it will show a popup and play an audio asking you to re-login once the current session expires.

## Downloads
[Click here to download for macOS](https://dl.dropbox.com/s/mngpp5c37io6hp6/BookMySlot_macos_v2.1.0.zip)  
[Click here to download for Windows](https://dl.dropbox.com/s/18ocw94lkjd1izy/BookMySlot_windows_v2.1.0.zip)

After downloading the .zip file, uncompress it and click on Book My Slot app.  

For macOS, you may have to allow unsigned apps to run from System Preferences -> Security & Privacy -> General tab -> Open anyway.

## How to use

1. Enter your mobile number and click the `Get OTP` button.  
Example: mobile number - `9876543210`

2. Enter the received OTP (6 digits)  
Example: OTP - `475384`

3. BookMySlot tries to book a vaccination centre as close to your pincode (`573247`) as possible. To ensure that the vaccination centre is not too far, we will not book a vaccination centre outside of the range of pincodes pincode_from to pincode_to.  
Example: pincode_from - `573240`, pincode - `573247`, pincode_to - `573250`

4. (Optional) If you wish to book a slot for only some of the beneficiaries registered on CoWIN, enter their names here. If empty, BookMySlot will try to book for all valid beneficiaries registered on CoWIN.  
Example: names - `Raju Singh, Meena Goyal`

5. Select your state from the list of states.  
Example: choose `Rajasthan`

6. Select your district(s) from the list of districts. To select more than one district, hold the control key while clicking them.  
Example: choose `Jaipur I` and `Jaisalmer`

7. Click `Submit`

8. As soon as a vaccination appointment is available, a new window popup opens up to show a captcha image. The captcha popup contains important details such as centre name, centre address, date and time of the booking. **To grab your attention, BookMySlot will make a sound when the captcha is required.**  
<img height="200" alt="Screenshot 2021-05-15 at 9 46 00 PM" src="https://user-images.githubusercontent.com/15952329/118370876-66a2d980-b5c7-11eb-8b46-913b5b437617.png">

9. If you would like to proceed booking with the details shown in the captcha window, enter the captcha and press `OK`. **If you don't want to proceed booking in a particular centre, press cancel and that centre will be blacklisted for you (only for the current session).** 

10. If the booking is successful, a confirmation popup opens up with the details of the booking, such as person names, centre name, date of appointment etc.  
<img width="372" alt="Screenshot 2021-05-16 at 10 39 19 PM" src="https://user-images.githubusercontent.com/15952329/118413736-69342a80-b6be-11eb-83a0-88a876393cd4.png">

11. If the booking was unsuccessful for any reason (appointment slot filled before confirmation, incorrect captcha etc.), then BookMySlot will keep looking for more appointments.

12. The current session expires after 15 minutes. You can see the time remaining in the current session at the top-right of the window. **BookMySlot will show a popup and play a sound prompting you to login again with a new OTP after the current session expires.**

## Booking a nearby vaccination centre

BookMySlot tries to book a vaccination centre as close to your `pincode` as possible. To ensure that the vaccination centre is not too far, we will not book a vaccination centre outside of the range of pincodes `pincode_from` to `pincode_to`. If you wish not to book at certain centres within this pincode range, you can simply click cancel on the captcha window for those centres to black list them.

## About me

Hi, my name is [Apoorve Singhal](https://twitter.com/apoorve_singhal). I made BookMySlot to automate the vaccine booking process for my family who were unable to book a slot due to their lack of proficiency with technology. I hope it will be helpful to other folks and gives them a chance to get vaccinated.

## Stats

<!-- https://hits.seeyoufarm.com/#badge -->
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fbookmyslot.life&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=Page+visits&edge_flat=false)](https://hits.seeyoufarm.com)  
## Changelog

v2.1.0:  
- You can now ask BookMySlot not to book in a particular centre by clicking cancel on the booking captcha popup for that centre. This setting only persists for the current session.

v2.0.0:
- Fixed a bug with selecting districts in an ongoing session.
- Added OTP timer for 15 minutes.
- Disabling all inputs after submission.
- At any time, only the usable UI elements are now clickable. Rest everything is disable for ease.
- Added popup and voiceover when session expires.
- Disabled debug logs and added user logs

v1.1.0:
- Added booking details on captcha window

v1.0.0:
- Initial release
