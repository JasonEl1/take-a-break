package main

import (
	"fmt"
	"os"
	"os/exec"
	"os/user"
	"path/filepath"
)

func main() {
	var cmd *exec.Cmd
	usr, _ := user.Current()

	if len(os.Args) == 4 {
		cmd = exec.Command("python3", filepath.Join(usr.HomeDir, ".local/share/take-a-break/reminder.py"), os.Args[1], os.Args[2], os.Args[3])
	} else if len(os.Args) == 3 {
		cmd = exec.Command("python3", filepath.Join(usr.HomeDir, ".local/share/take-a-break/reminder.py"), os.Args[1], os.Args[2])
	} else if len(os.Args) == 2 {
		cmd = exec.Command("python3", filepath.Join(usr.HomeDir, ".local/share/take-a-break/reminder.py"), os.Args[1])
	} else {
		cmd = exec.Command("python3", filepath.Join(usr.HomeDir, ".local/share/take-a-break/reminder.py"))
	}
	output, _ := cmd.CombinedOutput()

	fmt.Printf("%s", output)
}
