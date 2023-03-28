import subprocess
import json
from datetime import datetime

orgs = ["fifthtry", "fastn-stack", "fastn-community"]

org_vice_repos = {}

for org in orgs:
    # Define the command to run
    cmd = "gh repo list --json name,url,description,stargazerCount,isPrivate," \
          "isTemplate,licenseInfo,updatedAt,description,forkCount," \
          "templateRepository,homepageUrl,createdAt --limit 300 %s" % org

    # Call the command and capture its output
    output = subprocess.check_output(cmd, shell=True, text=True)

    # Parse the output as JSON
    repo_list = json.loads(output)

    # Extract the repository information from the JSON and store them in a
    # list of dictionaries
    repos = []
    for repo in repo_list:
        name = repo["name"]
        url = repo["url"]
        stars = repo["stargazerCount"]
        privacy = "private" if repo["isPrivate"] else "public"
        license = repo["licenseInfo"]["name"] if repo["licenseInfo"] else None
        updated_at = datetime.strptime(repo["updatedAt"], "%Y-%m-%dT%H:%M:%SZ")
        created_at = datetime.strptime(repo["createdAt"], "%Y-%m-%dT%H:%M:%SZ")
        desc = repo["description"] if repo["description"] else None
        homepageUrl = repo["homepageUrl"] if repo["homepageUrl"] else None
        forkCount = repo["forkCount"]
        isTemplate = repo["isTemplate"]
        templateRepository = (
            repo["templateRepository"]["owner"]["login"]
            + "/"
            + repo["templateRepository"]["name"]
            if repo["templateRepository"]
            else None
        )
        repo_dict = {
            "name": name,
            "url": url,
            "stars": str(stars),
            "privacy": privacy,
            "license": license,
            "updated-at": updated_at.isoformat(),
            "created-at": created_at.isoformat(),
            "description": desc,
            "fork-count": str(forkCount),
            "template-repository": templateRepository,
            "homepage-url": homepageUrl,
            "is-template": isTemplate
        }
        repos.append(repo_dict)

    org_vice_repos[org] = repos

# Write the list of dictionaries to a JSON file
with open("../artifacts.json", "w") as f:
    json.dump(org_vice_repos, f)

# Print a confirmation message
print("Repository information saved to 'artifacts.json'.")
