#!/usr/bin/env python3

# Copyright 2013 Gary Martin
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup

setup(name='BurritoBot',
      description='A bot with an undisclosed association with burritos',
      version='0.1.0',
      author='Gary Martin',
      author_email='gary.martin@physics.org',
      packages=['burrito', 'burrito.plugins', ],
      license='LICENSE.txt',
      entry_points="""
              [console_scripts]
              burritobot = burrito.burritocli:run
              """,
      )
