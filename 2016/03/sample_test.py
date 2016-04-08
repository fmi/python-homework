import datetime
import unittest

import solution


class TestSocialGraph(unittest.TestCase):
    def setUp(self):
        self.terry = solution.User("Terry Gilliam")
        self.eric = solution.User("Eric Idle")
        self.graham = solution.User("Graham Chapman")
        self.john = solution.User("John Cleese")
        self.michael = solution.User("Michael Palin")
        self.graph = solution.SocialGraph()
        self.graph.add_user(self.terry)
        self.graph.add_user(self.eric)
        self.graph.add_user(self.graham)
        self.graph.add_user(self.john)
        self.graph.add_user(self.michael)

    def test_add_get_and_delete_user(self):
        with self.assertRaises(solution.UserAlreadyExistsError):
            self.graph.add_user(self.terry)
        self.graph.delete_user(self.terry.uuid)
        self.graph.add_user(self.terry)
        self.assertEqual(self.graph.get_user(self.terry.uuid), self.terry)

    def test_following(self):
        self.graph.follow(self.terry.uuid, self.eric.uuid)
        self.assertTrue(
            self.graph.is_following(self.terry.uuid, self.eric.uuid))
        self.assertFalse(
            self.graph.is_following(self.eric.uuid, self.terry.uuid))

    def test_friends(self):
        self.graph.follow(self.terry.uuid, self.eric.uuid)
        self.assertNotIn(self.eric.uuid, self.graph.friends(self.terry.uuid))
        self.assertNotIn(self.terry.uuid, self.graph.friends(self.eric.uuid))
        self.graph.follow(self.eric.uuid, self.terry.uuid)
        self.assertIn(self.eric.uuid, self.graph.friends(self.terry.uuid))
        self.assertIn(self.terry.uuid, self.graph.friends(self.eric.uuid))


class TestUser(unittest.TestCase):
    def setUp(self):
        self.michael = solution.User("Michael Palin")

    def test_has_uuid(self):
        self.assertIsNotNone(getattr(self.michael, 'uuid'))

    def test_add_post(self):
        self.michael.add_post("larodi")
        post = next(self.michael.get_post())
        self.assertEqual(post.author, self.michael.uuid)
        self.assertEqual(post.content, "larodi")
        self.assertTrue(isinstance(post.published_at, datetime.datetime))

if __name__ == '__main__':
    unittest.main()
