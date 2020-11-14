#!/usr/bin/env python
# coding: utf-8

# # Insolation
# 
# This notebook is part of [The Climate Laboratory](https://brian-rose.github.io/ClimateLaboratoryBook) by [Brian E. J. Rose](http://www.atmos.albany.edu/facstaff/brose/index.html), University at Albany.

# ____________
# <a id='section1'></a>
# 
# ## 1. Distribution of insolation
# ____________
# 

# *These notes closely follow section 2.7 of Dennis L. Hartmann, "Global Physical Climatology", Academic Press 1994.*
# 

# The **amount of solar radiation** incident on the top of the atmosphere (what we call the "insolation") depends on
# 
# - latitude
# - season
# - time of day
# 
# This insolation is the primary driver of the climate system. Here we will examine the geometric factors that determine insolation, focussing primarily on the **daily average** values.

# ### Solar zenith angle
# 
# We define the **solar zenith angle** $\theta_s$ as the angle between the local normal to Earth's surface and a line between a point on Earth's surface and the sun.

# <img src='../images/Hartmann_Fig2.5.png'>

# From the above figure (reproduced from Hartmann's book), the ratio of the shadow area to the surface area is equal to the cosine of the solar zenith angle.

# ### Instantaneous solar flux
# 
# We can write the solar flux per unit surface area as
# 
# $$ Q = S_0 \left( \frac{\overline{d}}{d} \right)^2 \cos \theta_s $$
# 
# where $\overline{d}$ is the mean distance for which the flux density $S_0$ (i.e. the solar constant) is measured, and $d$ is the actual distance from the sun.
# 
# Question:
# 
# - what factors determine $\left( \frac{\overline{d}}{d} \right)^2$ ?
# - under what circumstances would this ratio always equal 1?

# ### Calculating the zenith angle
# 
# Just like the flux itself, the solar zenith angle depends latitude, season, and time of day.

# #### Declination angle
# The seasonal dependence can be expressed in terms of the **declination angle** of the sun: the latitude of the point on the surface of Earth directly under the sun at noon (denoted by $\delta$).
# 
# $\delta$ currenly varies between +23.45º at northern summer solstice (June 21) to -23.45º at northern winter solstice (Dec. 21).

# #### Hour angle
# 
# The **hour angle** $h$ is defined as the longitude of the subsolar point relative to its position at noon.

# #### Formula for zenith angle
# With these definitions and some spherical geometry (see Appendix A of Hartmann's book), we can express the solar zenith angle for any latitude $\phi$, season, and time of day as
# 
# $$ \cos \theta_s = \sin \phi \sin \delta + \cos\phi \cos\delta \cos h $$

# #### Sunrise and sunset
# 
# If $\cos\theta_s < 0$ then the sun is below the horizon and the insolation is zero (i.e. it's night time!)
# 
# Sunrise and sunset occur when the solar zenith angle is 90º and thus $\cos\theta_s=0$. The above formula then gives
# 
# $$ \cos h_0 = - \tan\phi \tan\delta $$
# 
# where $h_0$ is the hour angle at sunrise and sunset.

# #### Polar night
# 
# Near the poles special conditions prevail. Latitudes poleward of 90º-$\delta$ are constantly illuminated in summer, when $\phi$ and $\delta$ are of the same sign.  Right at the pole there is 6 months of perpetual daylight in which the sun moves around the compass at a constant angle $\delta$ above the horizon.
# 
# In the winter, $\phi$ and $\delta$ are of opposite sign, and latitudes poleward of 90º-$|\delta|$ are in perpetual darkness. At the poles, six months of daylight alternate with six months of daylight.
# 
# At the equator day and night are both 12 hours long throughout the year.

# ### Daily average insolation
# 
# Substituting the expression for solar zenith angle into the insolation formula gives the instantaneous insolation as a function of latitude, season, and time of day:
# 
# $$ Q = S_0 \left( \frac{\overline{d}}{d} \right)^2 \Big( \sin \phi \sin \delta + \cos\phi \cos\delta \cos h  \Big) $$
# 
# which is valid only during daylight hours, $|h| < h_0$, and $Q=0$ otherwise (night).

# To get the daily average insolation, we integrate this expression between sunrise and sunset and divide by 24 hours (or $2\pi$ radians since we express the time of day in terms of hour angle):
# 
# $$ \overline{Q}^{day} = \frac{1}{2\pi} \int_{-h_0}^{h_0} Q ~dh$$
# 
# $$ = \frac{S_0}{2\pi} \left( \frac{\overline{d}}{d} \right)^2 \int_{-h_0}^{h_0} \Big( \sin \phi \sin \delta + \cos\phi \cos\delta \cos h  \Big) ~ dh $$

# which is easily integrated to get our formula for daily average insolation:
# 
# $$ \overline{Q}^{day} = \frac{S_0}{\pi} \left( \frac{\overline{d}}{d} \right)^2 \Big( h_0 \sin\phi \sin\delta + \cos\phi \cos\delta \sin h_0 \Big)$$
# 
# where the hour angle at sunrise/sunset $h_0$ must be in radians.

