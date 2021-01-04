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

# %% [markdown] slideshow={"slide_type": "slide"}
# # Radiative Equilibrium
#
# This notebook is part of [The Climate Laboratory](https://brian-rose.github.io/ClimateLaboratoryBook) by [Brian E. J. Rose](http://www.atmos.albany.edu/facstaff/brose/index.html), University at Albany.

# %% [markdown]
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

# %% tags=["hide_input"]
#  This code is used just to create the skew-T plot of global, annual mean air temperature
# %matplotlib inline
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


# %% tags=["hide_input"]
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


# %% tags=["hide_input"]
skew = make_skewT()

# %% [markdown]
# Here we are going to work with some detailed **Single-Column Models** to understand questions such as
#
# - What physical factors actually determine this profile? 
# - Would the profile be different with different gases in the atmosphere?
# - What are the relative roles of **radiation** and **dynamics** (i.e. motion!) in setting this profile?
#
# We will start by **ignoring all processes except radiation**. We will calculate something called the **radiative equilibrium** temperature.

# %% [markdown]
# ____________
#
# ## 2. Radiative equilibrium -- the concept
# ____________

# %% [markdown]
# Models of radiative transfer slice up the atmospheric air column into a series of layer, and calculate the **emission** and **absorption** of radiation within each layer.
#
# It's really just a generalization of the model we already looked at:

# %% [markdown]
# ![Sketch of layer model](http://www.atmos.albany.edu/facstaff/brose/classes/ENV415_Spring2018/images/2layerAtm_sketch.png)

# %% [markdown]
# The concept of **radiative equilibrium** means that we **ignore all methods of heat exchange except for radiation**, and ask what temperature profile would exist under that assumption?
#
# We can answer that question by using a radiative transfer model to explicity compute the shortwave and longwave beams, and the warming/cooling of each layer associated with the radiative sources and sinks of energy.
#
# Basically, we reach radiative equilibrium when **energy is received and lost through radiation at the same rate in every layer**.

# %% [markdown]
# Because of the complicated dependence of emission/absorption features on the wavelength of radiation and the different gases, the beam is divided up into many different pieces representing different parts of the electromagnetic spectrum.
#
# We will not look explicitly at this complexity here, but we will **use a model** that represents these processes at the same level of detail we would in a GCM.

# %% [markdown]
# ____________
#
# ## 3. Setting up a single-column radiation model in climlab
# ____________

# %% [markdown]
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

# %% [markdown]
# We're going to use a model called the [Rapid Radiative Transfer Model](http://rtweb.aer.com/rrtm_frame.html) or RRTMG. This is a "serious" and widely-used radiation model, used in many comprehensive GCMs and Numerical Weather Prediction models.
#
# climlab provides an easy-to-use Python wrapper for the RRTMG code.

# %% [markdown]
# ### Water vapor data

# %% [markdown]
# Before setting up the model, we need some water vapor data. Why? Because our model needs to know how much water vapor exists at each vertical level, since water vapor is a radiatively important gas.
#
# We're actually going to use the specific humidity field from our CESM control simulation. We'll just take the global, time average of this data, and plot its vertical profile.

# %%
#  Load the model output as we have done before
cesm_data_path = "http://thredds.atmos.albany.edu:8080/thredds/dodsC/CESMA/"
atm_control = xr.open_dataset(cesm_data_path + "cpl_1850_f19/concatenated/cpl_1850_f19.cam.h0.nc")
#  The specific humidity is stored in the variable called Q in this dataset:
print(atm_control.Q)

# %% [markdown]
# Now take the global, annual average of the specific humidity:

# %%
# Take global, annual average of the specific humidity
weight_factor = atm_control.gw / atm_control.gw.mean(dim='lat')
Qglobal = (atm_control.Q * weight_factor).mean(dim=('lat','lon','time'))
# Take a look at what we just calculated ... it should be one-dimensional (vertical levels)
print(Qglobal)

# %% [markdown]
# And make a figure:

# %%
fig, ax = plt.subplots()
#  Multiply Qglobal by 1000 to put in units of grams water vapor per kg of air
ax.plot(Qglobal*1000., Qglobal.lev)
ax.invert_yaxis()
ax.set_ylabel('Pressure (hPa)')
ax.set_xlabel('Specific humidity (g/kg)')
ax.grid()

# %% [markdown]
# This shows a typical climatological humidity profile. Water vapor is a **trace gas**! But as we will see, it plays a very important role.
#
# Based on this figure, where is most of the water vapor?

# %% [markdown]
# ### Create a single-column model on the same grid as this water vapor data:

