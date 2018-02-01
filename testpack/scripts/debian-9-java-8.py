#!/usr/bin/env python3

import unittest
import os
import docker
from selenium import webdriver


class Test1and1Java8Image(unittest.TestCase):
    docker_container = None
    container_ip = None

    @classmethod
    def setUpClass(cls):
        image_to_test = os.getenv("IMAGE_NAME")
        if image_to_test == "":
            raise Exception("I don't know what image to test")
        client = docker.from_env()
        Test1and1Java8Image.container = client.containers.run(
            image=image_to_test,
            remove=True,
            detach=True,
            network_mode="bridge",
            user=10000,
            ports={8080:8080},
            working_dir="/var/www"
        )

        details = docker.APIClient().inspect_container(container=Test1and1Java8Image.container.id)
        Test1and1Java8Image.container_ip = details['NetworkSettings']['IPAddress']

    @classmethod
    def tearDownClass(cls):
        Test1and1Java8Image.container.stop()

    def setUp(self):
        print ("\nIn method", self._testMethodName)
        self.container = Test1and1Java8Image.container

    def execRun(self, command):
        result = self.container.exec_run(command)
        if isinstance(result, tuple):
            exit_code = result[0]
            output = result[1].decode('utf-8')
        else:
            output = result.decode('utf-8')
        return output

    def assertPackageIsInstalled(self, packageName):
        op = self.execRun("dpkg -l %s" % packageName)
        self.assertTrue(
            op.find(packageName) > -1,
            msg="%s package not installed" % packageName
        )

    # <tests to run>

    def test_docker_logs(self):
        expected_log_lines = [
            "Process 'java_server_runner' changed state to 'RUNNING'"
        ]
        container_logs = self.container.logs().decode('utf-8')
        for expected_log_line in expected_log_lines:
            self.assertTrue(
                container_logs.find(expected_log_line) > -1,
                msg="Docker log line missing: %s from (%s)" % (expected_log_line, container_logs)
            )

    def test_openjdk(self):
        self.assertPackageIsInstalled("openjdk-8-jre")

    def test_default_app(self):
        driver = webdriver.PhantomJS()
        driver.get("http://%s:8080/" % Test1and1Java8Image.container_ip)
        self.assertEqual('Java Default App', driver.title)

    # </tests to run>

if __name__ == '__main__':
    unittest.main(verbosity=1)
