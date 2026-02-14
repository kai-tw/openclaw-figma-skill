import os
import json
import argparse
import urllib.request
import urllib.parse

import ssl

class FigmaClient:
    BASE_URL = "https://api.api.figma.com/v1" # Wait, the URL was api.figma.com, why did I write api.api.figma.com?

    def __init__(self, token):
        self.token = token
        self.context = ssl._create_unverified_context()

    def _request(self, endpoint, params=None):
        url = f"https://api.figma.com/v1/{endpoint}"
        if params:
            url += "?" + urllib.parse.urlencode(params)
        
        req = urllib.request.Request(url)
        req.add_header("X-Figma-Token", self.token)
        
        with urllib.request.urlopen(req, context=self.context) as response:
            return json.loads(response.read().decode())

    def get_me(self):
        return self._request("me")

    def get_team_projects(self, team_id):
        return self._request(f"teams/{team_id}/projects")

    def get_project_files(self, project_id):
        return self._request(f"projects/{project_id}/files")

def main():
    parser = argparse.ArgumentParser(description="Figma API Tool")
    parser.add_argument("action", choices=["get-file", "get-comments", "export", "get-me", "get-team-projects", "get-project-files"])
    parser.add_argument("id", nargs="?", help="The file key, team ID, or project ID")
    parser.add_argument("--ids", help="Comma-separated layer IDs for export")
    parser.add_argument("--format", default="png", choices=["png", "jpg", "svg", "pdf"])
    parser.add_argument("--scale", type=float, default=1.0)
    
    args = parser.parse_args()
    
    token = os.getenv("FIGMA_TOKEN")
    if not token:
        print("Error: FIGMA_TOKEN environment variable not set.")
        return

    client = FigmaClient(token)
    
    try:
        if args.action == "get-file":
            if not args.id:
                print("Error: file_key is required.")
                return
            result = client.get_file(args.id)
            print(json.dumps(result, indent=2))
        elif args.action == "get-comments":
            if not args.id:
                print("Error: file_key is required.")
                return
            result = client.get_comments(args.id)
            print(json.dumps(result, indent=2))
        elif args.action == "get-me":
            result = client.get_me()
            print(json.dumps(result, indent=2))
        elif args.action == "get-team-projects":
            if not args.id:
                print("Error: team_id is required.")
                return
            result = client.get_team_projects(args.id)
            print(json.dumps(result, indent=2))
        elif args.action == "get-project-files":
            if not args.id:
                print("Error: project_id is required.")
                return
            result = client.get_project_files(args.id)
            print(json.dumps(result, indent=2))
        elif args.action == "export":
            if not args.id:
                print("Error: file_key is required.")
                return
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
