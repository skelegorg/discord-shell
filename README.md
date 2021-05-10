# discord shell
 navigate discord through the console! has the capability to function as a selfbot (i do not officially support this) or can run through a bot you create (as i have done)

start the bot by typing >terminal start
alternatively, if you have headless boot enabled the bot will boot into your default server when the script is executed.

traverse the server in a file-system like format with linux bash syntax
- ls: lists all categories in server, or alternatively if you are in a category, lists all text channels
- cd {category}: changes into a category. alternatively call with no argument to leave the current category
- snap {text channel}: take a snapshot of the given channel and display the last 15 messages sent
- watch {text channel}: open a view of the text channel that updates in real time as messages are sent.
- send {text channel} {message}: sends message in the given text channel.
- exit: exits terminal session, call >terminal close to deactivate the bot.
