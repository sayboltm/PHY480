#!/bin/bash

doconce format pandoc P3_prez SLIDE_TYPE=remark SLIDE_THEME=light
doconce slides_markdown P3_prez remark --slide_theme=light


#doconce format pandoc P3_prez_scratchwork SLIDE_TYPE=remark SLIDE_THEME=light
#doconce slides_markdown P3_prez_scratchwork remark --slide_theme=light
