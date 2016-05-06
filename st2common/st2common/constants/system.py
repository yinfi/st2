# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from st2common import __version__

__all__ = [
    'VERSION_STRING',

    'API_URL_ENV_VARIABLE_NAME',
    'AUTH_TOKEN_ENV_VARIABLE_NAME',
    'SYSTEM_KV_PREFIX'
]

VERSION_STRING = 'StackStorm v%s' % (__version__)

API_URL_ENV_VARIABLE_NAME = 'ST2_API_URL'
AUTH_TOKEN_ENV_VARIABLE_NAME = 'ST2_AUTH_TOKEN'

# Used to prefix all system variables stored in the key-value store.
SYSTEM_KV_PREFIX = 'system'
SYSTEM_KV_SCOPE = SYSTEM_KV_PREFIX

# Used to prefix all user scoped variables in key-value store.
USER_KV_SCOPE = 'user'

ALLOWED_KV_SCOPES = [
    SYSTEM_KV_SCOPE,
    USER_KV_SCOPE
]
