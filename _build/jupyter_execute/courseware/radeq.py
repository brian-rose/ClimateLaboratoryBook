#!/usr/bin/env python
# coding: utf-8

# # Radiative Equilibrium
# 
# This notebook is part of [The Climate Laboratory](https://brian-rose.github.io/ClimateLaboratoryBook) by [Brian E. J. Rose](http://www.atmos.albany.edu/facstaff/brose/index.html), University at Albany.

# ____________
# <a id='section1'></a>
# 
# ## 1. The observed annual, global mean temperature profile
# ____________
# 
# Let's look again the observations of air temperature from the NCEP Reanalysis data we first encountered in the [Radiation notes](https://brian-rose.github.io/ClimateLaboratoryBook/courseware/radiation.html).
# 
# In this notebook  we'll define a function to create the Skew-T diagram, because later we are going to reuse it several times.
# 
# *Click to expand code cells to see Python details* 

# In[1]:


#  This code is used just to create the skew-T plot of global, annual mean air temperature
get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from metpy.plots import SkewT
ncep_url = "http://www.esrl.noaa.gov/psd/thredds/dodsC/Datasets/ncep.reanalysis.derived/"
ncep_air = xr.open_dataset( ncep_url + "pressure/air.mon.1981-2010.ltm.nc", use_cftime=True)
#  Take global, annual average 
coslat = np.cos(np.deg2rad(ncep_air.lat))
weight = coslat / coslat.mean(dim='lat')
Tglobal = (ncep_air.air * weight).mean(dim=('lat','lon','time'))


# In[2]:


def make_skewT():
    fig = plt.figure(figsize=(9, 9))
    skew = SkewT(fig, rotation=30)
    skew.plot(Tglobal.level, Tglobal, color='black', linestyle='-', linewidth=2, label='Observations')
    skew.ax.set_ylim(1050, 10)
    skew.ax.set_xlim(-90, 45)
    # Add the relevant special lines
    skew.plot_dry_adiabats(linewidth=0.5)
    skew.plot_moist_adiabats(linewidth=0.5)
    #skew.plot_mixing_lines()
    skew.ax.legend()
    skew.ax.set_xlabel('Temperature (degC)', fontsize=14)
    skew.ax.set_ylabel('Pressure (hPa)', fontsize=14)
    return skew


# In[3]:


skew = make_skewT()


# Here we are going to work with some detailed **Single-Column Models** to understand questions such as
# 
# - What physical factors actually determine this profile? 
# - Would the profile be different with different gases in the atmosphere?
# - What are the relative roles of **radiation** and **dynamics** (i.e. motion!) in setting this profile?
# 
# We will start by **ignoring all processes except radiation**. We will calculate something called the **radiative equilibrium** temperature.

# ____________
# 
# ## 2. Radiative equilibrium -- the concept
# ____________

# Models of radiative transfer slice up the atmospheric air column into a series of layer, and calculate the **emission** and **absorption** of radiation within each layer.
# 
# It's really just a generalization of the model we already looked at:

# ![Sketch of layer model](http://www.atmos.albany.edu/facstaff/brose/classes/ENV415_Spring2018/images/2layerAtm_sketch.png)

# The concept of **radiative equilibrium** means that we **ignore all methods of heat exchange except for radiation**, and ask what temperature profile would exist under that assumption?
# 
# We can answer that question by using a radiative transfer model to explicity compute the shortwave and longwave beams, and the warming/cooling of each layer associated with the radiative sources and sinks of energy.
# 
# Basically, we reach radiative equilibrium when **energy is received and lost through radiation at the same rate in every layer**.

# Because of the complicated dependence of emission/absorption features on the wavelength of radiation and the different gases, the beam is divided up into many different pieces representing different parts of the electromagnetic spectrum.
# 
# We will not look explicitly at this complexity here, but we will **use a model** that represents these processes at the same level of detail we would in a GCM.

# ____________
# 
# ## 3. Setting up a single-column radiation model in climlab
# ____________

# ### Radiation models in climlab
# 
# We're now going to use **climlab** to run a **complex radiation model**, one that accounts for the spectral absorption properties of different gases.
# 
# climlab actually provides two different "GCM-level" [radiation codes](https://climlab.readthedocs.io/en/latest/api/climlab.radiation.Radiation.html):
# 
# - The [CAM3 radiation module](https://climlab.readthedocs.io/en/latest/api/climlab.radiation.CAM3.html) from NCAR (essentially the same radiation code used in our CESM simulations)
# - The [RRTMG (Rapid Radiative Transfer Model)](https://climlab.readthedocs.io/en/latest/api/climlab.radiation.RRTMG.html) which is used in many current GCMs.
# 
# The links above take you to the online [climlab documentation](http://climlab.readthedocs.io/en/latest/intro.html).

# We're going to use a model called the [Rapid Radiative Transfer Model](http://rtweb.aer.com/rrtm_frame.html) or RRTMG. This is a "serious" and widely-used radiation model, used in many comprehensive GCMs and Numerical Weather Prediction models.
# 
# climlab provides an easy-to-use Python wrapper for the RRTMG code.

