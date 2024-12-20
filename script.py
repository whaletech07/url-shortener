import os
import random
from github import Github, GithubException

def update_html_file(template_path, url):
    try:
        # Ensure the URL starts with "https://"
        if not url.startswith("https://"):
            url = "https://" + url
        
        # Copy the template file to index.html
        index_path = "index.html"
        with open(template_path, "r") as template_file:
            content = template_file.read()
        
        # Replace the placeholder with the provided URL.
        updated_content = content.replace("{{URL_PLACEHOLDER}}", url)
        
        with open(index_path, "w") as index_file:
            index_file.write(updated_content)
        
        print(f"Copied and updated HTML file with the URL: {url}")
        return index_path, updated_content
    except FileNotFoundError:
        print(f"Error: File '{template_path}' not found.")
        return None, None


def push_to_github(repo_name, file_path, github_token, commit_message="Add new entry"):
    try:
        # Authenticate with GitHub
        g = Github(github_token)
        repo = g.get_repo(repo_name)
        
        # Generate a random directory name
        random_dir = str(random.randint(1000, 9999))
        
        # Get the file name and construct the path in the repository
        file_name = os.path.basename(file_path)
        repo_file_path = f"{random_dir}/{file_name}"
        
        # Read the updated file content
        with open(file_path, "r") as file:
            content = file.read()
        
        # Create or update the file in the repository
        try:
            # Try to retrieve the file to check if it exists
            contents = repo.get_contents(repo_file_path)
            # If the file exists, update it
            repo.update_file(
                contents.path,
                commit_message,
                content,
                contents.sha
            )
            print(f"Updated '{repo_file_path}' in the GitHub repository.")
        except GithubException as e:
            if e.status == 404:
                # If the file does not exist, create it
                repo.create_file(repo_file_path, commit_message, content)
                print(f"Created '{repo_file_path}' in the GitHub repository.")
            else:
                raise  # Re-raise other exceptions
    except Exception as e:
        print(f"Error pushing to GitHub: {e}")

def main():
    # Configuration
    template_path = "template.html"
    repo_name = "user/repo"
    github_token = "token"
    
    # Ask for a URL
    url = input("Enter the URL to insert into the HTML file: ")
    
    # Update the HTML file
    index_path, updated_content = update_html_file(template_path, url)
    
    if index_path:
        # Push the changes to GitHub
        push_to_github(repo_name, index_path, github_token)
        
        # Delete the local index.html file after pushing
        os.remove(index_path)
        print(f"Deleted local '{index_path}' after pushing to GitHub.")
    else:
        print("Failed to update the HTML file.")

if __name__ == "__main__":
    main()
