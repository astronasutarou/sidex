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


def eprint(message, exc_info=None):
  app.logger.error('{}'.format(message), exc_info=exc_info)


def invalid_path(path):
  return '../' in path


@app.route('/get/<path:target>', methods=['GET','POST'])
def get(target):
  local_path = '{}/{}'.format(app.root,target)
  filename = os.path.basename(local_path)
  emsg = lambda s: 'cannot access "{}": {{}}.\n'.format(target).format(s)
  ## check if a valid token is given.
  if request.method == 'POST':
    token = request.form.get('get_token')
    if app.get_token is not None and token != app.get_token:
      return Response(emsg('invalid token'), status=400)
  elif request.method == 'GET':
    if app.get_token is not None:
      return Response(emsg('token required'), status=400)
  ## assert path seems valid.
  if invalid_path(target):
    return Response(emsg('invalid path'), status=500)
  ## access to file.
  if os.path.exists(local_path):
    if os.path.isdir(local_path):
      return Response(emsg('not a file'), status=500)
    try:
      with open(local_path, 'rb') as f:
        return Response(f.read(), mimetype='application/octet-stream')
    except Exception as e:
      eprint(str(e), exc_info=e)
      return Response(emsg(str(e)), status=500)
  else:
    return Response(emsg('no such file'), status=404)


@app.route('/')
def index():
  return Response('under construction.\n', status=501)


if __name__ == '__main__':
  from argparse import ArgumentParser as ap
  parser = ap(description='sidex server process')
  parser.add_argument('target', type=str,
    help='target directory')
  parser.add_argument(
    '--host', dest='host', metavar='host', type=str, default='0.0.0.0',
    help='set server hostname')
  parser.add_argument(
    '--port', dest='port', metavar='port', type=int, default=8080,
    help='set server port number')
  parser.add_argument(
    '--get-token', dest='get_token', metavar='token', type=str,
    help='limit get function by setting token')
  parser.add_argument(
    '--put-token', dest='put_token', metavar='token', type=str,
    help='enable put function by setting token')
  parser.add_argument(
    '--delete-token', dest='delete_token', metavar='token', type=str,
    help='enable delete function by setting token.')
  parser.add_argument(
    '--subdir', dest='subdir', metavar='subdirectory', type=str,
    help='set subdirectory')
  parser.add_argument(
    '--debug', dest='debug', action='store_true',
    help='enable debug messages')

  args = parser.parse_args()

  if args.get_token is not None: assert len(args.get_token) > 0
  if args.put_token is not None: assert len(args.put_token) > 0
  if args.delete_token is not None: assert len(args.delete_token) > 0

  app.subdir = args.subdir
  app.root = args.target
  app.get_token = args.get_token
  app.put_token = args.put_token
  app.delete_token = args.delete_token
  logleve = 'DEBUG' if args.debug else 'INFO'
  app.run(host=args.host, port=args.port, threaded=True, debug=args.debug)
