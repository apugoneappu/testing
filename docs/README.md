<img width="912" alt="Screenshot 2021-05-21 at 8 16 20 AM" src="https://user-images.githubusercontent.com/15952329/119075671-c86fa300-ba0e-11eb-9dcd-6804696420d4.png">

## Table of contents
- [Table of contents](#table-of-contents)
- [Overview](#overview)
- [Downloads](#downloads)
- [How to use](#how-to-use)
- [Booking a nearby vaccination centre](#booking-a-nearby-vaccination-centre)
- [About me](#about-me)
- [Stats](#stats)
- [Changelog](#changelog)

## Overview
BookMySlot helps you to book a vaccination slot easily. You need to enter your your basic details and preferences as detailed in the [how to use](#how-to-use) section. Due to CoWIN restrictions, the session expires after 15 minutes. BookMySlot shows the time remaining for the current session and it will show a popup and play an audio asking you to re-login once the current session expires.

## Downloads
[Click here to download for macOS v4](https://dl.dropbox.com/s/f1aelf4az31dnoz/BookMySlot_macos_v4.0.0.zip)  
[Click here to download for Windows v4](https://dl.dropbox.com/s/ygnzvnlk2awho89/BookMySlot_windows_v4.0.0.zip)

Version v4 release date: 21st May 8:00 AM 

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

5. (Optional) If you wish to book a slot for only some of the available vaccine types, enter their names here. If empty, BookMySlot will try to book for all available vaccines.   
Example: vaccine names - `Covaxin, Covishield`

6. (Optional) If you wish to book only free or paid slots, you can select the vaccine cost. 

7. Select your state from the list of states.  
Example: choose `Rajasthan`

8. Select your district(s) from the list of districts. To select more than one district, hold the control key while clicking them.  
Example: choose `Jaipur I` and `Jaisalmer`

9. Click `Submit`

10. As soon as a vaccination appointment is available, a new window popup opens up to show a captcha image. The captcha popup contains important details such as centre name, centre address, date and time of the booking. **To grab your attention, BookMySlot will make a sound when the captcha is required.**  
<img height="200" alt="Screenshot 2021-05-21 at 8 18 21 AM" src="https://user-images.githubusercontent.com/15952329/119075690-d6bdbf00-ba0e-11eb-90f0-f603de9a7e63.png">


11. If you would like to proceed booking with the details shown in the captcha window, enter the captcha and press `OK`. **If you don't want to proceed booking in a particular centre, press cancel and that centre will be blacklisted for you (only for the current session).** 

12. If the booking is successful, a confirmation popup opens up with the details of the booking, such as person names, centre name, date of appointment etc.  
<img width="372" alt="Screenshot 2021-05-16 at 10 39 19 PM" src="https://user-images.githubusercontent.com/15952329/118413736-69342a80-b6be-11eb-83a0-88a876393cd4.png">

13. If the booking was unsuccessful for any reason (appointment slot filled before confirmation, incorrect captcha etc.), then BookMySlot will keep looking for more appointments.

14. The current session expires after 15 minutes. You can see the time remaining in the current session at the top-right of the window. **BookMySlot will show a popup and play a sound prompting you to login again with a new OTP after the current session expires.**

## Booking a nearby vaccination centre

BookMySlot tries to book a vaccination centre as close to your `pincode` as possible. To ensure that the vaccination centre is not too far, we will not book a vaccination centre outside of the range of pincodes `pincode_from` to `pincode_to`. If you wish not to book at certain centres within this pincode range, you can simply click cancel on the captcha window for those centres to black list them.

## About me

I made BookMySlot to automate the vaccine booking process for my family who were unable to book a slot due to their lack of proficiency with technology. I hope it will be helpful to other folks and gives them a chance to get vaccinated. Please report issues by sending an email to [contact@bookmyslot.life](mailto:contact@bookmyslot.life)

## Stats

<!-- https://hits.seeyoufarm.com/#badge -->
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fbookmyslot.life&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=Page+visits&edge_flat=false)](https://hits.seeyoufarm.com)  
## Changelog

v4.0.0:
- Added option to restrict vaccine name, vaccine price
- Re-enabling all input options after every session
- Logging when OTP generated
- showing beneficiaries, vaccine name and price in captcha window
- vaccine names and beneficiary names can be in any case now

v3.0.0:
- CoWIN segregated slots into dose1 and dose2. This was causing captcha retries for some centres where `total doses = dose 1 + dose 2` was not matching up. Fixed that.

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
