package main

import (
	"log"
	"os"
	"os/exec"
	"path/filepath"
)

func main() {
	// Define the repository URL and the temporary directory for cloning
	repoURL := "https://github.com/abnormalhare/elemental-on-cards.git"
	tempDir := filepath.Join(os.TempDir(), "discord-bot-game")

	// Remove the temporary directory if it exists
	if _, err := os.Stat(tempDir); err == nil {
		if err := os.RemoveAll(tempDir); err != nil {
			log.Fatalf("Failed to remove temporary directory: %v", err)
		}
	}

	// Clone the repository
	log.Println("Cloning repository...")
	cmd := exec.Command("git", "clone", repoURL, tempDir)
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	if err := cmd.Run(); err != nil {
		log.Fatalf("Failed to clone repository: %v", err)
	}

	// Copy files from the cloned repository to the current directory
	log.Println("Updating files...")
	err := filepath.Walk(tempDir, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}

		// Skip the root directory
		if path == tempDir {
			return nil
		}

		// Determine the relative path and destination path
		relPath, err := filepath.Rel(tempDir, path)
		if err != nil {
			return err
		}
		destPath := filepath.Join(".", relPath)

		// If it's a directory, create it
		if info.IsDir() {
			if err := os.MkdirAll(destPath, os.ModePerm); err != nil {
				return err
			}
		} else {
			// If it's a file, copy it
			srcFile, err := os.Open(path)
			if err != nil {
				return err
			}
			defer srcFile.Close()

			destFile, err := os.Create(destPath)
			if err != nil {
				return err
			}
			defer destFile.Close()

			if _, err := destFile.ReadFrom(srcFile); err != nil {
				return err
			}
		}
		return nil
	})
	if err != nil {
		log.Fatalf("Failed to update files: %v", err)
	}

	// Clean up the temporary directory
	log.Println("Cleaning up...")
	if err := os.RemoveAll(tempDir); err != nil {
		log.Fatalf("Failed to remove temporary directory: %v", err)
	}

	// Restart the bot
	log.Println("Restarting the bot...")
	botCmd := exec.Command("python", "eoc.py")
	botCmd.Stdout = os.Stdout
	botCmd.Stderr = os.Stderr
	if err := botCmd.Start(); err != nil {
		log.Fatalf("Failed to restart the bot: %v", err)
	}

	log.Println("Update completed successfully.")
}
