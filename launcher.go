//take-a-break: VERSION=0.9.0

package main

import (
	"fmt"
	"log"
	"os"
	"os/exec"
	"os/user"
	"path/filepath"
)

func main() {
	var cmd *exec.Cmd
	usr, _ := user.Current()

	if len(os.Args) == 4 {
		cmd = exec.Command("python3", filepath.Join(usr.HomeDir, ".local/share/take-a-break/reminder.py"), os.Args[1], "-t", os.Args[3])
	} else {
		cmd = exec.Command("python3", filepath.Join(usr.HomeDir, ".local/share/take-a-break/reminder.py"), os.Args[1])
	}
	output, err := cmd.CombinedOutput()

	if err != nil {
		log.Fatalf("%v\n%s", err, output)
	}

	fmt.Printf("%s", output)
}