# %% [markdown]
# Here we will create the grid and state variables (air and surface temperature) for our single-column model.

# %%
import climlab
#  Make a model on same vertical domain as the GCM
mystate = climlab.column_state(lev=Qglobal.lev, water_depth=2.5)
print(mystate)

# %%
radmodel = climlab.radiation.RRTMG(name='Radiation (all gases)',  # give our model a name!
                              state=mystate,   # give our model an initial condition!
                              specific_humidity=Qglobal.values,  # tell the model how much water vapor there is
                              albedo = 0.25,  # this the SURFACE shortwave albedo
                              timestep = climlab.constants.seconds_per_day,  # set the timestep to one day (measured in seconds)
                             )
print(radmodel)

# %% [markdown]
# ### Explore the single-column model object

# %% [markdown]
# Look at a few interesting properties of the model we just created:

# %%
#  Here's the state dictionary we already created:
radmodel.state

# %%
#  Here are the pressure levels in hPa
radmodel.lev

# %% [markdown]
# There is a dictionary called `absorber_vmr` that holds the *volume mixing ratio* of all the radiatively active gases in the column:

# %%
radmodel.absorber_vmr

# %% [markdown]
# Most are just a single number because they are assumed to be **well mixed** in the atmosphere.
#
# The exception is ozone, which has a vertical structure taken from observations. Let's plot it

# %%
#  E.g. the CO2 content (a well-mixed gas) in parts per million
radmodel.absorber_vmr['CO2'] * 1E6

# %% [markdown]
# ### Python exercise: plot the ozone profile
#
# Make a simple plot showing the vertical structure of ozone, similar to the specific humidity plot we just made above.

# %%
# here is the data you need for the plot, as a plain numpy arrays:
print(radmodel.lev)
print(radmodel.absorber_vmr['O3'])

# %%

# %% [markdown]
# The other radiatively important gas is of course water vapor, which is stored separately in the `specific_humidity` attribute:

# %%
#  specific humidity in kg/kg, on the same pressure axis
print(radmodel.specific_humidity)

# %% [markdown] slideshow={"slide_type": "slide"}
# ### The RRTMG radiation model has lots of different input parameters
#
# For details you can look at the [documentation](http://climlab.readthedocs.io/en/latest/api/climlab.radiation.radiation.html)

# %% slideshow={"slide_type": "slide"}
for item in radmodel.input:
    print(item)

# %% [markdown] slideshow={"slide_type": "slide"}
# Many of the parameters control the **radiative effects of clouds**.
#
# But here we should note that the model is **initialized with no clouds at all**:

# %%
#  This is the fractional area covered by clouds in our column:
radmodel.cldfrac

# %% [markdown]
# ____________
#
# ## 4. Radiative equilibrium in the single-column model
# ____________

# %% [markdown]
# ### Step the model forward in time!

# %% [markdown]
# Here are the current temperatures (initial condition):

# %%
radmodel.Ts

# %%
radmodel.Tatm

# %% [markdown]
# Now let's take a single timestep:

# %%
radmodel.step_forward()

# %%
radmodel.Ts

# %% [markdown]
# The surface got warmer! 
#
# Let's take a look at all the diagnostic information that was generated during that timestep:

# %% [markdown]
# ### Diagnostic variables in our single-column model
#
# Every climlab model has a `diagnostics` dictionary. Here we are going to check it out as an `xarray` dataset:

# %%
climlab.to_xarray(radmodel.diagnostics)

# %% [markdown]
# The main "job" of a radiative transfer model it to calculate the shortwave and longwave fluxes up and down between each model layer.
#
# For example:

# %%
climlab.to_xarray(radmodel.LW_flux_up)

# %% [markdown]
# These are upward longwave fluxes in W/m2.
#
# Why are there 27 data points, when the model has 26 pressure levels?

# %%
radmodel.lev

# %%
radmodel.lev_bounds

# %% [markdown]
# The last element of the flux array represents the **upward flux from the surface to the first level**:

# %%
radmodel.LW_flux_up[-1]

# %% [markdown]
# The value is about 390 W m$^{-2}$. 
#
# Why?

# %%
sigma = 5.67E-8
sigma * 288**4

# %% [markdown]
# The surface temperature was initialized at 288 K, and the surface is treated as very close to a blackbody in the model.

# %% [markdown]
# What about the flux from the top layer out to space?
#
# Two ways to access this information:

# %%
radmodel.LW_flux_up[0]

# %%
radmodel.OLR

# %% [markdown]
# Of course there is a whole other set of fluxes for the shortwave radiation.
#
# One diagnostic we will often want to look at is the **net energy budget at the top of the atmosphere**:

