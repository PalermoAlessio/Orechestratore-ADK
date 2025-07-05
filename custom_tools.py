from google.adk.tools.base_tool import BaseTool
from google.adk.tools import google_search as adk_google_search

class CustomGoogleSearchTool(BaseTool):
    name: str = "google_search"
    description: str = "A custom tool for performing Google web searches."

    def search(self, query: str) -> str:
        return adk_google_search.invoke(query)

custom_google_search = CustomGoogleSearchTool(name="custom_google_search", description="A custom tool for performing Google web searches.")