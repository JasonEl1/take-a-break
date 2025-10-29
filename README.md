# take-a-break

Python command line tool to remind you to take breaks when working. Currently only works with Unix-like OS.

### Quick setup (MacOS)

Note: Currently only works with zsh

Open the `take-a-break` folder after downloading and run the following command in the terminal: `./setup.sh`

Enter the alias you want to use for this tool. I personally use it as `work`
This creates an alias named `work` or whatever else you decide to use in your .zshrc file. You can now use `work` (or your alternative chosen alias) followed by the appropriate commands to use the tool.

### How to use the tool:

When `work mode` is enabled, you will be reminded to take a break from your work every 30 mins via a popup window.

The following commands are available (assuming chosen alias is `work`) :

```
work get -> get current state of work mode (can be 'set' or 'unset')
work set -> set work mode to 'set' with default interval of 20 minutes
work set -t value -> set work mode to 'set' with a specific reminder interval (minutes)
work unset -> set work mode to 'unset'
work next -> get  time remaining until next reminder
```

The program will remind you to take a break after the specified time interval with the option to reset the reminder or unset work mode. The program does not continue running after `work set` is called, but makes use of cron to schedule the reminder at the correct time.

### Uninstallation

Note: Currently only works with zsh

Run `./uninstall.sh` in the `take-a-break` folder and provide your chosen alias name.