# ### The daily average zenith angle
# 
# It turns out that, due to optical properties of the Earth's surface (particularly bodies of water), the surface albedo depends on the solar zenith angle. It is therefore useful to consider the average solar zenith angle during daylight hours as a function of latidude and season.
# 
# The appropriate daily average here is weighted with respect to the insolation, rather than weighted by time. The formula is
# 
# $$ \overline{\cos\theta_s}^{day} = \frac{\int_{-h_0}^{h_0} Q \cos\theta_s~dh}{\int_{-h_0}^{h_0} Q ~dh} $$

# <img src='../images/Hartmann_Fig2.8.png'>

# The average zenith angle is much higher at the poles than in the tropics. This contributes to the very high surface albedos observed at high latitudes.

# ____________
# <a id='section2'></a>
# 
# ## 2. Computing daily insolation with `climlab`
# ____________

# Here are some examples calculating daily average insolation at different locations and times.
# 
# These all use a function called 
# ```
# daily_insolation
# ``` 
# in the package 
# ```
# climlab.solar.insolation
# ``` 
# to do the calculation. The code implements the above formulas to calculates daily average insolation anywhere on Earth at any time of year.

# The code takes account of *orbital parameters* to calculate current Sun-Earth distance.  
# 
# We can look up *past orbital variations* to compute their effects on insolation using the package 
# ```
# climlab.solar.orbital
# ```
# See the [next lecture](./Lecture14 -- Orbital variations.ipynb)!

# ### Using the `daily_insolation` function

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
import matplotlib.pyplot as plt
from climlab import constants as const
from climlab.solar.insolation import daily_insolation


# First, get a little help on using the `daily_insolation` function:

# In[2]:


help(daily_insolation)


# Here are a few simple examples.
# 
# First, compute the daily average insolation at 45ºN on January 1:

# In[3]:


daily_insolation(45,1)


# Same location, July 1:

# In[4]:


daily_insolation(45,181)


# We could give an array of values. Let's calculate and plot insolation at all latitudes on the spring equinox = March 21 = Day 80

# In[5]:


lat = np.linspace(-90., 90., 30)
Q = daily_insolation(lat, 80)
fig, ax = plt.subplots()
ax.plot(lat,Q)
ax.set_xlim(-90,90); ax.set_xticks([-90,-60,-30,-0,30,60,90])
ax.set_xlabel('Latitude')
ax.set_ylabel('W/m2')
ax.grid()
ax.set_title('Daily average insolation on March 21')


# ### In-class exercises
# 
# Try to answer the following questions **before reading the rest of these notes**.
# 
# - What is the daily insolation today here at Albany (latitude 42.65ºN)?
# - What is the **annual mean** insolation at the latitude of Albany?
# - At what latitude and at what time of year does the **maximum daily insolation** occur?
# - What latitude is experiencing either **polar sunrise** or **polar sunset** today?

# ____________
# <a id='section3'></a>
# 
# ## 3. Global, seasonal distribution of insolation (present-day orbital parameters)
# ____________

# Calculate an array of insolation over the year and all latitudes (for present-day orbital parameters). We'll use a dense grid in order to make a nice contour plot

# In[6]:


lat = np.linspace( -90., 90., 500)
days = np.linspace(0, const.days_per_year, 365 )
Q = daily_insolation( lat, days )


# And make a contour plot of Q as function of latitude and time of year.

# In[7]:


fig, ax = plt.subplots(figsize=(10,8))
CS = ax.contour( days, lat, Q , levels = np.arange(0., 600., 50.) )
ax.clabel(CS, CS.levels, inline=True, fmt='%r', fontsize=10)
ax.set_xlabel('Days since January 1', fontsize=16 )
ax.set_ylabel('Latitude', fontsize=16 )
ax.set_title('Daily average insolation', fontsize=24 )
ax.contourf ( days, lat, Q, levels=[-1000., 0.], colors='k' )


# ### Time and space averages

# Take the area-weighted global, annual average of Q...

# In[8]:


Qaverage = np.average(np.mean(Q, axis=1), weights=np.cos(np.deg2rad(lat)))
print( 'The annual, global average insolation is %.2f W/m2.' %Qaverage)


# Also plot the zonally averaged insolation at a few different times of the year:

# In[9]:


summer_solstice = 170
winter_solstice = 353
fig, ax = plt.subplots(figsize=(10,8))
ax.plot( lat, Q[:,(summer_solstice, winter_solstice)] );
ax.plot( lat, np.mean(Q, axis=1), linewidth=2 )
ax.set_xbound(-90, 90)
ax.set_xticks( range(-90,100,30) )
ax.set_xlabel('Latitude', fontsize=16 );
ax.set_ylabel('Insolation (W m$^{-2}$)', fontsize=16 );
ax.grid()


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

# In[ ]:




