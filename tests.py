import os

os.environ["DATABASE_URL"] = "postgresql:///blogly_test"

from unittest import TestCase

from app import app, db
from models import User, Post
# DEFAULT_IMAGE_URL

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        Post.query.delete()
        User.query.delete()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )
        db.session.add(test_user)
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id


        test_post = Post(
            title = "test_title",
            content = "test_content: story about a cat",
            user_id = self.user_id
        )

        db.session.add(test_post)
        db.session.commit()

        self.post_id = test_post.id

        print(self.post_id, "post-id")
        print(self.user_id, "user-id")


    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        """Test for showing all users"""
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)


    def test_users_page_redirection(self):
        """ Test for redirection to users page"""
        with app.test_client() as client:
            resp = client.get("/")

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/users")

    def test_users_redirection_followed(self):
        """ Tests the follow redirection"""
        with app.test_client() as client:
            resp = client.get("/", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)

    def test_user_page(self):
        """Tests that specific user's page renders"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertIn("user page renders correctly!", html)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("test_title", html)


    def test_delete_user(self):
        """Tests that user is deleted"""
        with app.test_client() as client:
            resp = client.post(f"/users/{self.user_id}/delete",
                               follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("test1_first", html)
            self.assertNotIn("test1_last", html)

    def test_new_blog_post_form(self):
        """Tests for new post form rendition"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/posts/new")

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("new post form renders correctly!", html)

    def test_blog_post_page(self):
        """Tests for specific post page rendition"""
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("test_content: story about a cat", html)

    def test_blog_post_edit_page(self):
        """Test for specific post edit page"""
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}/edit")

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("test_title", html)

    def test_delete_blog_post_redirection(self):
        """Test for redirection when deleting post"""
        with app.test_client() as client:
            resp = client.post(f"/posts/{self.post_id}/delete",
                               follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("test_title", html)