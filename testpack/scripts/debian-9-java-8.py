#!/usr/bin/env python3

import unittest
import os
import docker
from selenium import webdriver
from testpack_helper_library.unittests.dockertests import Test1and1Common


class Test1and1Java8Image(Test1and1Common):
    container_ip = None

    @classmethod
    def setUpClass(cls):
        Test1and1Common.setUpClass()
        details = docker.APIClient().inspect_container(container=Test1and1Common.container.id)
        Test1and1Java8Image.container_ip = details['NetworkSettings']['IPAddress']

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
