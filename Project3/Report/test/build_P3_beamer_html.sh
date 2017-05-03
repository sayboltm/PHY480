#!/bin/bash

doconce format pandoc P3_beamer SLIDE_TYPE=remark SLIDE_THEME=light
doconce slides_markdown P3_beamer remark --slide_theme=light
