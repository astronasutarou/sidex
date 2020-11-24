#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests


def sidex_request(url,method,filename=None,token=None):
  method = 'get'
  basename = os.path.basename(url)

  if method not in ('get','put','delete'):
    raise RuntimeError('invalid method.')
  if method == 'put' and filename is None:
    raise RuntimeError('upload file is not specified.')
  data = { 'method': method, 'token': token }

  if method == 'get':
    if os.path.exists(filename):
      raise RuntimeError('file "{}" already exists'.format(filename))
    return requests.post(url, data=data)
  elif method == 'put':
    with open(args.filename,'rb') as f:
      files = { 'payload': f.read(), }
    return requests.post(url, data=data, files=files)
  elif method == 'delete':
    return requests.post(url, data=data)
