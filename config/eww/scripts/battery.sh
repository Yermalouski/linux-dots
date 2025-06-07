#!/bin/bash

while true: do
    BATTERY=$(cat /sys/class/power_supply/BAT0/capacity)
    STATUS=$(cat /sys/class/power_supply/BAT0/status)
    echo "$BATTERY%"
    sleep 10
done
