//take-a-break: VERSION=0.9.0

package main

import (
	"os"
	"os/exec"
)

func main() {
	if len(os.Args) == 3 {
		exec.Command("python3", "reminder.py", os.Args[1], "-t", os.Args[2])
	} else {
		exec.Command("python3", "reminder.py", os.Args[1]) //check
	}
}
