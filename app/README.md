[Drive to save version's of android apk](https://drive.google.com/drive/folders/1moJrJnZqyKt1aVKzgNa-9p265LIcwpSY?usp=sharing)

To debug the app:

- Run the app locally `python main.py`
- Initialize buildozer `buildozer init`
- Edit the `buildozer.spec` file. Important to edit the requirements.
- Build apk `buildozer android debug`
- Connect phone via USB. Make sure to turn on `developer mode` and turn on `usb debugging`.
- Download [Android Log Viewer](https://bitbucket.org/mlopatkin/android-log-viewer/src/master/) from `Downloads` section.
- Run `./bin/andlogview`. Android Log Viewer will connect to phone via USB. It will show all the logs running at moment. Filter using `org.test.bookmyslot` for app related logs.
- Run the app `buildozer depoy run`. This will launch the app on phone and the Androd Log Viewer will show all the logs.
- If any error comes, app will crash and error will be displayed on the Android Log Viewer.
