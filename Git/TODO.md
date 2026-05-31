# TODO for Git

CI/CD & GitHub Actions Automation
Instead of manual deployments, advanced developers use GitHub Actions to automate testing, building, and deploying. 

    Reusable Workflows: Create centralized CI/CD workflows that multiple repositories can share, reducing duplication.
    Self-Hosted Runners: Set up and manage dedicated servers for running GitHub Actions to build massive projects securely.
    Custom Action Development: Write custom actions using JavaScript or Docker to handle highly specific, custom build steps. 
  
Infrastructure as Code (IaC) & Environments
Advanced developers treat environments as code to guarantee consistency across development, staging, and production.

    Environment Protection Rules: Set up required reviewers, wait timers, and deployment branches to ensure no code reaches production without human approval.
    Repository Variables and Secrets: Use GitHub’s built-in environment secrets to securely inject API keys and tokens during automated deployments. 
    
Advanced Git & Repository Hygiene
Knowing how to commit is basic; keeping your repository’s history clean and isolated is advanced.

    Git Worktrees: Manage multiple branches simultaneously in the same local repository without needing to clone the project multiple times.
    .git-blame-ignore-revs: Maintain clean commit history by telling GitHub to ignore auto-formatted or bulky code-style commits when viewing git blame.
    Complex Rebase and Cherry-Picking: Rewrite commit history to squash, split, or organize commits before merging into the main branch.
    
Security & Compliance
As software supply chains grow more complex, securing your code directly on GitHub is paramount. 
Secret Scanning & Dependabot: Configure GitHub to actively prevent committing exposed API keys and automatically create pull requests to update vulnerable dependencies.
CodeQL and Security Policies: Implement CodeQL to run semantic code analysis, catching vulnerabilities, SQL injections, and logic bugs before they leave the pull request phase
