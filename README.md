<h1 align="center">🤖 #66DaysOfData's Discord Bot</h1>
The #66DaysOfData is an initiative that has been started to help you develop better data science habits! This is the GitHub repository of the bot that is being used in the <a href="https://discord.gg/PgVEqYDepQ">Discord server</a>.

## ⚙️ Technologies used
* <a href="https://www.python.org/">Python</a>
* <a href="https://docs.pycord.dev/en/master/">Pycord</a>
* <a href="https://www.sqlite.org/">SQLite</a>

## 🧍 User commands
| Command/Feature | Description |
| --- | --- |
| /report | Sends a message to the admins |
| Report message | Right click on a message → Apps → Report message |
| /thanks \<user\> | Adds one point to a user in the leaderboard |
| /leaderboard | Shows the ranking |
| /last-day [user] | Gets the last day posted in #progress (14 days archive) |

## 🛡️ Admin commands
| Command/Feature | Description |
| --- | --- |
| /x-move-message \<#channel\> \<message_id_1\>, [message_id_2], [message_id_n] | Moves a message from one channel to a target one |
| /x-send-message \<#channel\> \<message\> | Sends a message to a channel |
| /x-remove-point \<user\> | Removes one point from a user |
| /x-choose-winners \<message_id\> \<#channel\> \<number_of_winners\> \<:emoji:\> [mention] [assign_role] | Chooses N random people who have reacted to a message (giveaway). You can also assign a role to these users. |
| /x-reaction-users \<message_id\> \<#channel\> \<:emoji:\> [mention] [assign_role] | Shows all the members who have reacted to a message |
| /x-poll \<question\> [option_1], [option_2], ... [option_10] | Creates a poll |
| Discord Nitro scam protection | Bans a user if the scam is detected |
| Detecting the 66th day | Sends a message to the admins |
