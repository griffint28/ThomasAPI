import unittest
from unittest.mock import patch
from flask import Flask
from ThomasApiApp.handlers.skillsHandler import skills_bp
from ThomasApiApp.dummy_data import data
import base64


class TestSkillsHandler(unittest.TestCase):

    def setUp(self):
        app = Flask(__name__)
        app.register_blueprint(skills_bp)
        self.app = app.test_client()
        credentials = base64.b64encode(b'user1:password123').decode('utf-8')
        self.valid_auth_header = {
            'Authorization': f'Basic {credentials}',
            'Content-Type': 'application/json'
        }

    @patch('ThomasApiApp.handlers.skillsHandler.requires_auth')
    def test_add_valid_data(self, mock_auth):
        mock_auth.return_value = lambda f: f

        name = "thomas"
        new_skills = {
            "programming": ["Python", "JavaScript", "Java"],
            "frameworks": ["Flask", "Django", "React"],
            "databases": ["PostgreSQL", "MongoDB"]
        }

        if name not in data:
            data[name] = {}

        response = self.app.post(f'/{name}/skills',
                                 json=new_skills,
                                 headers=self.valid_auth_header)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"message": "Information added successfully"})
        self.assertEqual(data[name]["skills"], new_skills)

    @patch('ThomasApiApp.handlers.skillsHandler.requires_auth')
    def test_add_no_data(self, mock_auth):
        mock_auth.return_value = lambda f: f

        name = "test_user_no_data"

        response = self.app.post(f'/{name}/skills',
                                 json={},
                                 headers=self.valid_auth_header)

        self.assertEqual(response.status_code, 400)
        self.assertIn("No data provided in request body.", response.data.decode())

    @patch('ThomasApiApp.handlers.skillsHandler.requires_auth')
    def test_get_valid_data(self, mock_auth):
        mock_auth.return_value = lambda f: f
        name = "thomas"
        test_data = {
            "programming": ["Python", "Java"],
            "tools": ["Git", "Docker"]
        }
        data[name] = {"skills": test_data}

        response = self.app.get(f'/{name}/skills',
                                headers=self.valid_auth_header)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, test_data)

if __name__ == '__main__':
    unittest.main()
