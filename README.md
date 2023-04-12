# Meeting Butler

Takes care of background tasks pertained to meeting and registrations.

## Syntax
All of the configuration settings are passed to the script by mean of ENV variables.
```
$ env meeting_butler_eventbrite_event=<EVENTID> \
  meeting_butler_eventbrite_token=<AUTHTOKEN> \
  meeting_butler_meetingtool_hostname=<HOSTNAME> \
  meeting_butler_meetingtool_token=<AUTHTOKEN> \
  meeting_butler_cache_filename=$(pwd)/cache.db \
  meeting_butler_debug=0 \
  meeting_butler_sync_every=86400 \
  poetry run python -m meeting_butler
```

## Defaults:
Default settings:
 - *meeting_butler_debug*" False
 - *meeting_butler_sync_every*: 86400 (seconds)
