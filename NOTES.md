# Notes
Some notes to myself as I'm developing this.

## OAuth & Authentication
- I feel like I want some sort of double authentication; oAuth at the server level, and something at the network level (like an API key implemented by tailscale funnel) to stop malicious traffic from even discovering my endpoint, or DDOSing it.


## Why google OAuth?
I use it to secure all my admin endpoints in the public cloud. Their infrastructure is set up to handle the threats of th public web, and it's a widely used identify provider that I trust (and is free).
