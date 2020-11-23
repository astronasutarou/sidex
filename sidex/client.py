#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, re, logging, requests



if __name__ == '__main__':
  from argparse import ArgumentParser as ap
  parser = ap(description='sidex minimal client')
  parser.add_argument('url', type=str,
    help='address to SIDEX server')
  parser.add_argument(
    '--get-token', dest='get_token', metavar='token', type=str,
    help='limit get function by setting token')
  parser.add_argument(
    '--put-token', dest='put_token', metavar='token', type=str,
    help='enable put function by setting token')
  parser.add_argument(
    '--delete-token', dest='delete_token', metavar='token', type=str,
    help='enable delete function by setting token.')

  args = parser.parse_args()

  payload =
