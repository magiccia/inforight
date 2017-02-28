# -*- coding: utf-8 -*-

"""
Tarbell project configuration
"""

# Google spreadsheet key
SPREADSHEET_KEY = "1dHV-cJ4G9Hm0vUca_41evnxhxi0ewB3q3SARzS4oLas"

# Exclude these files from publication
EXCLUDES = ["*.md", "requirements.txt"]

# Spreadsheet cache lifetime in seconds. (Default: 4)
# SPREADSHEET_CACHE_TTL = 4

# Create JSON data at ./data.json, disabled by default
# CREATE_JSON = True

# Get context from a local file or URL. This file can be a CSV or Excel
# spreadsheet file. Relative, absolute, and remote (http/https) paths can be 
# used.
# CONTEXT_SOURCE_FILE = ""

# EXPERIMENTAL: Path to a credentials file to authenticate with Google Drive.
# This is useful for for automated deployment. This option may be replaced by
# command line flag or environment variable. Take care not to commit or publish
# your credentials file.
# CREDENTIALS_PATH = ""

# S3 bucket configuration
S3_BUCKETS = {
    # Provide target -> s3 url pairs, such as:
    #     "mytarget": "mys3url.bucket.url/some/path"
    # then use tarbell publish mytarget to publish to it
    
    "production": "www.inforight.net/demo",
    "staging": "www.inforight.net/demo",
}

# Default template variables
DEFAULT_CONTEXT = {
    'name': 'inforight',
    'title': 'Inforight'
}


from clint.textui import puts
from flask import Blueprint, g
from tarbell.hooks import register_hook

import os

NAME = "Inforight"
blueprint = Blueprint("inforight", __name__)


@blueprint.route('/<slug>/')
def foia(slug):
    context = g.current_site.get_context()
    countries = {c['slug']: c for c in context['countries']}
    if slug not in countries.keys():
        return g.current_site.preview(slug)

    extra_context = {
        "country": countries[slug],
    }
    return g.current_site.preview('_foia.html', extra_context)


@register_hook('generate')
def foia_pages(site, output_root, quiet=False):
    if not quiet:
        puts("\nCreating country pages\n")

    data = site.get_context()
    countries = data["countries"]
    root_path = os.path.realpath(output_root)

    for country in countries:
        slug = country['slug']
        page_path = os.path.join(root_path, slug)
        if not os.path.exists(page_path):
            os.makedirs(page_path)
        index_path = os.path.join(page_path, 'index.html')
        if not quiet:
            puts("Writing {0}//{1}/index.html".format(output_root, slug))
        with site.app.test_client() as client:
            resp = client.get('/{0}/'.format(slug))
        f = open(index_path, 'w')
        f.write(resp.data)
        f.close()
