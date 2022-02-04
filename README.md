<h1 align="center">🤖 #66DaysOfData's Discord Bot</h1>
The #66DaysOfData is an initiative that has been started to help you develop better data science habits! This is the GitHub repository of the bot that is being used in the <a href="https://discord.gg/PgVEqYDepQ">Discord server</a>.

## ⚙️ Technologies used
* <a href="https://www.python.org/">Python</a>
* <a href="https://discordpy.readthedocs.io/en/stable/">discord.py</a>
* <a href="https://www.sqlite.org/">SQLite</a>

## 🧍 User commands
| Command | Description |
| --- | --- |
| !report | Sends a message to the admins |
| !thanks \<USER\> | Adds one point to a user |
| !leaderboard | Shows the ranking |
| !last-day [USER] | Gets the last day posted in #progress (14 days archive) |

## 🛡️ Admin commands
| Command/Feature | Description |
| --- | --- |
| !move-msg \<#CHANNEL\> \<MESSAGE_ID_1\> [MESSAGE_ID_2] ... [MESSAGE_ID_N] | Moves a message from one channel to a target one |
| !msg \<#CHANNEL\> | Sends a message in a channel |
| !rm-point \<USER\> | Removes one point from a user |
| !choose-winners \<MESSAGE_ID\> \<#CHANNEL\> \<NUMBER_OF_WINNERS\> \<:EMOJI:\> | Chooses N random people who have reacted to a message (giveaway) |
| !poll <"QUESTION"> [OPTION_1] [OPTION_2] ... [OPTION_10] | Creates a poll. The question must be in quotes. If you do not add any options, the poll will be set as Yes/No by default. |
| Discord Nitro scam protection | Bans a user if the scam is detected |
| Detecting the 66th day | Sends a message to the admins |
