# SMU gym-booking automation

> **Historical and unmaintained.** This project is no longer intended for use. It is retained only as a portfolio example of web scraping and browser automation.

## Overview

This Python project was built to read SMU gym-slot listings from a Trumba calendar and automate form completion for selected times. It combines HTTP requests, HTML parsing, and Selenium browser control.

The booking site, form fields, browser-driver requirements, and university policies may have changed since the project was created. The repository has not been tested against the current service.

## Repository contents

| Path | Purpose |
| --- | --- |
| `gym_booker.py` | Reads preferred times, discovers booking links, and controls the browser. |
| `html_parsing_functions.py` | Extracts and inspects HTML form fields. |
| `timings.txt` | Historical example of preferred booking times. |
| `requirements.txt` | Original pinned Python environment. |

## Privacy and authorization

The source contains placeholders for a user's name, email address, student identifier, and phone number. Do not commit real personal details, credentials, cookies, or generated pages to a public repository.

Automated booking should only be attempted where the service owner explicitly permits it. Users are responsible for current university rules, website terms, access controls, request rates, and the effect of automated submissions. This repository does not attempt to bypass authentication or access restrictions.

## Compatibility

The original project used Microsoft Edge, Selenium 4.2, and Python packages pinned in `requirements.txt`. Platform-specific date formatting and current browser-driver behavior may differ. No support or compatibility guarantees are provided.

## License and reuse

No open-source license has been applied. The project is shared for viewing as a historical portfolio artifact.