# ### Water vapor data

# Before setting up the model, we need some water vapor data. Why? Because our model needs to know how much water vapor exists at each vertical level, since water vapor is a radiatively important gas.
# 
# We're actually going to use the specific humidity field from our CESM control simulation. We'll just take the global, time average of this data, and plot its vertical profile.

# In[4]:


#  Load the model output as we have done before
cesm_data_path = "http://thredds.atmos.albany.edu:8080/thredds/dodsC/CESMA/"
atm_control = xr.open_dataset(cesm_data_path + "cpl_1850_f19/concatenated/cpl_1850_f19.cam.h0.nc")
#  The specific humidity is stored in the variable called Q in this dataset:
print(atm_control.Q)


# Now take the global, annual average of the specific humidity:

# In[5]:


# Take global, annual average of the specific humidity
weight_factor = atm_control.gw / atm_control.gw.mean(dim='lat')
Qglobal = (atm_control.Q * weight_factor).mean(dim=('lat','lon','time'))
# Take a look at what we just calculated ... it should be one-dimensional (vertical levels)
print(Qglobal)


# And make a figure:

# In[6]:


fig, ax = plt.subplots()
#  Multiply Qglobal by 1000 to put in units of grams water vapor per kg of air
ax.plot(Qglobal*1000., Qglobal.lev)
ax.invert_yaxis()
ax.set_ylabel('Pressure (hPa)')
ax.set_xlabel('Specific humidity (g/kg)')
ax.grid()


# This shows a typical climatological humidity profile. Water vapor is a **trace gas**! But as we will see, it plays a very important role.
# 
# Based on this figure, where is most of the water vapor?

# ### Create a single-column model on the same grid as this water vapor data:

# Here we will create the grid and state variables (air and surface temperature) for our single-column model.

# In[7]:


import climlab
#  Make a model on same vertical domain as the GCM
mystate = climlab.column_state(lev=Qglobal.lev, water_depth=2.5)
print(mystate)


# In[8]:


radmodel = climlab.radiation.RRTMG(name='Radiation (all gases)',  # give our model a name!
                              state=mystate,   # give our model an initial condition!
                              specific_humidity=Qglobal.values,  # tell the model how much water vapor there is
                              albedo = 0.25,  # this the SURFACE shortwave albedo
                              timestep = climlab.constants.seconds_per_day,  # set the timestep to one day (measured in seconds)
                             )
print(radmodel)


# ### Explore the single-column model object

# Look at a few interesting properties of the model we just created:

# In[9]:


#  Here's the state dictionary we already created:
radmodel.state


# In[10]:


#  Here are the pressure levels in hPa
radmodel.lev


# There is a dictionary called `absorber_vmr` that holds the *volume mixing ratio* of all the radiatively active gases in the column:

# In[11]:


radmodel.absorber_vmr


# Most are just a single number because they are assumed to be **well mixed** in the atmosphere.
# 
# The exception is ozone, which has a vertical structure taken from observations. Let's plot it

# In[12]:


#  E.g. the CO2 content (a well-mixed gas) in parts per million
radmodel.absorber_vmr['CO2'] * 1E6


# ### Python exercise: plot the ozone profile
# 
# Make a simple plot showing the vertical structure of ozone, similar to the specific humidity plot we just made above.

# In[13]:


# here is the data you need for the plot, as a plain numpy arrays:
print(radmodel.lev)
print(radmodel.absorber_vmr['O3'])


# In[ ]:





# The other radiatively important gas is of course water vapor, which is stored separately in the `specific_humidity` attribute:

# In[14]:


#  specific humidity in kg/kg, on the same pressure axis
print(radmodel.specific_humidity)


# ### The RRTMG radiation model has lots of different input parameters
# 
# For details you can look at the [documentation](http://climlab.readthedocs.io/en/latest/api/climlab.radiation.radiation.html)

# In[15]:


for item in radmodel.input:
    print(item)


# Many of the parameters control the **radiative effects of clouds**.
# 
# But here we should note that the model is **initialized with no clouds at all**:

# In[16]:


#  This is the fractional area covered by clouds in our column:
radmodel.cldfrac


# ____________
# 
# ## 4. Radiative equilibrium in the single-column model
# ____________

# ### Step the model forward in time!

# Here are the current temperatures (initial condition):

# In[17]:


radmodel.Ts


# In[18]:


radmodel.Tatm


# Now let's take a single timestep:

# In[19]:


radmodel.step_forward()


# In[20]:


radmodel.Ts


# The surface got warmer! 
# 
# Let's take a look at all the diagnostic information that was generated during that timestep:

# ### Diagnostic variables in our single-column model
# 
# Every climlab model has a `diagnostics` dictionary. Here we are going to check it out as an `xarray` dataset:

# In[21]:


climlab.to_xarray(radmodel.diagnostics)


# The main "job" of a radiative transfer model it to calculate the shortwave and longwave fluxes up and down between each model layer.
# 
# For example:

# In[22]:


climlab.to_xarray(radmodel.LW_flux_up)


