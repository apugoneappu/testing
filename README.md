<img width="912" alt="Screenshot 2021-06-09 at 5 49 42 PM" src="https://user-images.githubusercontent.com/15952329/121356131-36442600-c94e-11eb-893f-d97292bf1c7d.png">


## Table of contents
- [Table of contents](#table-of-contents)
- [Overview](#overview)
- [Downloads](#downloads)
- [How to use](#how-to-use)
- [Booking a nearby vaccination centre](#booking-a-nearby-vaccination-centre)
- [About me](#about-me)
- [Donation](#donation)
- [Stats](#stats)
- [Changelog](#changelog)

## Overview
BookMySlot helps you to book a vaccination slot easily. You need to enter your your basic details and preferences as detailed in the [how to use](#how-to-use) section. Due to CoWIN restrictions, the session expires after 15 minutes. BookMySlot shows the time remaining for the current session and it will show a popup and play an audio asking you to re-login once the current session expires.

## Downloads
### [Click here to download for macOS v6](https://dl.dropbox.com/s/wjwun81b842in68/BookMySlot_macos_v6.0.0.zip)  
### [Click here to download for Windows v6](https://dl.dropbox.com/s/n8vlqkdhutvwqho/BookMySlot_windows_v6.0.0.zip)

### [Click here to download Fully automatic version for macOS vfm1](#TODO)  
### [Click here to download Fully automatic version for windows vfw1](https://dl.dropbox.com/s/ek0c4h6fe4h3n3v/BookMySlot_windows_vfw1.0.0.zip)  
### [Click here to download OTP reader for Android vfa1](https://dl.dropbox.com/s/fm6edwzk9g0mxv5/BookMySlot_android_v1.0.0.apk) - Please visit [this page](https://www.verizon.com/support/knowledge-base-222186/) to allow installation of apps from outside the play store.

Version v6 release date: 9th June 5:53 PM
Android v1 release date 20th June 7:17 AM 

After downloading the .zip file, uncompress it and click on Book My Slot app.  

For macOS, you may have to allow unsigned apps to run from System Preferences -> Security & Privacy -> General tab -> Open anyway.

## How to use

1. Enter your mobile number and click the `Get OTP` button.<br/>Example: mobile number - `9876543210`
2. Enter the received OTP (6 digits)<br/>Example: OTP - `475384`
3. BookMySlot tries to book a vaccination centre as close to your pincode (`573247`) as possible. To ensure that the vaccination centre is not too far, we will not book a vaccination centre outside of the range of pincodes pincode_from to pincode_to.<br/>Example: pincode_from - `573240`, pincode - `573247`, pincode_to - `573250`
4. Click the `Get beneficiaries` button. Then, select all the names for which you wish to book a slot for. 
5. **(Optional) You can remove the confirmation before slot booking by unselecting the 'Confirm slot details before booking' option. However, this may lead to booking at unwanted centres.**
6. (Optional) If you wish to book a slot for only some of the available vaccine types, enter their names here. If empty, BookMySlot will try to book for all available vaccines.<br/>Example: vaccine names - `Covaxin, Covishield`
7. (Optional) If you wish to book only free or paid slots, you can select the vaccine cost. 
8. Select your state from the list of states.<br/>Example: choose `Rajasthan`
9. Select your district(s) from the list of districts. To select more than one district, hold the control key while clicking them.<br/>Example: choose `Jaipur I` and `Jaisalmer`
10. Click `Submit`
11. As soon as a vaccination appointment is available, a new window popup opens up to confirm the booking. The popup contains important details such as centre name, centre address, date and time of the booking. **To grab your attention, BookMySlot will make a sound when the confirmation is required.**<br/><img width="372" alt="Screenshot 2021-06-09 at 6 10 05 PM" src="https://user-images.githubusercontent.com/15952329/121356230-49ef8c80-c94e-11eb-9e6a-d1a848e3c2dd.png">
12. If you would like to proceed booking with the details shown in the popup, press `OK`. **If you don't want to proceed booking in a particular centre, press cancel and that centre will be blacklisted for you (only for the current session).** 
13. If the booking is successful, a confirmation popup opens up with the details of the booking, such as person names, centre name, date of appointment etc.<br/><img width="607" alt="Screenshot 2021-06-09 at 6 10 14 PM" src="https://user-images.githubusercontent.com/15952329/121356247-4c51e680-c94e-11eb-8660-8a6bf62cb161.png">
14. If the booking was unsuccessful for any reason (appointment slot filled before confirmation etc.), then BookMySlot will keep looking for more appointments.
15. The current session expires after 15 minutes. You can see the time remaining in the current session at the top-right of the window. **BookMySlot will show a popup and play a sound prompting you to login again with a new OTP after the current session expires.**

## Booking a nearby vaccination centre

BookMySlot tries to book a vaccination centre as close to your `pincode` as possible. To ensure that the vaccination centre is not too far, we will not book a vaccination centre outside of the range of pincodes `pincode_from` to `pincode_to`. If you wish not to book at certain centres within this pincode range, you can simply click cancel on the confirmation popup for those centres to black list them.

## About me

Hi! I made BookMySlot to automate the vaccine booking process for my family who were unable to book a slot due to their lack of proficiency with technology. I hope it will be helpful to other folks and gives them a chance to get vaccinated. Please report issues by sending an email to [contact@bookmyslot.life](mailto:contact@bookmyslot.life)

## Donation

If the app helped you, please consider supporting the development of this app! **60% of all proceeds will be donated for COVID relief.**  
Please click the button below to donate. 

<form>
  <script src="https://checkout.razorpay.com/v1/payment-button.js" data-payment_button_id="pl_HKfrUOWYZDvUhR" async>
  </script>
</form>

## Stats

<!-- https://hits.seeyoufarm.com/#badge -->
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fbookmyslot.life&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=Page+visits&edge_flat=false)](https://hits.seeyoufarm.com)  
## Changelog

v6.0.0:
- Handled a change on CoWIN which stopped the session after 21 retries.
- CoWIN has removed captcha.
- Option to book without confirmation

v5.0.0:
- Now beneficiary names are fetched for easy use
- Session will not keep getting logged out
- Added prompt to update the app
- Added link for donation

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
