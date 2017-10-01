#!/usr/bin/env python
import RPi.GPIO as GPIO

# Hardware SPI

# CS setup

# code to read one MCP chip


def readBoard():
    inner = read_mcp(CS[0])
    middle = read_mcp(CS[1])
    outer = read_mcp(CS[2])
