# Copyright 2020 Google LLC
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

import bleach
import os
from flask import Flask
from flaskext.markdown import Markdown
from markdown.extensions.wikilinks import WikiLinkExtension
from . import util

def wikilink_to_url(label, base, end):
    label = util.canonical_wikilink(label)
    url = '/node/' + label
    return url

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Add blueprints here.
    from . import agora
    app.register_blueprint(agora.bp)
    app.add_url_rule('/', endpoint='index')

    # Jinja2 extensions.
    Markdown(app, tab_length=2, extensions=["sane_lists", WikiLinkExtension(build_url=wikilink_to_url)])
 
    @app.template_filter('linkify')
    def linkify(s):
         return bleach.linkify(s)

    return app
