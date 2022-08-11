
from urllib.robotparser import RobotFileParser

class CustomRobotParser(RobotFileParser):
    def read_file(self, webdriver):
        """Reads the robots.txt URL with Selenium and feeds it to the parser."""
        webdriver.get(self.url)
        page_source = webdriver.page_source
        self.parse(page_source.splitlines())