# %%
radmodel.ASR - radmodel.OLR

# %% [markdown]
# ***Is the model gaining or losing energy?***

# %% [markdown]
# ### Integrate out to equilibrium
#
# Here I want to step forward in time until the model is very close to energy balance.
#
# We can use a `while` loop, conditional on the top-of-atmosphere imbalance:

# %%
while np.abs(radmodel.ASR - radmodel.OLR) > 0.01:
    radmodel.step_forward()

# %% [markdown]
# Check the energy budget again:

# %%
#  Check the energy budget again
radmodel.ASR - radmodel.OLR


# %% [markdown]
# Indeed, the imbalance is now small.

# %% [markdown]
# ### Compare the radiative equilibrium temperature to observations

# %% [markdown]
# Here's a helper function we'll use to add model temperature profiles to our skew-T plot:

# %%
def add_profile(skew, model, linestyle='-', color=None):
    line = skew.plot(model.lev, model.Tatm - climlab.constants.tempCtoK,
             label=model.name, linewidth=2)[0]
    skew.plot(1000, model.Ts - climlab.constants.tempCtoK, 'o', 
              markersize=8, color=line.get_color())
    skew.ax.legend()


# %%
skew = make_skewT()
add_profile(skew, radmodel)
skew.ax.set_title('Pure radiative equilibrium', fontsize=18);

# %% [markdown]
# What do you think about this model -- data comparison?

# %% [markdown]
# ____________
#
# ## 5. Effects of different gases on the radiative equilibrium profile
# ____________

# %% [markdown]
# **Models are for experimenting and playing with!**
#
# We have just built a single-column radiation model with several different absorbing gases. *We can learn about their effects by taking them away.*

# %% [markdown]
# ### Radiative equilibrium without water vapor

# %%
# Make an exact clone of our existing model
radmodel_noH2O = climlab.process_like(radmodel)
radmodel_noH2O.name = 'Radiation (no H2O)'
print(radmodel_noH2O)

# %%
#  Here is the water vapor profile we started with
radmodel_noH2O.specific_humidity

# %% [markdown]
# Now get rid of the water entirely!

# %%
radmodel_noH2O.specific_humidity *= 0.

# %%
radmodel_noH2O.specific_humidity

# %% [markdown]
# And run this new model forward to equilibrium:

# %%
#  it's useful to take a single step first before starting the while loop
#   because the diagnostics won't get updated 
#  (and thus show the effects of removing water vapor)
#  until we take a step forward
radmodel_noH2O.step_forward()
while np.abs(radmodel_noH2O.ASR - radmodel_noH2O.OLR) > 0.01:
    radmodel_noH2O.step_forward()

# %%
radmodel_noH2O.ASR - radmodel_noH2O.OLR

# %%
skew = make_skewT()
for model in [radmodel, radmodel_noH2O]:
    add_profile(skew, model)

# %% [markdown]
# What do you think you can learn from this about the radiative role of water vapor?

# %% [markdown]
# ### Exercise: radiative equilibrium without ozone
#
# Following the steps above, make another model, but this time instead of removing the water vapor, remove the ozone!
#
# Make another skew-T plot comparing all three model results.
#
# If you have time, try a third case in which you remove both the water vapor and the ozone!

# %%

# %% [markdown]
# ____________
#
# ## 6. Summary of radiative equilibrium results
# ____________

# %% [markdown]
# - We used the `RRTMG` radiation model with prescribed profiles of absorbing gases to calculate **pure radiative equilibrium** temperature profiles.
# - Radiative Equilibriu means the temperatures that the surface and air column would have **if radiation was the only physical process that could transfer energy between levels**.
# - We computed several different radiative equilibrium profiles, with and without key absorbing gases
#     - The profile without water vapor is **much colder at surface and lower troposphere**, but about the same in the stratosphere
#     - The profile without ozone is **much colder in the stratosphere**, but about the same near the surface.
#     - In fact there really isn't a stratosphere at all without ozone! The temperature is nearly isothermal in the upper atmosphere in that profile.

# %% [markdown]
# However the really key takeaway message is that **none of these radiative equilibrium profiles look much like the observations in the troposphere**.
#
# This strongly suggests that other physical processes (aside from radiation) are important in determining the observed temperature profile.

# %% [markdown]
# Plotting on the skew-T diagram makes it clear that **all the radiative equilibrium profiles are statically unstable near the surface**.
#
# The next step is therefore to look at the effects of convective mixing on the temperatures of the surface and lower troposphere.

# %% [markdown] slideshow={"slide_type": "skip"}
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
