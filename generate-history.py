import os
import random
import subprocess
from datetime import date, timedelta, datetime

# --- Configuration ---
START_DATE = date(2007, 1, 1)
END_DATE = date.today()
FILE_NAME = "activity_log.txt"
# ---------------------

def make_commit(commit_date):
    # Append to a dummy file to create a trackable change
    with open(FILE_NAME, "a") as f:
        f.write(f"Activity on {commit_date}\n")
    
    # Format date for Git environment variables
    git_date = commit_date.strftime("%Y-%m-%dT%H:%M:%S")
    
    # Stage the file
    subprocess.run(["git", "add", FILE_NAME], check=True)
    
    # Set the environment variables to spoof the commit dates
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = git_date
    env["GIT_COMMITTER_DATE"] = git_date
    
    # Commit the changes quietly
    subprocess.run(
        ["git", "commit", "-m", f"chore: activity update for {commit_date.strftime('%Y-%m-%d')}"],
        env=env,
        check=True,
        stdout=subprocess.DEVNULL
    )

def main():
    # Ensure we are in a git repository
    if not os.path.exists(".git"):
        print("Initializing new Git repository...")
        subprocess.run(["git", "init"], check=True)
    
    current_date = START_DATE
    total_commits = 0
    
    print(f"Generating commits from {START_DATE} to {END_DATE}...")
    print("This might take a minute...")
    
    while current_date <= END_DATE:
        num_commits = random.randint(0, 5)
        
        for _ in range(num_commits):
            # Randomize the time of day (between 9:00 AM and 6:59 PM)
            hour = random.randint(9, 18)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            
            commit_time = datetime.combine(current_date, datetime.min.time()).replace(
                hour=hour, minute=minute, second=second
            )
            
            make_commit(commit_time)
            total_commits += 1
            
        current_date += timedelta(days=1)
        
    print(f"\nSuccess! Created {total_commits} commits over the chosen time period.")
    print("You can now link your remote repository and push your changes:")
    print("  git remote add origin <your-github-repo-url>")
    print("  git branch -M main")
    print("  git push -u origin main")

if __name__ == "__main__":
    main()