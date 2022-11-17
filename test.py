import unittest
import ProjectV1
import requests

class ProjectTest:
    def test_index(self):
        response = requests.get("http://127.0.0.1:5000/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('<h2>This site is used to manage and organize Tasks and Projects</h2>' in response.text, True)

    def test_delete_method(self):
        self.assertEqual(len(ProjectV1.projects), 3)
        ProjectV1.delete_project(1)
