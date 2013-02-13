bugsquasher
===========

A pluggable tool for squashing bugs and tracking down issues


Some commands
=============

Taking
------

    $ bgsq take 890183 # Adds a new bug for tracking


Listing
-------

    $ bgsq list # List tracked bugs

    Bug: 887818 Working Dir: /super/working/dir/rh-887818
    VM Status:  poweroff
    Bug Title: Easy bug
        Status: NEW
        4 comments
    Bug: 890183 Working Dir: /super/working/dir/rh-890183
    VM Status:  poweroff
    Bug Title: Super difficult bug
        Status: ON_DEV
        6 comments



Show
----

    $ bgsq show 890183 # Shows available information for this bug
    VM Status:  poweroff
    Bug Title: Super difficult bug
        Status: ON_DEV
        6 comments

    $ bgsq show -v 890183 # Shows detailed information for this bug
    VM Status:  poweroff
    Bug Title: Super difficult bug
        Status: ON_DEV
        6 comments

        Comment: 1
            Author: mickey@mouse.com, Private: 20121217T12:05:06, Date False
            blah blah blah

        Comment 2:
            Author: mickey@mouse.com, Private: 20121217T12:05:06, Date False
            bleh bleh bleh
        ......



Update Bug info
---------------

    $ bgsq update -b 890183 # updates bug information