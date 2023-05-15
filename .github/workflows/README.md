## Github Actions workflow

#### Scheduled version

```
on:
 schedule:
   - cron: "0 18 * * *"
```

Time is based on [Coordinated Universal Time (UTC)](https://en.wikipedia.org/wiki/Coordinated_Universal_Time)

```
* * * * *
| | | | |------> Weekday (0-6)
| | | |--------> Month (1-12)
| | |----------> Day (1-31)
| |------------> hours (0-23)
|--------------> minutes (0-59)

### Examples ###

# Every 30 mins
"*/30 * * * *"

# End of everyday 2AM UTC (7PM PST)
"0 2 * * *"

# Every morning 6PM UTC (10AM PST)
"0 18 * * *"
```
