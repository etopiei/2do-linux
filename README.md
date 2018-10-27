# 2Do Linux/Windows/macOS Cross Platform Client

I use 2Do everyday to manage everything I have to do, however I also prefer to use Linux for development, and it is the main app the I miss when I'm not using macOS. As there is no way Linux 2Do app I thought it would be fun to create a client app for linux. As a consequence of this being written in Python this is also a cross platform app, and as there is no Windows app either this could also be used on Windows, however I do not anticipate that I will test this much.

**Disclaimer:** This is experimental software written to help solve a problem I've had, it is not guarenteed to work perfectly, or indeed at all. Please also note it will be lacking a lot of features supported by 2Do as I will be prioritising features that I use the most before adding other features in.

# Current Setup

Requirements:

	pip3 install appjar

To test this out go to 2Do app and save a .db file and save it in the same directory as the app.
Then run:

	python3 main.py

## RoadMap

1. ~~Get UI to display current tasks from an SQL Lite Database taken from an app backup.~~
2. Get Basic Features working such as ~~completing tasks~~, ~~searching~~ and changing dates - These actions should update the database
3. Output the current data into a .plist file consistent with 2do dropbox sync files.
4. Implement DropBox connectivity and gzipping files.

## Possible Future Tasks

 - Use a different GUI library (I'm not 100% sold on appJar, it works for now but I'm trying to keep the presentation logic seperate so it can be changed later)
 - Add advanced features such as alerts, notes, attachments, priority, tags (tags may be required for inital release, even though I don't personally use tags)
 - ~~Search (Again this might be part of the inital release, it's kinda important)~~
 - Customise UI colours

## Contributing

If you wish to contribute feel free to add an issue or pull request.
For any further queries please email me at: me.etopiei@gmail.com

