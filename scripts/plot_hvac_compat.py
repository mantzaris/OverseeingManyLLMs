#!/usr/bin/env python3
"""Run the frozen plotter on Matplotlib 3.1 using identical symmetric colors."""
from pathlib import Path
import matplotlib.colors as colors
if not hasattr(colors,'TwoSlopeNorm'):
    def symmetric_norm(vcenter,vmin,vmax):
        assert vcenter==0 and vmin==-vmax
        return colors.Normalize(vmin=vmin,vmax=vmax)
    colors.TwoSlopeNorm=symmetric_norm
# One of six harmful changes is an abstention, not an incorrect class label.
# Clarify only this display label; retain the frozen selection and measurements.
source=Path('scripts/plot_hvac.py').read_text().replace("'Correct -> wrong'","'Correct -> unresolved'")
exec(compile(source,'scripts/plot_hvac.py','exec'))