# These are upward longwave fluxes in W/m2.
# 
# Why are there 27 data points, when the model has 26 pressure levels?

# In[23]:


radmodel.lev


# In[24]:


radmodel.lev_bounds


# The last element of the flux array represents the **upward flux from the surface to the first level**:

# In[25]:


radmodel.LW_flux_up[-1]


# The value is about 390 W m$^{-2}$. 
# 
# Why?

# In[26]:


sigma = 5.67E-8
sigma * 288**4


# The surface temperature was initialized at 288 K, and the surface is treated as very close to a blackbody in the model.

# What about the flux from the top layer out to space?
# 
# Two ways to access this information:

# In[27]:


radmodel.LW_flux_up[0]


# In[28]:


radmodel.OLR


# Of course there is a whole other set of fluxes for the shortwave radiation.
# 
# One diagnostic we will often want to look at is the **net energy budget at the top of the atmosphere**:

# In[29]:


radmodel.ASR - radmodel.OLR


# ***Is the model gaining or losing energy?***

# ### Integrate out to equilibrium
# 
# Here I want to step forward in time until the model is very close to energy balance.
# 
# We can use a `while` loop, conditional on the top-of-atmosphere imbalance:

# In[30]:


while np.abs(radmodel.ASR - radmodel.OLR) > 0.01:
    radmodel.step_forward()


# Check the energy budget again:

# In[31]:


#  Check the energy budget again
radmodel.ASR - radmodel.OLR


# Indeed, the imbalance is now small.

# ### Compare the radiative equilibrium temperature to observations

# Here's a helper function we'll use to add model temperature profiles to our skew-T plot:

# In[32]:


def add_profile(skew, model, linestyle='-', color=None):
    line = skew.plot(model.lev, model.Tatm - climlab.constants.tempCtoK,
             label=model.name, linewidth=2)[0]
    skew.plot(1000, model.Ts - climlab.constants.tempCtoK, 'o', 
              markersize=8, color=line.get_color())
    skew.ax.legend()


# In[33]:


skew = make_skewT()
add_profile(skew, radmodel)
skew.ax.set_title('Pure radiative equilibrium', fontsize=18);


# What do you think about this model -- data comparison?

# ____________
# 
# ## 5. Effects of different gases on the radiative equilibrium profile
# ____________

# **Models are for experimenting and playing with!**
# 
# We have just built a single-column radiation model with several different absorbing gases. *We can learn about their effects by taking them away.*

# ### Radiative equilibrium without water vapor

# In[34]:


# Make an exact clone of our existing model
radmodel_noH2O = climlab.process_like(radmodel)
radmodel_noH2O.name = 'Radiation (no H2O)'
print(radmodel_noH2O)


# In[35]:


#  Here is the water vapor profile we started with
radmodel_noH2O.specific_humidity


# Now get rid of the water entirely!

# In[36]:


radmodel_noH2O.specific_humidity *= 0.


# In[37]:


radmodel_noH2O.specific_humidity


# And run this new model forward to equilibrium:

# In[38]:


#  it's useful to take a single step first before starting the while loop
#   because the diagnostics won't get updated 
#  (and thus show the effects of removing water vapor)
#  until we take a step forward
radmodel_noH2O.step_forward()
while np.abs(radmodel_noH2O.ASR - radmodel_noH2O.OLR) > 0.01:
    radmodel_noH2O.step_forward()


# In[39]:


radmodel_noH2O.ASR - radmodel_noH2O.OLR


# In[40]:


skew = make_skewT()
for model in [radmodel, radmodel_noH2O]:
    add_profile(skew, model)


# What do you think you can learn from this about the radiative role of water vapor?

# ### Exercise: radiative equilibrium without ozone
# 
# Following the steps above, make another model, but this time instead of removing the water vapor, remove the ozone!
# 
# Make another skew-T plot comparing all three model results.
# 
# If you have time, try a third case in which you remove both the water vapor and the ozone!

# In[ ]:





# ____________
# 
# ## 6. Summary of radiative equilibrium results
# ____________

# - We used the `RRTMG` radiation model with prescribed profiles of absorbing gases to calculate **pure radiative equilibrium** temperature profiles.
# - Radiative Equilibriu means the temperatures that the surface and air column would have **if radiation was the only physical process that could transfer energy between levels**.
# - We computed several different radiative equilibrium profiles, with and without key absorbing gases
#     - The profile without water vapor is **much colder at surface and lower troposphere**, but about the same in the stratosphere
#     - The profile without ozone is **much colder in the stratosphere**, but about the same near the surface.
#     - In fact there really isn't a stratosphere at all without ozone! The temperature is nearly isothermal in the upper atmosphere in that profile.

# However the really key takeaway message is that **none of these radiative equilibrium profiles look much like the observations in the troposphere**.
# 
# This strongly suggests that other physical processes (aside from radiation) are important in determining the observed temperature profile.

# Plotting on the skew-T diagram makes it clear that **all the radiative equilibrium profiles are statically unstable near the surface**.
# 
# The next step is therefore to look at the effects of convective mixing on the temperatures of the surface and lower troposphere.

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
