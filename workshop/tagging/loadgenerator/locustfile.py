#!/usr/bin/python
#
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import random
from locust import HttpUser, TaskSet, between

def index(l):
    l.client.get("/")

def credit_check(l):
    customernum=random.randint(10000000, 99999999)
    l.client.get("/check?customernum=" + str(customernum))

class UserBehavior(TaskSet):

    def on_start(self):
        index(self)

    tasks = {credit_check: 1}

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 50)
