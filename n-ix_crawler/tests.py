import json
import sys
import unittest

from github_crawler import get_extra, get_input, get_urls, main, parse_repo, write_results


class TestCrawlerWikis(unittest.TestCase):
    def setUp(self):
        self.keywords = ["python", "redis", "django"]
        self.obj_type = "Wikis"
        self.urls = get_urls(self.keywords, self.obj_type)
        self.result_wikis = [
            {
                "url": "https://github.com/balakrishnanm/mybook/wiki/Python-Django"
            },
            {
                "url": "https://github.com/alibond/appunti.italiadigitale.docs/wiki/Django"
            },
            {
                "url": "https://github.com/victorhooi/victorwiki/wiki/django"
            },
            {
                "url": "https://github.com/kailiu-unsw/python/wiki/Django"
            },
            {
                "url": "https://github.com/cfbatalla/LenguajesDeAltoNivel/wiki/Django"
            }
        ]

    def test_get_urls_return_type_wikis(self):
        self.assertIsInstance(self.urls, list)

    def test_get_urls_return_member_type_wikis(self):
        if len(self.urls) > 0:
            self.assertIsInstance(self.urls[0], dict)

    def test_get_urls_return_member_type_keys_wikis(self):
        if self.urls:
            self.assertIn('url', self.urls[0])

    def test_get_urls(self):
        urls = get_urls(self.keywords, self.obj_type)
        self.assertTrue(urls)

    def test_write_results(self):
        write_results(self.result_wikis)
        with open('result.json', 'r') as f:
            contents = f.read()
            self.assertEqual(json.loads(contents), self.result_wikis)

    def test_get_input_type(self):
        with open('input.json', 'r') as f:
            content = f.read()
            self.assertIsInstance(get_input(content), tuple)

    def test_get_input_len(self):
        with open('input.json', 'r') as f:
            content = f.read()
            self.assertEqual(len(get_input(content)), 3)

    def test_main(self):
        with open('input.json', 'r') as f:
            sys.stdin = f
            self.assertEqual(main(), None)


class TestCrawlerRepos(unittest.TestCase):
    def setUp(self):
        self.keywords = ["python", "redis", "django"]
        self.obj_type = "Repositories"
        self.urls = get_urls(self.keywords, self.obj_type)
        self.result_repos = [
            {
                "url": "https://github.com/fabiocaccamo/django-freeze",
                "extra": {
                    "owner": "fabiocaccamo",
                    "language_stats": {
                        "Python": 94.7,
                        "HTML": 3.3,
                        "JavaScript": 2.0
                    }
                }
            },
            {
                "url": "https://github.com/Anupam-dagar/Portfolio-Generator",
                "extra": {
                    "owner": "Anupam-dagar",
                    "language_stats": {
                        "Python": 56.7,
                        "JavaScript": 27.7,
                        "HTML": 15.6
                    }
                }
            },
            {
                "url": "https://github.com/justdjango/Shopping_cart",
                "extra": {
                    "owner": "justdjango",
                    "language_stats": {
                        "JavaScript": 48.3,
                        "CSS": 30.1,
                        "Python": 12.8,
                        "HTML": 8.8
                    }
                }
            }
        ]

    def test_get_url_return_type_repos(self):
        self.assertIsInstance(self.urls, list)

    def test_get_url_return_member_type_repos(self):
        if len(self.urls) > 0:
            self.assertIsInstance(self.urls[0], dict)

    def test_get_url_return_member_type_has_key_urls(self):
        if len(self.urls) > 0:
            self.assertIn('url', self.urls[0])

    def test_parse_repo_result_type(self):
        if self.urls:
            result = parse_repo(self.urls[0].get('url'))
            self.assertIsInstance(result, dict)

    def test_parse_repo_result_has_key_urls(self):
        if self.urls:
            result = parse_repo(self.urls[0].get('url'))
            self.assertIn('url', result)

    def test_parse_repo_result_has_key_extra(self):
        if self.urls:
            result = parse_repo(self.urls[0].get('url'))
            self.assertIn('extra', result)

    def test_parse_repo_result_extra_has_key_owner(self):
        if self.urls:
            result = parse_repo(self.urls[0].get('url'))
            self.assertIn('owner', result.get('extra'))

    def test_parse_repo_result_extra_has_key_language_stats(self):
        if self.urls:
            result = parse_repo(self.urls[0].get('url'))
            self.assertIn('language_stats', result.get('extra'))

    def test_get_extra_return_type(self):
        results = get_extra(self.urls, 'Repositories')
        self.assertIsInstance(results, list)

    def test_get_extra_return_member_type(self):
        results = get_extra(self.urls, 'Repositories')
        if len(results) > 0:
            self.assertIsInstance(results[0], dict)

    def test_get_extra_result_has_key_urls(self):
        results = get_extra(self.urls, 'Repositories')
        self.assertIn('url', results[0])

    def test_get_extra_result_has_key_extra(self):
        results = get_extra(self.urls, 'Repositories')
        self.assertIn('extra', results[0])

    def test_get_extra_result_extra_has_key_owner(self):
        results = get_extra(self.urls, 'Repositories')
        self.assertIn('owner', results[0].get('extra'))

    def test_get_extra_result_extra_has_key_language_stats(self):
        results = get_extra(self.urls, 'Repositories')
        self.assertIn('language_stats', results[0].get('extra'))

    def test_write_results(self):
        write_results(self.result_repos)
        with open('result.json', 'r') as f:
            contents = f.read()
            self.assertEqual(json.loads(contents), self.result_repos)


class TestCrawlerIssues(unittest.TestCase):
    def setUp(self):
        self.keywords = ["python", "redis", "django"]
        self.obj_type = "Issues"
        self.urls = get_urls(self.keywords, self.obj_type)
        self.result_issues = [
            {"url": "https://github.com/andreagrandi/covid-api/issues/1"},
            {"url": "https://github.com/Prefeitura-Comunica/thread/issues/3"},
            {"url": "https://github.com/deity-io/falcon/issues/770"},
            {"url": "https://github.com/zgq105/blog/issues/80"}
        ]

    def test_get_url_issues(self):
        self.assertIsInstance(self.urls, list)

    def test_get_url_member_type_issues(self):
        if self.urls:
            self.assertIsInstance(self.urls[0], dict)

    def test_get_url_return_member_type_keys_issues(self):
        if self.urls:
            self.assertIn('url', self.urls[0])

    def test_write_results(self):
        write_results(self.result_issues)
        with open('result.json', 'r') as f:
            contents = f.read()
            self.assertEqual(json.loads(contents), self.result_issues)


if __name__ == '__main__':
    unittest.main()
