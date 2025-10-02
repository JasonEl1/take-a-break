# take-a-break

Python command line tool to remind you to take breaks when working. Currently only works with Unix-like OS.

### Quick setup (MacOS)

Open the `take-a-break` folder after downloading and run the following command in the terminal: `./setup.sh`

Enter the alias you want to use for this tool. I personally use it as `work`
This creates an alias named `work` or whatever else you decide to use in your .zshrc file. You can now use `work` (or your alternative chosen alias) followed by the appropriate commands to use the tool.

### How to use the tool:

When `work mode` is enabled, you will be reminded to take a break from your work every 30 mins via a popup window.

The state of `work mode` can be altered using the following commands (assuming chosen alias is `work`) :

```
work get -> get current state of work mode (can be 'set' or 'unset')
work set -> set work mode to 'set'
work set --time=value -> set work mode to 'set' with a specific reminder interval (minutes)
work unset -> set work mode to 'unset'
work next -> get  time remaining until next reminder
work update -> set next reminder to 30 minutes from now. Only works if work mode is 'set'.
```

To set a break reminder for a longer or shorter duration than the default 30 minutes, use `work set -t {duration}`

Note: `update` achieves the same result as runnning `unset` followed by `set` and `next`.
