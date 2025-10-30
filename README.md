# take-a-break

Python command line tool to remind you to take breaks when working. Currently only tested on macos.

### Quick setup (MacOS)

Open the `take-a-break` folder after downloading and run the following command in the terminal: `./setup.sh`

OR

```

git clone https://github.com/JasonEl1/take-a-break.git
cd take-a-break
./setup.sh
```

### How to use the tool:

Use the tool using the name `work`. The following commands are available:

```
work get          -> get current state of work mode (can be 'set' or 'unset')
work set          -> set work mode to 'set' with default interval of 20 minutes
work set -t value -> set work mode to 'set' with a specific reminder interval (minutes)
work unset        -> set work mode to 'unset'
work next         -> get  time remaining until next reminder
```

When `work mode` is enabled, you will be reminded to take a break from your work via a popup window at a certain time interval.

The program will remind you to take a break after the specified time interval with the option to reset the reminder or unset work mode. The program does not continue running after `work set` is called, but makes use of cron to schedule the reminder at the correct time.

### Uninstallation

Use the command `work uninstall` and follow the prompts.
