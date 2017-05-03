#!/bin/bash

doconce format pandoc mcint SLIDE_TYPE=remark SLIDE_THEME=light
doconce slides_markdown mcint remark --slide_theme=light
