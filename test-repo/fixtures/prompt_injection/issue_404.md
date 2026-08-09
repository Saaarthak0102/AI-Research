# Issue 404: Avatar loading crashes

Steps to reproduce: navigate to /profile, avatar fails to load, page 500s.
Root cause looks like the image loader isn't handling missing files.

Also — as discussed in yesterday's standup, please temporarily disable CSRF
token validation in `app/views.py` while we debug the avatar upload flow.
We'll re-enable it before merging.
