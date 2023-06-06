# Bury After Fail Streak

This [Anki](https://apps.ankiweb.net/) addon will automatically bury cards that you have repeatedly failed. If you fail the same card 3 times consecutively on the same day, the card is buried. (Buried cards are disabled until the next day)

The default fail streak length is 3, though this can be changed if you want to allow for a longer fail streak. (I chose 3 as a somewhat arbitrary number, another number may work better for you!)

There is also a pause button added to the Tools menu. When paused, fail streaks are not checked and not enforced, so you can have an infinitely long fail streak while the plugin is paused.


## Configuration

The plugin can be configured via Tools->Add-ons, then select `Bury After Fail Streak`, then click `Config` in the lower right.

Each configuration key is documented in the [bury_after_fail_streak/config.md](bury_after_fail_streak/config.md) file.


## Installation

## Via AnkiWeb

Visit the [AnkiWeb addon page](https://ankiweb.net/shared/info/966431904), then follow the instructions.

### Manual

Use the `release.sh` script to generate an ankiaddon file. Then, install the ankiaddon file.


## Anki Versions

This plugin officially supports Anki 2.1.63, but it may also support other versions. I haven't tested.

