#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, Response
from flask import request, url_for, render_template
import os, re, logging, requests

werkzeug = logging.getLogger('werkzeug')
werkzeug.setLevel('ERROR')

app = Flask(__name__)


@app.context_processor
def override_url_for():
  def url_for_subdir(endpoint, *args, **options):
    subdir = '/{}'.format(app.subdir) if app.subdir else ''
    return subdir+url_for(endpoint, *args, **options)
  return dict(url_for=furl_for_subdir)


def eprint(message, exc_info=None):
  remote = request.remote_addr
  app.logger.error(remote+':{}'.format(message), exc_info=exc_info)


def iprint(message):
  remote = request.remote_addr
  app.logger.info(remote+':{}'.format(message))


def dprint(message):
  remote = request.remote_addr
  app.logger.debug(remote+':{}'.format(message))


def invalid_path(path):
  return '../' in path


def default_delete_function(req, local_path, **options):
  filename = os.path.basename(local_path)
  os.unlink(local_path)
  return Response('"{}" successfully deleted.\n'.format(filename))


@app.route('/delete/<path:target>', methods=['POST',])
def delete(target):
  local_path = '{}/{}'.format(app.workdir,target)
  filename = os.path.basename(local_path)
  dirname = os.path.dirname(local_path)
  emsg = lambda s: 'cannot delete "{}": {{}}.\n'.format(target).format(s)
  ## check if a valid token is given.
  if app.delete_token is None:
    return Response(emsg('function disabled'), status=400)
  token = request.form.get('delete_token')
  dprint('delete_token = {}'.format(token))
  if app.delete_token is not None and token != app.delete_token:
    return Response(emsg('invalid token'), status=400)
  ## assert path seems valid.
  if invalid_path(target):
    eprint('invalid path: {}'.format(target))
    return Response(emsg('invalid path'), status=400)
  ## create a file.
  try:
    return app.delete_function(request,local_path)
  except FileNotFoundError as e:
    eprint(str(e))
    return Response(emsg('file not found'), status=404)
  except Exception as e:
    eprint(str(e))
    errmsg = emsg('unexpected error: {}'.format(e.__class__.__name__))
    return Response(errmsg, status=500)


def default_put_function(req, local_path, **options):
  filename = os.path.basename(local_path)
  req.files['payload'].save(local_path)
  return Response('"{}" successfully uploaded.\n'.format(filename))


@app.route('/put/<path:target>', methods=['POST',])
def put(target):
  local_path = '{}/{}'.format(app.workdir,target)
  filename = os.path.basename(local_path)
  dirname = os.path.dirname(local_path)
  emsg = lambda s: 'cannot create "{}": {{}}.\n'.format(target).format(s)
  ## check if a valid token is given.
  if app.put_token is None:
    return Response(emsg('function disabled'), status=400)
  token = request.form.get('put_token')
  dprint('put_token = {}'.format(token))
  if app.put_token is not None and token != app.put_token:
    return Response(emsg('invalid token'), status=400)
  ## assert path seems valid.
  if invalid_path(target):
    eprint('invalid path: {}'.format(target))
    return Response(emsg('invalid path'), status=400)
  ## override is not allowed.
  if os.path.exists(local_path):
    eprint('file "{}" already exists.'.format(local_path))
    return Response(emsg('overwrite prohibited'), status=400)
  ## create a file.
  if 'payload' not in request.files:
    return Response(emsg('"payload" is required'), status=400)
  try:
    return app.put_function(request,local_path)
  except FileNotFoundError as e:
    eprint(str(e))
    return Response(emsg('file not found'), status=404)
  except Exception as e:
    eprint(str(e))
    errmsg = emsg('unexpected error: {}'.format(e.__class__.__name__))
    return Response(errmsg, status=500)


def default_get_function(req, local_path, **options):
  with open(local_path, 'rb') as f:
    return Response(f.read(), mimetype='application/octet-stream')


@app.route('/get/<path:target>', methods=['GET','POST'])
def get(target):
  local_path = '{}/{}'.format(app.workdir,target)
  filename = os.path.basename(local_path)
  emsg = lambda s: 'cannot access "{}": {{}}.\n'.format(target).format(s)
  ## check if a valid token is given.
  if app.get_token is not None:
    dprint('token is requred.')
    if request.method == 'GET':
      return Response(emsg('token required'), status=400)
    token = request.form.get('get_token')
    dprint('get_token = "{}"'.format(token))
    if token != app.get_token:
      return Response(emsg('invalid token'), status=400)
  ## assert path seems valid.
  if invalid_path(target):
    eprint('invalid path: {}'.format(target))
    return Response(emsg('invalid path'), status=500)
  ## access to file.
  #if os.path.exists(local_path):
  try:
    return app.get_function(request, local_path)
  except FileNotFoundError as e:
    eprint(str(e))
    return Response(emsg('file not found'), status=404)
  except IsADirectoryError as e:
    eprint(str(e))
    return Response(emsg('directory requested'), status=400)
  except Exception as e:
    eprint(str(e))
    errmsg = emsg('unexpected error: {}'.format(e.__class__.__name__))
    return Response(errmsg, status=500)


@app.route('/')
def index():
  return Response('under construction.\n', status=501)


def setup_sidex(
    workdir, subdir=None,
    get_function=default_get_function,
    put_function=default_put_function,
    delete_function=default_delete_function,
    get_token=None, put_token=None, delete_token=None,
    log_handler=None, log_level='INFO'):
  if get_token is not None: assert len(get_token) > 0
  if put_token is not None: assert len(put_token) > 0
  if delete_token is not None: assert len(delete_token) > 0
  app.workdir = workdir
  app.get_function = get_function
  app.put_function = put_function
  app.delete_function = delete_function
  app.get_token = get_token
  app.put_token = put_token
  app.delete_token = delete_token
  app.subdir = subdir
  app.logger.setLevel(log_level)
  if log_handler is not None:
    werkzeug.handlers = []
    app.logger.handlers = [log_handler,]
  return app


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

  log_level = 'DEBUG' if args.debug else 'INFO'
  log_handler = logging.StreamHandler()
  log_handler.setFormatter(logging.Formatter(
    fmt='[%(asctime)s] %(levelname)s:%(name)s:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'))

  server = setup_sidex(
    args.target, subdir=args.subdir,
    get_token=args.get_token, put_token=args.put_token,
    delete_token=args.delete_token,
    log_handler=log_handler, log_level=log_level)
  server.run(host=args.host, port=args.port, threaded=True, debug=args.debug)
