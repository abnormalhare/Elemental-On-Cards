package main

import (
	"log"
	"os"
	"os/exec"
	"path/filepath"
)

func main() {
	// Define the repository URL
	repoURL := "https://github.com/abnormalhare/elemental-on-cards.git"

	// Define the repository directory as "cards"
	repoDir := "./cards"
	_, err := os.Stat(filepath.Join(repoDir, ".git"))
	if os.IsNotExist(err) {
		// Clone the repository if it doesn't exist
		log.Println("Cloning repository into 'cards' folder...")
		cmd := exec.Command("git", "clone", repoURL, repoDir)
		cmd.Stdout = os.Stdout
		cmd.Stderr = os.Stderr
		if err := cmd.Run(); err != nil {
			log.Fatalf("Failed to clone repository: %v", err)
		}
	} else {
		// Pull the latest changes if the repository exists
		log.Println("Pulling latest changes in 'cards' folder...")
		cmd := exec.Command("git", "-C", repoDir, "pull")
		cmd.Stdout = os.Stdout
		cmd.Stderr = os.Stderr
		if err := cmd.Run(); err != nil {
			log.Fatalf("Failed to pull latest changes: %v", err)
		}
	}

	// Restart the bot
	log.Println("Restarting the bot...")
	botCmd := exec.Command("python", "eoc.py")
	botCmd.Dir = repoDir // Set the working directory to "cards"
	botCmd.Stdout = os.Stdout
	botCmd.Stderr = os.Stderr
	if err := botCmd.Start(); err != nil {
		log.Fatalf("Failed to restart the bot: %v", err)
	}

	log.Println("Update completed successfully.")
}
