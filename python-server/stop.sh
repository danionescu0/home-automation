#!/bin/bash
ps ax |grep background.py |cut -d ' ' -f 2 |xargs kill -9
