# to-bus-stations

[![Refresh TTC Feed](https://github.com/thomassth/to-bus-stations/actions/workflows/ttc.yml/badge.svg)](https://github.com/thomassth/to-bus-stations/actions/workflows/ttc.yml) [![Parse TTC stops data](https://github.com/thomassth/to-bus-stations/actions/workflows/ttc_stops.yml/badge.svg)](https://github.com/thomassth/to-bus-stations/actions/workflows/ttc_stops.yml) [![Parse TTC subway closure data](https://github.com/thomassth/to-bus-stations/actions/workflows/ttc_subway_closure.yml/badge.svg)](https://github.com/thomassth/to-bus-stations/actions/workflows/ttc_subway_closure.yml) [![Parse TTC subway slow zone data](https://github.com/thomassth/to-bus-stations/actions/workflows/ttc_slow_zones.yml/badge.svg)](https://github.com/thomassth/to-bus-stations/actions/workflows/ttc_slow_zones.yml)

[![Refresh YRT Feed](https://github.com/thomassth/to-bus-stations/actions/workflows/yrt.yml/badge.svg)](https://github.com/thomassth/to-bus-stations/actions/workflows/yrt.yml) [![Parse YRT data](https://github.com/thomassth/to-bus-stations/actions/workflows/yrt_stops.yml/badge.svg)](https://github.com/thomassth/to-bus-stations/actions/workflows/yrt_stops.yml)

[![Deploy static content to Pages](https://github.com/thomassth/to-bus-stations/actions/workflows/static.yml/badge.svg)](https://github.com/thomassth/to-bus-stations/actions/workflows/static.yml)

Inspired by https://github.com/hkbus/hk-bus-crawling, this repo crawl, parse & hosts **useful, static** transit data.

Main consumer is https://tobus.ca/.

## Useful

Data that has an immediate use case / foreseeable use case in short term.

Example: Stop data is needed for geolocation, and are included.

Example 2: Subway station descriptions do not have foreseeable use case in short term, and are not included.

## Static

Data that doesn't change in rapid sucessions.

Example: Preplanned subway closures are not expected to change rapidly without notice, and are included.

Example 2: Service alerts change within minutes & can come and go without notice, and are not included.

## Credits
[@thomassth](https://github.com/thomassth) made most of it

[@YiweiShen](https://github.com/YiweiShen) helping with Python workflow
