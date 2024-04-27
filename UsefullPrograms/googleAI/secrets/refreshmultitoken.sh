#!/bin/bash


# Step 1: Run Google Authenticator in the background for AALLL API
(google-oauthlib-tool --client-secrets ~/VASTSYSTEEM/UsefullPrograms/googleAI/secrets/client_secret.json --scope https://www.googleapis.com/auth/contacts --scope https://www.googleapis.com/auth/calendar --scope https://www.googleapis.com/auth/assistant-sdk-prototype --save)&

# Step 3: Run confirm_tokens.py script concurrently
#python3 ~/VASTSYSTEEM/UsefullPrograms/googleAI/secrets/confirm_tokens.py &

# Step 3: Wait for the Google Authenticator to finish
wait

# Step 4: Copy credentials for Google MULTITOKEN
cp ~/.config/google-oauthlib-tool/credentials.json ~/VASTSYSTEEM/UsefullPrograms/googleAI/secrets/multitoken.json



exit 1



