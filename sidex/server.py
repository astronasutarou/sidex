#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, Response
from flask import request, url_for, render_template
import os, re, logging, requests
