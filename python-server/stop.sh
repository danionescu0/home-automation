#!/bin/bash
ps ax |grep background.py |cut -d ' ' -f 1 |xargs kill -9
