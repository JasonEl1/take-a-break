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

	args := []string{"python3", filepath.Join(usr.HomeDir, ".local/share/take-a-break/reminder.py")}
	args = append(args, os.Args[1:]...)

	cmd = exec.Command(args[0], args[1:]...)
	output, _ := cmd.CombinedOutput()

	fmt.Printf("%s", output)
}
