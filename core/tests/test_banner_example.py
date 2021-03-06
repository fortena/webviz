import unittest
import shutil
import os
from os import path
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class TestBannerExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        thisdir = path.abspath(path.dirname(__file__))

        cls.tempdir = tempfile.mkdtemp()
        os.chdir(cls.tempdir)

        exampledir = '{}/../examples/banner_example/'.format(thisdir)

        script = '{0}/banner_example.py'.format(exampledir)
        image = '{0}/test_image.svg'.format(exampledir)
        os.system('python {0} {1}'.format(script, image))

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        cls.driver = webdriver.Chrome(options=options)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tempdir)
        cls.driver.close()

    def setUp(self):
        address = 'file://{}/webviz_example/index.html'.format(self.tempdir)
        self.driver.get(address)

    def test_contains_img(self):
        images = self.driver.find_elements_by_xpath('//img')
        self.assertEqual(len(images), 1)
        location = images[0].get_attribute('src')
        self.assertIn('resources/img/test_image.svg', location)

    def test_file_moved(self):
        self.assertTrue(path.isfile(path.join(
            self.tempdir,
            'webviz_example',
            'resources',
            'img',
            'test_image.svg')))


if __name__ == '__main__':
    unittest.main()
