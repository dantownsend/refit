#!/bin/bash

pytest -s --cov=refit --cov-report=html $@
