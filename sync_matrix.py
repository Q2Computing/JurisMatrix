import json
import urllib.request
import sys

VERSION_URL = "https://www.ecfr.gov/api/versioner/v1/versions/title-15.json"

def verify_source_of_truth():
    try:
        req = urllib.request.Request(
            VERSION_URL, 
            headers={'User-Agent': 'JurisMatrix-ComplianceBot/1.0'}
        )
        # Enforce a strict timeout so it fails fast if disconnected
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status != 200:
                raise Exception(f"Source responded with status code {response.status}")
            data = json.loads(response.read().decode())
            print("Successfully verified connection to eCFR source of truth.")
            return True
    except Exception as e:
        print(f"CRITICAL COMPLIANCE FAILURE: Cannot reach eCFR source of truth. Error: {e}")
        # Return false to trigger deployment halt
        return False

if __name__ == "__main__":
    is_connected = verify_source_of_truth()
    if not is_connected:
        print("HALTING DEPLOYMENT: Source of truth verification failed. Failing closed.")
        sys.exit(1) # Non-zero exit code kills the GitHub Actions workflow
    else:
        sys.exit(0)
