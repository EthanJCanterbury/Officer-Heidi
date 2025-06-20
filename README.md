
# Officer Heidi - AI Code Detection Slack Bot

Officer Heidi is a Slack bot designed to analyze GitHub repositories and detect potentially AI-generated code to help prevent fraud.

## Features

- 🔍 Analyzes GitHub repositories for AI-generated code patterns
- 📊 Calculates comment-to-code ratios
- 🤖 Provides AI likelihood scores (Not AI, Maybe AI, Probly AI, Definitly AI)
- 📝 Shows recent commit history
- 👤 Analyzes repository owner's GitHub account age
- ⚠️ Flags suspicious patterns and new accounts

## Setup Instructions

### 1. Create Slack App

1. Go to [Slack API Apps](https://api.slack.com/apps)
2. Click "Create New App"
3. Choose "From an app manifest"
4. Select your workspace
5. Copy and paste the contents of `manifest.json`
6. Click "Create"
7. Click "Install to Workspace"

### 2. Get Required Tokens

After creating your Slack app, you'll need these tokens:

**SLACK_BOT_TOKEN:**
- Go to your app's "OAuth & Permissions" page
- Copy the "Bot User OAuth Token" (starts with `xoxb-`)

**SLACK_APP_TOKEN:**
- Go to your app's "Basic Information" page
- Scroll to "App-Level Tokens"
- Click "Generate Token and Scopes"
- Add `connections:write` scope
- Copy the token (starts with `xapp-`)

**SLACK_SIGNING_SECRET:**
- Go to your app's "Basic Information" page
- Find "Signing Secret" in the "App Credentials" section

### 3. Set Environment Variables in Replit

Go to the Secrets tab in your Replit workspace and add:

- `SLACK_BOT_TOKEN`: Your bot token from step 2
- `SLACK_APP_TOKEN`: Your app token from step 2
- `SLACK_SIGNING_SECRET`: Your signing secret from step 2

### 4. Deploy

Click the "Deploy" button in Replit and choose "Reserved VM Deployment" to keep the bot running 24/7.

## Usage

In any Slack channel where the bot is invited, use:

```
/heidi-check https://github.com/username/repository
```

Officer Heidi will analyze the repository and provide a detailed report including:

- Repository owner information and account age
- Code analysis metrics
- AI likelihood assessment
- Recent commit history
- Suspicious file identification

## AI Detection Methodology

Officer Heidi uses multiple detection methods:

1. **Pattern Recognition**: Looks for common AI-generated code patterns
2. **Comment Analysis**: Analyzes comment-to-code ratios
3. **Structure Analysis**: Detects overly structured or repetitive code
4. **Temporal Analysis**: Considers account age and commit patterns
5. **Linguistic Analysis**: Identifies AI-typical comments and documentation

## Fraud Prevention Use Cases

- Hiring verification (checking candidate's code authenticity)
- Code review assistance
- Academic integrity monitoring
- Contest/competition verification
- General due diligence for code authenticity
