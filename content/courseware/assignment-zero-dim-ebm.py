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
# # Assignment: Climate change in the zero-dimensional EBM
#
# This notebook is part of [The Climate Laboratory](https://brian-rose.github.io/ClimateLaboratoryBook) by [Brian E. J. Rose](http://www.atmos.albany.edu/facstaff/brose/index.html), University at Albany.

# %% [markdown]
# ## Learning goals
#
# Students completing this assignment will gain the following skills and concepts:
#
# - Familiarity with the Jupyter notebook
# - Familiarity with the zero-dimensional Energy Balance Model
# - Understanding of the adjustment toward equilibrium temperature
# - Introduction to the concept of albedo feedback
# - Use of numerical timestepping to find the equilibrium temperature
# - Python programming skills: arrays, loops, and simple graphs

# %% [markdown]
# ## Instructions
#
# - In a local copy of this notebook (on the JupyterHub or your own device) **add your answers in additional cells**.
# - **Complete the required problems** below. 
# - Some assignments have **optional bonus problems**. These are meant to be interesting and thought-provoking, but are not required. Extra credit will be given for interesting answers to the bonus problems.
# - Remember to set your cell types to `Markdown` for text, and `Code` for Python code!
# - **Include comments** in your code to explain your method as necessary.
# - Remember to actually answer the questions. **Written answers are required** (not just code and figures!)
# - Submit your solutions in **a single Jupyter notebook** that contains your text, your code, and your figures.
# - *Make sure that your notebook* ***runs cleanly without errors:***
#     - Save your notebook
#     - From the `Kernel` menu, select `Restart & Run All`
#     - Did the notebook run from start to finish without error and produce the expected output?
#     - If yes, save again and submit your notebook file
#     - If no, fix the errors and try again.

# %% [markdown]
# ## Problem 1: Time-dependent warming in the zero-dimensional Energy Balance Model

# %% [markdown]
# In lecture we defined a zero-dimensional energy balance model for the global mean surface temperature $T_s$ as follows
#
# $$ C  \frac{dT_s}{dt} = \text{ASR} - \text{OLR}$$
#
# $$ \text{ASR} = (1-\alpha) Q $$
#
# $$ \text{OLR} = \tau \sigma T_s^4$$
#
# where we defined these terms:
#
# - $C$ is a heat capacity for the atmosphere-ocean column
# - $\alpha$ is the global mean planetary albedo
# - $\sigma = 5.67 \times 10^{-8}$ W m$^{-2}$ K$^{-4}$ is the Stefan-Boltzmann constant
# - $\tau$ is our transmissivity parameter for the atmosphere.
# - $Q$ is the global-mean incoming solar radiation, or *insolation*.

# %% [markdown]
# Refer back to our class notes for parameter values.
#
# 1. If the heat penetrated to twice as deep into the ocean, the value of $C$ would be twice as large. Would this affect the **equilibrium temperature**? Why or why not?
# 2. In class we used numerical timestepping to investigate a *hypothetical climate change scenario* in which $\tau$ decreases to 0.57 and $\alpha$ increases to 0.32. We produced a graph of $T_s(t)$ over a twenty year period, starting from an initial temperature of 288 K. Here you will repeat this calculate with a larger value of $C$ and compare the warming rates. Specifically:
#     - Repeat our in-class time-stepping calculation with the same parameters we used before (including a heat capacity of $C = 4\times10^8$ J m$^{-2}$ K$^{-1}$), but extend it to 50 years. **You should create an array of temperatures with 51 elements, beginning from 288 K**.
#     - Now do it again, but use $C = 8\times10^8$ J m$^{-2}$ K$^{-1}$ (representing 200 meters of water). You should **create another 51-element array** of temperatures also beginning from 288 K.
#     - **Make a well-labeled graph** that compares the two temperatures over the 50-year period.
#     
# 4. What do your results show about the role of heat capacity on climate change? **Give a short written answer.**

# %%

# %% [markdown]
# ## Problem 2: Albedo feedback in the Energy Balance Model

# %% [markdown]
# For this exercise, we will introduce a new physical process into our model by **letting the planetary albedo depend on temperature**. The idea is that a warmer planet has less ice and snow at the surface, and thus a lower planetary albedo.
#
# Represent the ice-albedo feedback through the following formula:
#
# $$ \alpha(T) = \left\{ \begin{array}{ccc}
# \alpha_i &   & T \le T_i \\
# \alpha_o + (\alpha_i-\alpha_o) \frac{(T-T_o)^2}{(T_i-T_o)^2} &   & T_i < T < T_o \\
# \alpha_o &   & T \ge T_o \end{array} \right\}$$
#
# with the following parameter values:
#
# - $\alpha_o = 0.289$ is the albedo of a warm, ice-free planet
# - $\alpha_i = 0.7$ is the albedo of a very cold, completely ice-covered planet
# - $T_o = 293$ K is the threshold temperature above which our model assumes the planet is ice-free
# - $T_i = 260$ K is the threshold temperature below which our model assumes the planet is completely ice covered. 
#
# For intermediate temperature, this formula gives a smooth variation in albedo with global mean temperature. It is tuned to reproduce the observed albedo $\alpha = 0.299$ for $T = 288$ K. 

# %% [markdown]
# 1. 
#     - Define a Python function that implements the above albedo formula. *There is definitely more than one way to do it. It doesn't matter how you do it as long as it works!*
#     -  Use your function to calculate albedos for a wide range on planetary temperature (e.g. from $T=250$ K to $T=300$ K.)
#     - Present your results (albedo as a function of global mean temperature, or $\alpha(T)$) in a nicely labeled graph.
#     
# 2. Now investigate a climate change scenario with this new model:
#     - Suppose that the transmissivity decreases from 0.611 to 0.57 (same as before)
#     - Your task is to **calculate the new equilibrium temperature**. First, explain very briefly why you can't just solve for it analytically as we did when albedo was a fixed number.
#     - Instead, you will use numerical time-stepping to find the equilibrium temperature
#     - Repeat the procedure from Question 3 *(time-step forward for 50 years from an initial temperature of 288 K and make a graph of the results)*, but this time **use the function you defined above to compute the albedo for the current temperature**.
#     - Is the **new equilibrium temperature larger or smaller** than it was in the model with fixed albedo? **Explain why in your own words.**

# %%

# %% [markdown]
# ## Bonus problem
#
# *Open-ended investigation for extra credit, not required*
#
# Something very different occurs in this model if you introduce a strong negative radiative forcing, either by substantially reducing greenhouse gases (which we would represent as an increase in the transmissivity $\tau$), or by decreasing the incoming solar radiation $Q$.
#
# Investigate, using your numerical model code, and report your results along with your thoughts.

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
