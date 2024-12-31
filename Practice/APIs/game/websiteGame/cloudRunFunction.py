"""
This module contains a Google Cloud Function to stop all versions of a Flask app running on Google App Engine.
The function is triggered via an HTTP request and is intended to be used when a budget limit is reached.
Functions:
    stop_flask_app(request): Stops all versions of a specified service in a Google App Engine app.
Usage:
    Deploy this function to Google Cloud Functions and configure it to be triggered by an HTTP request.
    Ensure that the necessary permissions are granted to the service account running this function.
Configuration:
    - app_id: The App ID of your Google App Engine application.
    - service_name: The name of the service whose versions you want to stop.
"""
from google.cloud import appengine_admin_v1
import functions_framework

@functions_framework.http
def stop_flask_app(request):
    """Stops all versions of a Flask app on Google App Engine when a budget limit is reached."""
    
    # Configuration
    app_id = "genai-game-446310"  # Replace with your App ID
    service_name = "default"  # Replace with your service name

    # Initialize the client
    client = appengine_admin_v1.VersionsClient()

    try:
        # Get the list of versions for the specified service
        parent = f"apps/{app_id}/services/{service_name}"
        versions = client.list_versions(parent=parent)

        # Delete all versions
        for version in versions:
            client.delete_version(name=version.name)

        return f"Successfully stopped all versions of service '{service_name}' in app '{app_id}'.", 200

    except Exception as e:
        return f"Error stopping Flask app: {e}", 500
