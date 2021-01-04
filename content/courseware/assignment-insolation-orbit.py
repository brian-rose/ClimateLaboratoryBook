# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.8.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Assignment: Insolation and orbital parameters
#
# This notebook is part of [The Climate Laboratory](https://brian-rose.github.io/ClimateLaboratoryBook) by [Brian E. J. Rose](http://www.atmos.albany.edu/facstaff/brose/index.html), University at Albany.

# %% [markdown]
# ## Instructions
#
# Follow examples in the lecture notes on [Insolation](https://brian-rose.github.io/ClimateLaboratoryBook/courseware/insolation.html) and [Orbital variations](https://brian-rose.github.io/ClimateLaboratoryBook/courseware/orbital.html) to complete the following exercises. The bonus problem at the end is not required, but could be interesting and will earn extra credit.

# %% [markdown]
# ## Part 1
#
# Calculate the incoming solar radiation (insolation) at three different latitudes: 
# - the equator
# - 45ºN
# - the North Pole. 
#
# Use present-day orbital parameters.
#
# 1. **Make a well-labeled graph** that shows **all three insolation curves on the same plot**. The x
# axis of your graph should be days of the calendar year (beginning January 1), and the y axis should be insolation in W/m2. Include a legend showing which curve corresponds to which latitude.
# 2. Comment on the very different shapes of these three curves.

# %%

# %% [markdown]
# ## Part 2
#
# **Make the same graph using the orbital parameters of 10,000 years ago** (just after the end of the last ice age). Compare with your graph from Part 1 to answer these questions:
#
# 1. Was the insolation at northern high latitudes at summer solstice weaker or stronger 10,000 years ago compared to present conditions?
# 2. Was the summer season longer or shorter at high northern latitudes? To see this, look at the length of time between polar sunrise and polar sunset.
# 3. What other differences do you notice?

# %%

# %% [markdown]
# ## Part 3
#
# Calculate the **annual average insolation** for an array of latitudes ranging from the South Pole to the North Pole.
#
# Present your results as a well-labeled graph of annual average insolation as a function of latitude. You may use either present-day, or any other orbital parameters, but make sure you explain clearly what you using.

# %%

# %% [markdown]
# ## Part 4
#
# Recall that the **equilibrium temperature** in [our zero-dimensional EBM](https://brian-rose.github.io/ClimateLaboratoryBook/courseware/zero-dim-ebm.html#3.-Equilibrium-temperature) is
#
# $$T_{eq} = \left( \frac{(1-\alpha) ~ Q}{\tau~ \sigma} \right)^{\frac{1}{4}}$$
#
#
# **Suppose that this model applies independently at every latitude, where $Q$ is the annual average insolation at that latitude** (i.e. ignore exchanges of energy between adjacent latitude bands). 
#
# Using the annual mean $Q$ you computed in Part 3, make a graph of $T_{eq}$ as a function of latitude. Make sure to state clearly any assumptions you make about the parameter values $\alpha, \tau$.
#
#

# %%

# %% [markdown]
# ## Part 5 
#
# 1. What are typical **annual-average surface temperature** values at the South Pole, North Pole, and equator on Earth? Make sure to state your sources for these numbers. 
# 2. How do these compare to the equilibrium temperatures you computed in Part 4? 
# 3. Discuss some possible shortcomings of the simple model you used in Part 4.

# %%

# %% [markdown]
# ## Bonus question (for fun and extra credit)
#
# Repeat the exercises above for **a planet with zero eccentricity and 90º obliquity**.
#
# Speculate on what the seasonal cycle of temperature might look like at different locations on this planet.
#
# *90º obliquity means the planet’s rotation axis is parallel with the earth-sun plane, as if the planet were lying on its side. In our solar system, the planet Uranus has an obliquity close to 90º, as do many of the newly discovered extra-solar planets.*

# %%

# %% [markdown]
# ____________
#
# ## Credits
#
# This notebook is part of [The Climate Laboratory](https://brian-rose.github.io/ClimateLaboratoryBook), an open-source textbook developed and maintained by [Brian E. J. Rose](http://www.atmos.albany.edu/facstaff/brose/index.html), University at Albany.
#
# It is licensed for free and open consumption under the
# [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/) license.
#
# Development of these notes and the [climlab software](https://github.com/brian-rose/climlab) is partially supported by the National Science Foundation under award AGS-1455071 to Brian Rose. Any opinions, findings, conclusions or recommendations expressed here are mine and do not necessarily reflect the views of the National Science Foundation.
# ____________

# %%
