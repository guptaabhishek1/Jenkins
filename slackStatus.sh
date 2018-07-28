MESSAGE=$1
COLOR_CODE=$2

# Changses 
EMOJI="${2:-gherkin}"
SLACK_CHANNEL="#test"
SLACK_HOOK="https://hooks.slack.com/services/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"
USERNAME="Jenkins"

# Dont not change anything from here 
# console logging
echo -e "SLACK MESSAGE: $MESSAGE\nSLACK EMOJI: $EMOJI\nSLACK_CHANNEL: $SLACK_CHANNEL\n COLOR:$COLOR_CODE"

# send the notification
curl -v \
-H "Accept: application/json" \
-H "Content-Type:application/json" \
-X POST --data '{"channel": "'"$SLACK_CHANNEL"'", "username": "'"$USERNAME"'", "attachments": [{"color": "'"$COLOR_CODE"'", "text": "'"$MESSAGE"'"}]}' $SLACK_HOOK
