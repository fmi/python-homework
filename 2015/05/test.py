import time
import errno
import socket
import unittest
import threading
import http.server
import urllib.parse
import socketserver

import solution

class TestHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):

    def __init__(self, *args, **kwargs):
        http.server.HTTPServer.__init__(self, *args, **kwargs)
        self.responses = {}
        self.touched_paths = []
        self._mx = threading.Lock()

    def add_to_touched(self, path):
        with self._mx:
            self.touched_paths.append(path)

    def is_touched(self, path):
        with self._mx:
            res = path in self.touched_paths
        return res

    def finish_request(self, *args):
        try:
            http.server.HTTPServer.finish_request(self, *args)
        except socket.error as err:
            if err.errno in [errno.EPIPE, errno.ECONNRESET]:
                return
            raise err

class TestHTTPHandler(http.server.BaseHTTPRequestHandler):
    
    def do_GET(self):
        self.server.add_to_touched(self.path)
        self.defalt_headers()

        if not hasattr(self.server, 'responses'):
            return self.end_with_not_found()

        if self.path not in self.server.responses:
            return self.end_with_not_found()

        response = self.server.responses[self.path]

        if callable(response):
            response(self)
            return

        self.send_header('Content-Type', 'text/plain')
        self.send_response(200)
        self.end_headers()

        self.wfile.write(bytes(response, 'UTF-8'))

    def end_with_not_found(self):
        self.send_response(404)
        self.end_headers()

    def log_request(self, *args, **kwargs):
        pass

    def defalt_headers(self):
        self.send_header('Connection', 'close')


def contains_callback(search_for):
    def contains(string):
        return str(string).find(search_for) != -1
    return contains

def always_true(string):
    return True

def always_false(string):
    return False
        
def sleep_func(output, sleep_time):
    '''
    Used to simulate a HTTP rqeuest which takes some time.
    '''
    def with_sleep(hndl):
        hndl.send_response(200)
        hndl.end_headers()
        time.sleep(sleep_time)
        hndl.wfile.write(bytes(output, 'UTF-8'))
    return with_sleep


def test_timeout(seconds):
    '''
    There will be quite a lot deadlocks in the tested solutions.
    We will use this decorator in order to set maximum running time of a test.
    This way a deadlock will not stop the whole test.
    '''
    def timed_out_test(test_func):
        def decorated_test(self):
            test_thread = threading.Thread(target=test_func, args=(self,))
            test_thread.daemon = True
            test_thread.start()
            test_thread.join(seconds)
            self.assertFalse(test_thread.is_alive(), 
                'Test took too long: %ds' % seconds)

        # We set the name of the function to be the same as the decorated one
        # becaue unittest calls its tests with it.
        decorated_test.__name__ = test_func.__name__
        return decorated_test
    return timed_out_test


