---
date: 2021-10-12T00:00:00+00:00
author: Ryan Svihla
layout: post
tags: [ kubernetes, github, docker ]
---
<h1>Busy Engineers Guide to Deploying on K8s Part 1 - Setting up Docker with GitHub Packages</h1>

Post Valid as of October 12, 2021.

### Busy Engineer's Guide to Deploying On K8s

* [Part 1 - GitHub Packages (this post)](/2021/10/12/busy-engineers-guide-to-deploying-on-k8s-part-1-github-packages.html)
* [Part 2 - Kind ](/2021/10/12/busy-engineers-guide-to-deploying-on-k8s-part-2-kind.html)
* [Part 3 - Helm](/2021/10/12/busy-engineers-guide-to-deploying-on-k8s-part-3-helm.html)


While trying to take some coworkers through setting up Docker with GitHub Packages I ran some not obvious edges and my boss pointed out
for new to Docker and new to Kubernetes people these could be totally derailing corners. I have to agree, so this series will take people front to back
through setting up Kubernetes with the options most readily available to us.

## Why GitHub Packages

Docker is easy right?! While it is easy to push to DockerHub it would require pushing to private repositories on private accounts and getting
access to the company DockerHub account is not as easy as we would hope. I have seen similar in other companies so I do not think it is alone that way for us.
Why not Google, EC2, etc? Same reasons as above. GitHub Packages has the advantage of, if you already have code in GitHub you can now start publishing to docker on 
company resources and really stay on those resources for as long as you need until the company DockerHub opens up for you. Honestly, I have had several projects
canceled before I got access to the company DockerHub, so it ends up being a fatal blocker to our progress. Pragmatically, we can just use GitHub Packages and get on with our lives.


## Why aren't the docs good enough?

I had to go through a few hoops to get a package actually setup and showing in the repository in the GitHub UI. While this is all documented, again I knew where to look and had used
GitHub Packages in an earlier iteration where the documents were honestly clearer to me. Also, the second part of this series will talk about using GitHub Packages with
to Kubernetes. Again something rather basic for existing Kubernetes users, but that seems to be what the docs expect. This goes very quickly off the rails if you change one thing,
and we live in a world where there are plenty of options for everything.

## Getting started 

I am going the easiest route, if you know how to do any of these things any other way, go for it

### Mac and Linux

* Install [Homebrew](https://brew.sh) will we need it for lots of things
* Install [GitHub CLI](https://cli.github.com) with `brew install gh`
* Login to GitHub with `gh auth login` 
* First question `What account do you want to log into?` select the `GitHub.com` option unless your org has an enterprise server and then I can't help you at this time.
* Second question `What is your preferred protocol for Git operations?` select `ssh`
* Select defaults for the rest of the questions and follow the prompts to complete the login

### Optional make a repository and nodejs project

* Create a new repository `gh repo create` 
* "Visibility?" Answer: Private
* "Would you like to add a .gitignore?" Answer: Yes
* "Choose a .gitignore template?" Answer: Node
* "Would you like to add a license?" Answer: Yes (I picked MIT pick your preference)
* "Choose a license MIT License?" Answer: Yes
* "This will create the "..." repository on GitHub. Continue?" Answer: Yes
* "Clone the remote project directory ..?" Answer: Yes
* Install node `brew install nodejs`
* Change to new directory in my case `cd demo-ghpkg`
* Create express site `npx express-generator -f`
* add a Dockerfile to the directory with this content

```
FROM node:16

# Create app directory
WORKDIR /usr/src/app

# Install app dependencies
# A wildcard is used to ensure both package.json AND package-lock.json are copied
# where available (npm@5+)
COPY package*.json ./

RUN npm install
# If you are building your code for production
# RUN npm ci --only=production

# Bundle app source
COPY . .

EXPOSE 3000
CMD [ "npm", "start" ]
```

* create a github action `mkdir -p .github/workflows`
* create the file `touch .github/workflows/deploy-to-ghpkg.yaml`
* add the following content to it

```yaml
name: GH Packages Push

on:
  push:
    # Publish `main` as Docker `latest` image.
    branches:
      - main
      - seed

    # Publish `v1.2.3` tags as releases.
    tags:
      - v*

  # Run tests for any PRs.
  pull_request:

env:
  IMAGE_NAME: app

jobs:
  # Push image to GitHub Packages.
  push:
    runs-on: ubuntu-latest
    permissions:
      packages: write
      contents: read

    steps:
      - uses: actions/checkout@v2

      - name: Build image
        run: docker build . --file Dockerfile --tag $IMAGE_NAME --label "runnumber=${GITHUB_RUN_ID}"

      - name: Log in to registry
        # This is where you will update the PAT to GITHUB_TOKEN
        run: echo "${{ secrets.GITHUB_TOKEN }}" | docker login ghcr.io -u ${{ github.actor }} --password-stdin

      - name: Push image
        run: |
          IMAGE_ID=ghcr.io/${{ github.repository_owner }}/$IMAGE_NAME

          # Change all uppercase to lowercase
          IMAGE_ID=$(echo $IMAGE_ID | tr '[A-Z]' '[a-z]')
          # Strip git ref prefix from version
          VERSION=$(echo "${{ github.ref }}" | sed -e 's,.*/\(.*\),\1,')
          # Strip "v" prefix from tag name
          [[ "${{ github.ref }}" == "refs/tags/"* ]] && VERSION=$(echo $VERSION | sed -e 's/^v//')
          # Use Docker `latest` tag convention
          [ "$VERSION" == "main" ] && VERSION=latest
          echo IMAGE_ID=$IMAGE_ID
          echo VERSION=$VERSION
          docker tag $IMAGE_NAME $IMAGE_ID:$VERSION
          docker push $IMAGE_ID:$VERSION
```
* build the docker file to test docker `build -t app .` if it compiles well you can just skip to the next step
* go and commit all of this with 2 commands `git add -A` and `git commit -am "the first commit`
* push the commit `git push origin main`
* View your repo `gh repo view --web`
* Click on the Actions link, you should see your image being built and pushed
<img title="actions.png" src="/assets/actions.png" border="0" alt="actions" width="600" height="355" />
* After the image is built you can click on the Packages link
<img title="packages.png" src="/assets/packages.png" border="0" alt="packages" width="600" height="355" />

### What did we do

* We installed the github cli
* We created a repository
* We installed nodejs and created an express project in our new repo
* We built a dockerfile and validated it worked
* We added a GitHub action that pushed the docker file on commit to our GitHub Packages
* We committed our changes in Git and pushed them up to GitHub
* We validated the package built and was available in our repository

Follow the [next steps here](/2021/10/12/busy-engineers-guide-to-deploying-on-k8s-part-2-kind.html)
