#!/usr/bin/env python
# coding: utf-8

# # Advanced topic: Analytical solution of the global Energy Balance Model
# 
# This notebook is part of [The Climate Laboratory](https://brian-rose.github.io/ClimateLaboratoryBook) by [Brian E. J. Rose](http://www.atmos.albany.edu/facstaff/brose/index.html), University at Albany.

# ____________
# ## 1. The zero-dimensional Energy Balance Model: recap
# ____________

# Previously we considered a zero-dimensional **Energy Balance Model** with the governing equation
# 
# $$ C \frac{dT_s}{dt} = (1-\alpha) Q - \tau \sigma T_s^4 $$
# 
# where
# - $T_s$ is the global average surface temperature
# - $C$ is the **heat capacity** of Earth system, in units of J m$^{-2}$ K$^{-1}$.
# - $\tau$ is the transmissivity of the atmosphere (a measure of the strength of the greenhouse effect).
# 
# We have seen that numerical solutions of this time-dependent model are easy to implement. However the model is solvable analytically once we make a (very good) approximation by linearing the OLR in terms of departures from equilibrium.
# 
# The analytical solutions will give us considerable insight into what's actually going on in the model.

# ____________
# ## 2. Linearizing about the equilibrium solution
# ____________

# ### Equilibrium solutions
# 
# We've already seen that the equilibrium solution of the model is
# 
# $$ T_{eq} = \left( \frac{(1-\alpha) Q}{\tau \sigma} \right)^\frac{1}{4} $$
# 
# and tuned the model parameter based on this relationship.

# We are going to **linearize the equation** for small perturbations away from this equilibrium.
# 
# Let $T_s = T_{eq} + T_s^\prime$ and restrict our solution to $T_s^\prime << T_{eq}$.
# 
# Note this this is not a big restriction! For example, a 10 degree warming or cooling is just $\pm$3.4% of the absolute equilibrium temperature.

# ### Linearizing the governing equation
# 
# Now use a first-order Taylor series expansion to write
# 
# $$ \text{OLR} = \tau \sigma T_s^4 $$
# 
# $$OLR = \tau \sigma T_s^4 = \tau \sigma \left( T_{eq} + T_s^\prime \right)^4  \approx \tau \sigma \left( T_{eq}^4 + 4 T_{eq}^3 T_s^\prime \right) $$

# and the budget for the perturbation temperature thus becomes
# 
# $$C \frac{d T_s^\prime}{d t} = -\lambda_0 T_s^\prime$$
# 
# where we define
# 
# $$\lambda_0 = 4 \tau \sigma T_{eq}^3 $$

# Putting in our observational values, we get 

# In[1]:


lambda_0 = 4 * sigma * tau * Teq_observed**3
#  This is an example of formatted text output in Python
print( 'lambda_0 = {:.2f} W m-2 K-1'.format(lambda_0)  )


# This is actually our first estimate of what is often called the **Planck feedback**. It is the tendency for a warm surface to cool by increased longwave radiation to space. 
# 
# It may also be refered to as the "no-feedback" climate response parameter. As we will see, $\lambda_0$ quantifies the sensitivity of the climate system in the absence of any actual feedback processes.

# ____________
# ## 3. Solving the linear ODE
# ____________

# Now define
# 
# $$ t^* = \frac{C}{\lambda_0}  $$
# 
# This is a positive constant with dimensions of time (seconds). With these definitions the temperature evolves according to
# 
# $$ \frac{d T_s^\prime}{d t} = - \frac{T_s^\prime}{t^*}$$
# 
# This is one of the simplest ODEs. Hopefully it looks familiar to most of you. It is the equation for an **exponential decay** process. 

# We can easily solve for the temperature evolution by integrating from an initial condition $T_s^\prime(0)$:
# 
# $$ \int_{T_s^\prime(0)}^{T_s^\prime(t)} \frac{d T_s^\prime}{T_s^\prime} = -\int_0^t  \frac{dt}{t^*}$$
# 
# $$\ln \bigg( \frac{T_s^\prime(t)}{T_s^\prime(0)} \bigg) = -\frac{t}{t^*}$$
# 
# $$T_s^\prime(t) = T_s^\prime(0) \exp \bigg(-\frac{t}{t^*} \bigg)$$
# 
# I hope that the mathematics is straightforward for everyone in this class. If not, go through it carefully and make sure you understand each step.

# ____________
# ## 4. e-folding time for relaxation of global mean temperature
# ____________

# Our model says that surface temperature will relax toward its equilibrium value over a characteristic time scale $t^*$. This is an **e-folding time** – the time it takes for the perturbation to decay by a factor $1/e = 0.37$
# 
# *What should this timescale be for the climate system?*
# 
# To estimate $t^*$ we need a value for the effective heat capacity $C$.
# 
# Our "quick and dirty" estimate above used 100 meters of water to set this heat capacity.

# #### What is the right choice for water depth $H$? 
# 
# That turns out to be an interesting and subtle question. It depends very much on the timescale of the problem
# 
# - days?
# - years?
# - decades?
# - millenia?

# We will revisit this question later in the course. For now, let’s just continue assuming $H = 100$ m (a bit deeper than the typical depth of the surface mixed layer in the oceans).
# 
# Now calculate the e-folding time for the surface temperature:

# In[2]:


tstar = C / lambda_0   #  Calculated value of relaxation time constant
seconds_per_year = 60.*60.*24.*365.
print( 'The e-folding time is {:1.2e} seconds or about {:1.0f} years.'.format(tstar, tstar / seconds_per_year))


# This is a rather fast timescale relative to other processes that can affect the planetary energy budget. 
# 
# **But notice that if the climate feedback parameter $\lambda$ is smaller, the timescale gets longer.**  We will come back to this later.

# ____________
# 
# ## 5. Summary
# ____________

# - We can solve the zero-dimensional EBM by linearizing the fourth-power dependence of OLR on temperature.
# - The result is a simple exponential decay model.
# - The system will tend to relax toward its equilibrium temperature on an $e$-folding timescale that depends on 
#     1. radiative feedback processes, and 
#     2. effective heat capacity.
# - In our estimate, this e-folding time is relatively short.
# - *In the absence of other processes that can either increase the heat capacity or lower (in absolute value) the feedback parameter, the Earth would never be very far out of energy balance.*
# - We will quantify this statement more as the term progresses.

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
