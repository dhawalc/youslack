# YouTubeSlack Notifications

This project automatically sends notifications to a Slack channel when new YouTube videos are uploaded to specified channels.

## Features

- Monitors multiple YouTube channels for new video uploads
- Sends notifications to a Slack channel using a webhook
- Runs automatically every hour using GitHub Actions
- Can be manually triggered through GitHub Actions

## Setup

1. Clone this repository
2. Set up YouTube Data API credentials and obtain an API key
3. Set up a Slack webhook URL for your desired channel
4. Add the YouTube API key and Slack webhook URL as secrets in your GitHub repository settings:
   - YOUTUBE_API_KEY
   - SLACK_WEBHOOK_URL
5. Customize the list of YouTube channel IDs in the `youslack.py` file
6. Push your changes to GitHub

## Usage

The script will run automatically every hour via GitHub Actions. You can also manually trigger it from the Actions tab in your GitHub repository.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
