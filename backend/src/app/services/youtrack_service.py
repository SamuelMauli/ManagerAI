# Add these functions to your existing youtrack_service.py

def get_pending_tasks_count(self):
    """
    Returns the count of pending tasks assigned to the user.
    This is an example, you'll need to adjust the query for your YouTrack setup.
    """
    # Example query: find issues that are not resolved and are assigned to me.
    query = "for: me state: -Resolved" 
    try:
        issues = self.youtrack_client.get_issues(query=query, size=100)
        return len(issues)
    except Exception as e:
        print(f"Error fetching YouTrack tasks: {e}")
        return 0 # Return 0 if there's an error

def get_active_projects_count(self):
    """
    Returns the count of all accessible projects.
    """
    try:
        projects = self.youtrack_client.get_projects()
        return len(projects)
    except Exception as e:
        print(f"Error fetching YouTrack projects: {e}")
        return 0
        
def get_all_projects(self):
    """
    Returns a list of all accessible projects.
    """
    try:
        return self.youtrack_client.get_projects()
    except Exception as e:
        print(f"Error fetching YouTrack projects: {e}")
        return []