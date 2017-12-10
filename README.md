# Hooker Map

`Hooker Index = Median net income per year / Median hooker rate per hour`

## Story

I am a long time subscriver of [r/MapPorn](https://www.reddit.com/r/MapPorn/) on Reddit.
Several days ago I saw a post titled
[
  "How many times per month you can afford hooker with your country's average monthly wage
  considering that average hooker costs €50 for half hour(€100 for Switzerland)"
](
  https://www.reddit.com/r/MapPorn/comments/7i7vas/how_many_times_per_month_you_can_afford_hooker/
) (the image has been already deleted).

I thought that it is curious, but that post was really terrible.
So I decided to create a new one but more accurate:
1. I decided to find actual costs, instead of this weak assumption _"€50 for half hour(€100 for Switzerland)"_.
2. I think that median net income makes more sense than average wage in this case.

## Sources

Median net income data is from Eurostat: http://ec.europa.eu/eurostat/web/gdp-and-beyond/quality-of-life/median-income

Median hooker rate per hour is scrapped from various websites.

Source code of scrapper and table generator on GitHub: https://github.com/HornyRussianGuy/hooker_map


## Results

[Results table on Gist](https://gist.github.com/HornyRussianGuy/273c9057e2bab307db62175bd098aee4)

[Results map on Imgur](https://i.imgur.com/V17vrHg.png) (tha map is created via [mapchart.net](https://mapchart.net/europe.html))

## Possible pitfalls

After I finishing scrapping, I've realised that one of 3 websites gave me most of the data.

For some countries there is huge difference in average rates at local websites (on the local language) and at foreign websites (in English). Hookers expect foreigners to pay much more. It skews the data.

## Running
