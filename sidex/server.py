#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, Response
from flask import request, url_for, render_template
import os, re, logging, requests


log_handler = logging.StreamHandler()
log_handler.setFormatter(logging.Formatter(
  fmt='%(asctime)s %(levelname)s:%(name)s:%(message)s',
  datefmt='%Y-%m-%d %H:%M:%S'))

werkzeug = logging.getLogger('werkzeug')
werkzeug.setLevel('ERROR')
werkzeug.handlers = [log_handler,]

app = Flask(__name__)
app.logger.handlers = [log_handler,]


@app.context_processor
def override_url_for():
  def url_for_subdir(endpoint, *args, **options):
    subdir = '/{}'.format(app.subdir) if app.subdir else ''
    return subdir+url_for(endpoint, *args, **options)
  return dict(url_for=furl_for_subdir)