class TestCrawler(unittest.TestCase):
    '''
        Finally! The tests themselves. We set up a local HTTP server over which
        we have full control. That way we are sure the test will not be a subject
        to network errors and slow downs.
    '''
    
    def setUp(self):
        self.httpd = TestHTTPServer(('', 0), TestHTTPHandler)
        self.httpd_thread = threading.Thread(target=self.httpd.serve_forever)
        self.httpd_thread.start()

    def tearDown(self):
        self.httpd.shutdown()
        self.httpd_thread.join()

    def server_address(self):
        return 'http://%s:%d/' % (self.httpd.server_name, self.httpd.server_port)

    def path_to_url(self, path):
        return urllib.parse.urljoin(self.server_address(), path)

    @test_timeout(4)
    def test_no_result(self):

        contains_luck = contains_callback('You are lucky, FMI python 2015')

        urls = map(self.path_to_url, ["/1", "/2", "wrong.url!", "/3", "/5",])

        result = solution.crawler(iter(urls), contains_luck, 4)

        self.assertIsNone(result, ('Did not expect the string "you are '
                                    'lucky" in any of the URLs'))

    @test_timeout(4)
    def test_simple_operation(self):
        self.httpd.responses = {
            '/path1': 'Hello, lonely! How are you today?'
        }
        success_url = self.path_to_url('/path1')

        work_urls = [
            self.path_to_url('/path-not-here'),
            success_url,
            self.path_to_url('/ops'),
        ]

        callback = contains_callback('How are you today?')
        result = solution.crawler(iter(work_urls), callback, 3)
        self.assertEqual(result, success_url)

    @test_timeout(4)
    def test_wrong_arguments_passed(self):
        with self.assertRaises(Exception):
            solution.crawler(iter([]), always_false, -1)

        with self.assertRaises(Exception):
            solution.crawler(iter([]), always_false, 0)

        with self.assertRaises(Exception):
            solution.crawler(iter(['http://google.com']), None, 3)

        with self.assertRaises(Exception):
            solution.crawler(None, always_false, 3)

    @test_timeout(4)
    def test_with_non_2xx_responses(self):

        search_for = 'some string'
        server_response = 'There should be some string in here'

        def create_err_handler(status_code):
            def error_handler(hndl):
                hndl.send_response(status_code)
                hndl.end_headers()
            return error_handler
        
        def return_409_and_the_string(hndl):
            hndl.send_response(409)
            hndl.end_headers()
            hndl.wfile.write(bytes(server_response, 'UTF-8'))

        self.httpd.responses = {
            '/500': create_err_handler(500),
            '/504': create_err_handler(504),
            '/401': create_err_handler(401),
            '/416': create_err_handler(416),
            '/409': return_409_and_the_string,
            '/bingo': server_response,
        }

        urls = [self.path_to_url(path) for path in self.httpd.responses]

        result = solution.crawler(iter(urls), contains_callback(search_for), 5)
        self.assertEqual(result, self.path_to_url('/bingo'))

    @test_timeout(8)
    def test_crawling_stops_after_successful_callback(self):
        search_for = 'Ame-no-Murakumo-no-Tsurugi'
        server_response = 'Ame-no-Murakumo-no-Tsurugi was given to the warrior'
        success_path = '/kusanagi'

        touched = []
        not_touched = []
        urls = []

        for i in range(10):
            path = '/touched-{0}'.format(i)
            self.httpd.responses[path] = 'Nothing to see here'
            urls.append(self.path_to_url(path))
            touched.append(path)

        self.httpd.responses[success_path] = server_response
        urls.append(self.path_to_url(success_path))
        touched.append(success_path)

        for i in range(10):
            path = '/not-touched-{0}'.format(i)
            self.httpd.responses[path] = 'Nothing to see here'
            urls.append(self.path_to_url(path))
            not_touched.append(path)

        result = solution.crawler(iter(urls), contains_callback(search_for), 2)
        self.assertEqual(result, self.path_to_url(success_path))

        for path in touched:
            self.assertTrue(self.httpd.is_touched(path), 
                'crawler did not check {0}'.format(path))

        # There might be up to 2 (workers_count) urls visited before the crawler 
        # returns.
        for path in not_touched[2:]:
            self.assertFalse(self.httpd.is_touched(path), 
                'crawler did check `{0}` when it was not supposed to'.format(path))

    @test_timeout(2)
    def test_empty_iterator(self):
        result = solution.crawler(iter([]), always_true, 4)
        self.assertIsNone(result)

    @test_timeout(4)
    def test_only_one_worker(self):

        self.httpd.responses = {
            '/500': 'cuddly',
            '/504': 'little',
            '/401': 'cat',
            '/416': 'which',
            '/409': 'eats',
            '/bingo': 'mice',
            '/355': 'but',
            '/356': 'likes',
            '/357': 'fish',
            '/358': 'too',
        }

        urls = [self.path_to_url(path) for path in self.httpd.responses]
        result = solution.crawler(iter(urls), contains_callback('mice'), 1)
        self.assertEqual(result, self.path_to_url('/bingo'))

    @test_timeout(10)
    def test_if_concurrent_with_sleep_in_server(self):
        '''
        All responsens will be ~1 second long. If the solution is not concurrent
        and it tried all URLs in turns it should have been working for more than 2
        seconds since there are at least 2 URLs in the work queue.
        '''
        urls = []
        concurrency = 5
        
        def with_sleep(hndl):
            hndl.send_response(404)
            hndl.end_headers()
            time.sleep(0.5)
            hndl.wfile.write(bytes('not what you are searching for', 'UTF-8'))

        for i in range(concurrency):
            path = '/not-there-{0}'.format(i)
            self.httpd.responses[path] = with_sleep
            urls.append(self.path_to_url(path))

        success_path = '/bingo'
        success_url = self.path_to_url(success_path)

        self.httpd.responses[success_path] = 'I made in less than 5 seconds'
        urls.append(success_url)

        callback = contains_callback('less than 5')

        start = time.time()
        result = solution.crawler(iter(urls), callback, concurrency)
        took = time.time() - start

        self.assertEqual(result, success_url)
        msg = ('This crawler is probably not an concurrent one.')
        self.assertTrue(took < 1, msg)

    @test_timeout(30)
    def test_timeout_value(self):
        urls = []
        concurrency = 2
        
        def with_sleep(hndl):
            hndl.send_response(200)
            hndl.end_headers()
            time.sleep(4)
            hndl.wfile.write(bytes('I made in less than 5 seconds', 'UTF-8'))

        for i in range(concurrency):
            path = '/timeout-{0}'.format(i)
            self.httpd.responses[path] = with_sleep
            urls.append(self.path_to_url(path))

        success_path = '/bingo'
        success_url = self.path_to_url(success_path)

        self.httpd.responses[success_path] = 'I made in less than 5 seconds'
        urls.append(success_url)

        callback = contains_callback('less than 5')

        start = time.time()
        result = solution.crawler(iter(urls), callback, concurrency)
        took = time.time() - start

        self.assertEqual(result, success_url, 'Crawler did not timeout')
        msg = ('This crawler is probably not an concurrent one.')
        self.assertTrue(took < 5, msg)

    @test_timeout(4)
    def test_when_callback_never_returns_true(self):

        self.httpd.responses = {
            '/500': 'cuddly',
            '/504': 'little',
            '/401': 'cat',
            '/416': 'which',
            '/409': 'eats',
            '/bingo': 'mice',
            '/355': 'but',
            '/356': 'likes',
            '/357': 'fish',
            '/358': 'too',
        }

        urls = [self.path_to_url(path) for path in self.httpd.responses]
        result = solution.crawler(iter(urls), always_false, 3)
        self.assertIsNone(result)

    @test_timeout(15)
    def test_race_condition(self):
        urls = []
        search_string = 'success'

        path = '/failure'
        self.httpd.responses[path] = 'failure'
        urls.append(self.path_to_url(path))

        path = '/slow_success'
        self.httpd.responses[path] = sleep_func(search_string, 1)
        urls.append(self.path_to_url(path))

        path = '/fast_success'
        self.httpd.responses[path] = sleep_func(search_string, 0.5)
        expected_result = self.path_to_url(path)
        urls.append(expected_result)

        callback = contains_callback(search_string)

        result = solution.crawler(iter(urls), callback, 3)
        self.assertEqual(result, expected_result)

    @test_timeout(10)
    def test_race_condition_with_timeout(self):
        urls = []
        search_string = 'success'

        path = '/timed_out_success'
        self.httpd.responses[path] = sleep_func(search_string, 4)
        urls.append(self.path_to_url(path))

        path = '/slow_success'
        self.httpd.responses[path] = sleep_func(search_string, 2)
        urls.append(self.path_to_url(path))

        for i in range(5):
            path = '/not_success_{0}'.format(i)
            self.httpd.responses[path] = 'nothing to see here'
            urls.append(self.path_to_url(path))

        path = '/fast_success'
        self.httpd.responses[path] = search_string
        expected_result = self.path_to_url(path)
        urls.append(expected_result)

        callback = contains_callback(search_string)

        result = solution.crawler(iter(urls), callback, 3)
        self.assertEqual(result, expected_result)

    @test_timeout(8)
    def test_with_many_wrong_urls(self):
        success_path = '/success'
        self.httpd.responses[success_path] = 'first not wrong url'

        urls = [self.path_to_url('/not-found-{0}'.format(i)) for i in range(15)]

        urls += ["wrong.url!", "python://almost-an-URL", "http://almost-a-domain"]

        success_url = self.path_to_url(success_path)
        urls.append(success_url)

        callback = contains_callback('not wrong')
        result = solution.crawler(iter(urls), callback, 5)
        self.assertEqual(result, success_url)

    @test_timeout(10)
    def test_crawler_starts_no_more_than_expected_workers(self):

        urls = []

        for i in range(5):
            path = '/not_success_{0}'.format(i)
            self.httpd.responses[path] = sleep_func('nothing to see here', 0.100)
            urls.append(self.path_to_url(path))

        start = time.time()
        result = solution.crawler(iter(urls), always_false, 4)
        took = time.time() - start

        self.assertIsNone(result)
        # if the time is less than 200ms it meas there have been more than 4 workers
        self.assertTrue(took >= 0.200, 'crawler spawned more workers than expected')


if __name__ == '__main__':
    unittest.main()
