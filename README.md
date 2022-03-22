<h1 align="center">🤖 #66DaysOfData's Discord Bot</h1>
The #66DaysOfData is an initiative that has been started to help you develop better data science habits! This is the GitHub repository of the bot that is being used in the <a href="https://discord.gg/PgVEqYDepQ">Discord server</a>.

## ⚙️ Technologies used
* <a href="https://www.python.org/">Python</a>
* <a href="https://discordpy.readthedocs.io/en/stable/">discord.py</a>
* <a href="https://www.sqlite.org/">SQLite</a>

## 🧍 User commands
| Command | Description |
| --- | --- |
| !report | Sends a message to the admins. |
| !thanks \<user\> | Adds one point to a user. |
| !leaderboard | Shows the ranking. |
| !last-day [user] | Gets the last day posted in #progress (14 days archive). |

## 🛡️ Admin commands
| Command/Feature | Description |
| --- | --- |
| !move-msg \<#channel\> \<message_id_1\> [message_id_2] ... [message_id_n] | Moves a message from one channel to a target one. |
| !msg \<#channel\> \<message\> | Sends a message in a channel. |
| !rm-point \<user\> | Removes one point from a user. |
| !choose-winners \<message_id\> \<#channel\> \<number_of_winners\> \<:emoji:\> [mention] [assign_role] | Chooses N random people who have reacted to a message (giveaway). If you want to mention them, type "yes" after the emoji. You can also assign a role to these users. |
| !reaction-users \<message_id\> \<#channel\> \<:emoji:\> [mention] [assign_role] | Similar to !choose-winners, but it gives a list with all members that reacted to a message. |
| !poll <"question"> [option_1] [option_2] ... [option_10] | Creates a poll. The question must be in quotes. If you do not add any options, the poll will be set as Yes/No by default. |
| Discord Nitro scam protection | Bans a user if the scam is detected. |
| Detecting the 66th day | Sends a message to the admins. |
