I started out looking at the raw gzipped .plsit files that are synced with Dropbox for 2do. However this structure was difficult to follow and understand how the syncing works. While the end goal is to be able to sync back to Dropbox, looking elsewhere turned out to be more fruitful.

I next found out that in the Mac app you can export a .db file and save the current 2do state with this. This turned out to be an SQLite Database (which makes sense given that 2Do is most likely using Core Data. The SQLite Databse made the structure apparent very quickly and I worked out the following information from a bit of investigation of the tables used.

 - Tasks are stored in the `tasks` table
 - tasktype: (0 = normal, 1 = checklist, 2 = project)
 - parent: (self explantory uses the parents task's uid)
 - title: The task title
 - notes: additional notes on the task
 - duedate (6406192800 means no duedate, otherwise it is a unix timestamp)
 - datestamp: creation date
 - calendaruid: this indicates the associated calendar object in the calendar table. (a calendar is a list in 2Do)
 - priority, iscompleted, isdeleted (these are all pretty self explanatory)
 - startdate, duetime (also pretty obvious) 
 - creationstamp: Not sure how this differs from datestamp (reminder to look into this)

 - The calendar table has title, uid, redcolor, greencolor, bluecolor
 - If it is a user created list, it's parent name will be LIST
 - canshowinall, canshowintoday: these indicate if the tasks for this list should show in these views.

I think this information will be enough to go from a db to display, which will be my first aim, and while not on par with features it should be a workable 2Do client. I will make it read and write solely from the database. 

After this is done, and looking good as a cross platform app I will attempt to setup syncing as well.
