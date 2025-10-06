from pyngrok import ngrok

# Start a tunnel on port 8000
public_url = ngrok.connect(8000)
print("Public URL:", public_url)

# Keep it running so the tunnel stays active
input("Press ENTER to stop ngrok\n")


#33aq5QpJzTRRD4vSzlZb5UyS6XI_3RQ4b58pS1SruFVWHvtSx -- this is auth token for ngrok