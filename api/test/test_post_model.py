import unittest
from uuid import uuid4
from datetime import datetime

from zimmerman.main import db
from zimmerman.main.model.main import Post, User
from zimmerman.test.base import BaseTestCase


class TestPostModel(BaseTestCase):
    def test_create_post(self):
        """ Test for post model """

        # Create test user
        user = User(
            public_id=str(uuid4().int)[:15],
            email="email@test.com",
            username="testUser",
            full_name="Test User",
            password="test1234",
            joined_date=datetime.utcnow(),
        )

        db.session.add(user)
        db.session.commit()

        # Create post
        post = Post(
            owner_id=user.id,
            creator_public_id=user.public_id,
            content="Test content",
            image_file="",
            status="normal",
        )

        db.session.add(post)
        db.session.commit()

        self.assertTrue(isinstance(post, Post))


if __name__ == "__main__":
    unittest.main()
