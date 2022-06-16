# Sucri Bot
## About
Sucri Bot is a discord bot designed to do some basic tasks on Charlemagne's MPSI2's Discord server, updated year after year.

Sucri Bot est un bot discord développé pour faire quelques tâches basiques sur le serveur Discord de la MPSI2 de Charlemagne, mis à jour année après année.

## Features
- **Commands**:
    - `$sucri help`: returns the list of commands
    - `$sucri mail [mail]` : returns the email adress of the specified user
    - `$sucri td` : shows the time and date of TDs
- **Other**:
    - Automatic reminder to take the french books
    - *BETA* Random exercise generator

## Build
The code is hosted on `repl.it` and can be found [here](https://replit.com/@redrapious/SucriBot). To keep the bot "alive", the `webserver.py` script is running and is frequently pinged by an `UptimeBot` request.

Alternatively, it can be hosted on a Raspberry Pi. 

### Tokens and IDs
First, you'll need to create a discord application on your [Discord Developper](https://discord.com/developers/applications/) account. Then, create a bot, and request a token for it.

Second, copy and past the following IDs in the beggining of the `main.py` file:
- admin_id: the ID of the bot's owner
- serveur_id: the ID of the MPSI2 discord server
- tdgrp1_id: the ID of the group of the first TD
- eleve_id: the ID of the `Eleves` role
- general_sans_profs: the ID of the channel (usually `général-sans-profs') where the bot will post the french books reminders

## Contributors
- **pa1n**: initial creator of the bot in 2020
- **[Red Rapious](https://github.com/Red-Rapious)**: developper of the bot since september 2021
- **[marilabs](https://github.com/marilabs)**: illustrator of the wonderful logo which can be found in the ressources, and usually used as a profile picture for the bot

## License
This work is licensed under the [CC-BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) license.