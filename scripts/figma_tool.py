import os
import json
import argparse
import urllib.request
import urllib.parse

class FigmaClient:
    BASE_URL = "https://api.figma.com/v1"

    def __init__(self, token):
        self.token = token

    def _request(self, endpoint, params=None):
        url = f"{self.BASE_URL}/{endpoint}"
        if params:
            url += "?" + urllib.parse.urlencode(params)
        
        req = urllib.request.Request(url)
        req.add_header("X-Figma-Token", self.token)
        
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())

    def get_file(self, file_key):
        return self._request(f"files/{file_key}")

    def get_comments(self, file_key):
        return self._request(f"files/{file_key}/comments")

    def export_images(self, file_key, ids, format="png", scale=1):
        params = {
            "ids": ids,
            "format": format,
            "scale": scale
        }
        return self._request(f"images/{file_key}", params)

def main():
    parser = argparse.ArgumentParser(description="Figma API Tool")
    parser.add_argument("action", choices=["get-file", "get-comments", "export"])
    parser.add_argument("file_key", help="The Figma file key")
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
            result = client.get_file(args.file_key)
            print(json.dumps(result, indent=2))
        elif args.action == "get-comments":
            result = client.get_comments(args.file_key)
            print(json.dumps(result, indent=2))
        elif args.action == "export":
            if not args.ids:
                print("Error: --ids is required for export action.")
                return
            result = client.export_images(args.file_key, args.ids, args.format, args.scale)
            print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
