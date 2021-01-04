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
# # Grey radiation modeling with climlab
#
# This notebook is part of [The Climate Laboratory](https://brian-rose.github.io/ClimateLaboratoryBook) by [Brian E. J. Rose](http://www.atmos.albany.edu/facstaff/brose/index.html), University at Albany.

# %% [markdown]
# ____________
# <a id='section1'></a>
#
# ## 1. Introducing `climlab`
# ____________
#
# ``climlab`` is a flexible engine for process-oriented climate modeling.
# It is based on a very general concept of a model as a collection of individual, 
# interacting processes. ``climlab`` defines a base class called ``Process``, which
# can contain an arbitrarily complex tree of sub-processes (each also some 
# sub-class of ``Process``). Every climate process (radiative, dynamical, 
# physical, turbulent, convective, chemical, etc.) can be simulated as a stand-alone
# process model given appropriate input, or as a sub-process of a more complex model. 
# New classes of model can easily be defined and run interactively by putting together an
# appropriate collection of sub-processes.
#
# ``climlab`` is a work-in-progress, and the code base will evolve substantially over the course of this semester.
# The latest code can always be found on ``github``:
#
# https://github.com/brian-rose/climlab
#
# You are strongly encouraged to clone the ``climlab`` repository and use ``git`` to keep your local copy up-to-date.
#
# Running this notebook requires that ``climlab`` is already installed on your system.

# %%
# %matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from numpy import cos, deg2rad, log
import climlab

# %% [markdown]
# ____________
# <a id='section2'></a>
#
# ## 2. Using `climlab` to implement the two-layer leaky greenhouse model
# ____________
#
# One of the things that ``climlab`` is set up to do is the grey-radiation modeling we have already been discussing.
#
# Since we already derived a [complete analytical solution to the two-layer leaky greenhouse model](Lecture06 -- Elementary greenhouse models.ipynb), we will use this to validate the `climlab` code.
#
#

# %% [markdown]
# ### Validation
#
# We want to verify that the model reproduces the observed OLR given observed temperatures, and the absorptivity that we tuned in the analytical model. The target numbers are:
#
# \begin{align}
# T_s &= 288 \text{ K} \\
# T_0 &= 275 \text{ K} \\
# T_1 &= 230 \text{ K} \\
# \end{align}
#
# $$ \epsilon = 0.586  $$
#
# $$ OLR = 238.5 \text{ W m}^{-2} $$
#

# %% [markdown]
# ### Initialize a model in `climlab`
# The first thing we do is create a new model.
#
# The following example code is sparsely commented but will hopefully orient you on the basics of defining and working with a `climlab Process` object.

# %%
#  Test in a 2-layer atmosphere
col = climlab.GreyRadiationModel(num_lev=2)
print( col)

# %%
col.subprocess

# %% [markdown]
# Every item in the above dictionary is itself an instance of the `climlab.Process` object:

# %%
print( col.subprocess['LW'])

# %% [markdown]
# The `state` dictionary holds the state variables of the model. In this case, temperatures:

# %%
climlab.to_xarray(col.state)

# %% [markdown]
# Access these either through dictionary methods or as attributes of the model object:

# %%
print( col.state['Ts'])
print( col.Ts)
col.Ts is col.state['Ts']

# %% [markdown]
# Now we are assigning the "observed" temperatures to our model state:

# %%
col.Ts[:] = 288.
col.Tatm[:] = np.array([230., 275.])
climlab.to_xarray(col.state)

# %%
LW = col.subprocess['LW']
print(LW)

# %%
LW.absorptivity

# %%
#  copying the tuned value of epsilon from Lecture 6 notes
LW.absorptivity = 0.586
LW.absorptivity

# %%
#  This does all the calculations that would be performed at each time step, 
#  but doesn't actually update the temperatures
col.compute_diagnostics()
#  Print out the dictionary
col.diagnostics

# %%
#  Check OLR against our analytical solution
col.OLR

# %%
# Like the state variables, the diagnostics can also be accessed in two different ways
col.diagnostics['OLR']

# %%
col.state

# %%
# perform a single time step
col.step_forward()

# %%
col.state

# %% [markdown]
# We just stepped forward one discreet unit in time. Because we didn't specify a timestep when we created the model, it is set to a default value:

# %%
col.timestep

# %% [markdown]
# which is 1 day (expressed in seconds).

# %% [markdown]
# Now we will integrate the model out to equilibrium.
#
# We could easily write a loop to call the `step_forward()` method many times.
#
# Or use a handy shortcut that allows us to specify the integration length in physical time units:

# %%
# integrate out to radiative equilibrium
col.integrate_years(2.)

# %%
# Check for equilibrium
col.ASR - col.OLR

# %%
#  The temperatures at radiative equilibrium
col.state

# %% [markdown]
# Compare these to the analytical solutions for radiative equilibrium with $\epsilon = 0.58$:
#
# \begin{align}
# T_s &= 296.4 \text{ K} \\
# T_0 &= 262.3 \text{ K} \\
# T_1 &= 233.8 \text{ K} \\
# \end{align}
#

# %% [markdown]
# So it looks like `climlab` agrees with our analytical results to within 0.1 K. That's good.

# %% [markdown]
# ____________
# <a id='section3'></a>
#
# ## 3. The observed annual, global mean temperature profile
# ____________
#
# We want to model the OLR in a column whose temperatures match observations. As we've done before, we'll calculate the global, annual mean air temperature from the NCEP Reanalysis data.

# %%
## The NOAA ESRL server is shutdown! January 2019
## This will try to read the data over the internet.
ncep_filename = 'air.mon.1981-2010.ltm.nc'
##  to read over internet
ncep_url = "http://www.esrl.noaa.gov/psd/thredds/dodsC/Datasets/ncep.reanalysis.derived/pressure/"
path = ncep_url
##  Open handle to data
ncep_air = xr.open_dataset( path + ncep_filename, decode_times=False )

#url = 'http://apdrc.soest.hawaii.edu:80/dods/public_data/Reanalysis_Data/NCEP/NCEP/clima/pressure/air'
#air = xr.open_dataset(url)
# The name of the vertical axis is different than the NOAA ESRL version..
#ncep_air = air.rename({'lev': 'level'})
print( ncep_air)

# %%
#  Take global, annual average and convert to Kelvin
weight = cos(deg2rad(ncep_air.lat)) / cos(deg2rad(ncep_air.lat)).mean(dim='lat')
Tglobal = (ncep_air.air * weight).mean(dim=('lat','lon','time'))
print( Tglobal)

# %% [markdown]
# We're going to convert this to degrees Kelvin, using a handy list of pre-defined constants in `climlab.constants`

# %%
climlab.constants.tempCtoK

# %%
Tglobal += climlab.constants.tempCtoK
print(Tglobal)


# %%
#  A handy re-usable routine for making a plot of the temperature profiles
#  We will plot temperatures with respect to log(pressure) to get a height-like coordinate

def zstar(lev):
    return -np.log(lev / climlab.constants.ps)

def plot_soundings(result_list, name_list, plot_obs=True, fixed_range=True):
    color_cycle=['r', 'g', 'b', 'y']
    # col is either a column model object or a list of column model objects
    #if isinstance(state_list, climlab.Process):
    #    # make a list with a single item
    #    collist = [collist]
    fig, ax = plt.subplots(figsize=(9,9))
    if plot_obs:
        ax.plot(Tglobal, zstar(Tglobal.level), color='k', label='Observed')    
    for i, state in enumerate(result_list):
        Tatm = state['Tatm']
        lev = Tatm.domain.axes['lev'].points
        Ts = state['Ts']
        ax.plot(Tatm, zstar(lev), color=color_cycle[i], label=name_list[i])
        ax.plot(Ts, 0, 'o', markersize=12, color=color_cycle[i])
    #ax.invert_yaxis()
    yticks = np.array([1000., 750., 500., 250., 100., 50., 20., 10., 5.])
    ax.set_yticks(-np.log(yticks/1000.))
    ax.set_yticklabels(yticks)
    ax.set_xlabel('Temperature (K)', fontsize=14)
    ax.set_ylabel('Pressure (hPa)', fontsize=14)
    ax.grid()
    ax.legend()
    if fixed_range:
        ax.set_xlim([200, 300])
        ax.set_ylim(zstar(np.array([1000., 5.])))
    #ax2 = ax.twinx()
    
    return ax


# %%
plot_soundings([],[] );

# %% [markdown]
# ____________
# <a id='section4'></a>
#
# ## 4. A 30-layer model using the observed temperatures
# ____________
#
#

# %%
#  initialize a grey radiation model with 30 levels
col = climlab.GreyRadiationModel()
print(col)

# %%
col.lev

# %%
col.lev_bounds

# %%
# interpolate to 30 evenly spaced pressure levels
lev = col.lev
Tinterp = np.interp(lev, np.flipud(Tglobal.level), np.flipud(Tglobal))
Tinterp
#  Need to 'flipud' because the interpolation routine 
#  needs the pressure data to be in increasing order

# %%
# Initialize model with observed temperatures
col.Ts[:] = Tglobal[0]
col.Tatm[:] = Tinterp

# %%
# This should look just like the observations
result_list = [col.state]
name_list = ['Observed, interpolated']
plot_soundings(result_list, name_list);

# %% [markdown]
# ### Tune absorptivity to get observed OLR

# %%
col.compute_diagnostics()
col.OLR

# %%
# Need to tune absorptivity to get OLR = 238.5
epsarray = np.linspace(0.01, 0.1, 100)
OLRarray = np.zeros_like(epsarray)

# %%
for i in range(epsarray.size):
    col.subprocess['LW'].absorptivity = epsarray[i]
    col.compute_diagnostics()
    OLRarray[i] = col.OLR

plt.plot(epsarray, OLRarray)
plt.grid()
plt.xlabel('epsilon')
plt.ylabel('OLR')


# %% [markdown]
# The necessary value seems to lie near 0.055 or so.
#
# We can be more precise with a numerical root-finder.

# %%
def OLRanom(eps):
    col.subprocess['LW'].absorptivity = eps
    col.compute_diagnostics()
    return col.OLR - 238.5


# %%
# Use numerical root-finding to get the equilibria
from scipy.optimize import brentq
# brentq is a root-finding function
#  Need to give it a function and two end-points
#  It will look for a zero of the function between those end-points
eps = brentq(OLRanom, 0.01, 0.1)
print( eps)

# %%
col.subprocess.LW.absorptivity = eps
col.subprocess.LW.absorptivity

# %%
col.compute_diagnostics()
col.OLR

# %% [markdown]
# ____________
# <a id='section5'></a>
#
# ## 5. Radiative forcing in the 30-layer model
# ____________
#
# Let's compute radiative forcing for a **2% increase in absorptivity**.

# %%
#  clone our model using a built-in climlab function
col2 = climlab.process_like(col)
print(col2)

# %%
col2.subprocess['LW'].absorptivity *= 1.02
col2.subprocess['LW'].absorptivity

# %%
#  Radiative forcing by definition is the change in TOA radiative flux,
# HOLDING THE TEMPERATURES FIXED.
col2.Ts - col.Ts

# %%
col2.Tatm - col.Tatm

# %%
col2.compute_diagnostics()
col2.OLR

# %% [markdown]
# The OLR decreased after we added the extra absorbers, as we expect. Now we can calculate the Radiative Forcing:

# %%
RF = -(col2.OLR - col.OLR)
print( 'The radiative forcing is %.2f W/m2.' %RF)

# %% [markdown]
# ____________
# <a id='section6'></a>
#
# ## 6. Radiative equilibrium in the 30-layer model
# ____________
#

# %%
re = climlab.process_like(col)

# %%
#  To get to equilibrium, we just time-step the model forward long enough
re.integrate_years(1.)

# %%
#  Check for energy balance
print( 'The net downward radiative flux at TOA is %.4f W/m2.' %(re.ASR - re.OLR))

# %%
result_list.append(re.state)
name_list.append('Radiative equilibrium (grey gas)')
plot_soundings(result_list, name_list)

# %% [markdown]
# Some properties of the **radiative equilibrium** temperature profile:
#
# - The surface is warmer than observed.
# - The lower troposphere is colder than observed.
# - Very cold air is sitting immediately above the warm surface.
# - There is no tropopause, no stratosphere.

# %% [markdown]
# ____________
# <a id='section7'></a>
#
# ## 7. Radiative-Convective Equilibrium in the 30-layer model
# ____________
#
# We recognize that the large drop in temperature just above the surface is unphysical. Parcels of air in direct contact with the ground will be warmed by mechansisms other than radiative transfer.
#
# These warm air parcels will then become buoyant, and will convect upward, mixing their heat content with the environment.
#
# We **parameterize** the statistical effects of this mixing through a **convective adjustment**. 
#
# At each timestep, our model checks for any locations at which the **lapse rate** exceeds some threshold. Unstable layers are removed through an energy-conserving mixing formula.
#
# This process is assumed to be fast relative to radiative heating. In the model, it is instantaneous.

# %% [markdown]
# ### Add the convective adjustment as an additional subprocess

# %%
#  Here is the existing model
print(re)

# %%
#  First we make a new clone
rce = climlab.process_like(re)
#  Then create a new ConvectiveAdjustment process
conv = climlab.convection.ConvectiveAdjustment(state=rce.state, 
                                               adj_lapse_rate=6.)
#  And add it to our model
rce.add_subprocess('Convective Adjustment', conv)
print( rce)

# %% [markdown]
# This model is exactly like our previous models, except for one additional subprocess called ``Convective Adjustment``. 
#
# We passed a parameter ``adj_lapse_rate`` (in K / km) that sets the neutrally stable lapse rate -- in this case, 6 K / km.
#
# This number is chosed to very loosely represent the net effect of **moist convection**.

# %%
#  Run out to equilibrium
rce.integrate_years(1.)

# %%
#  Check for energy balance
rce.ASR - rce.OLR

# %%
result_list.append(rce.state)
name_list.append('Radiatve-Convective equilibrium (grey gas)')

# %%
plot_soundings(result_list, name_list)

# %% [markdown]
# Introducing convective adjustment into the model cools the surface quite a bit (compared to Radiative Equilibrium, in green here) -- and warms the lower troposphere. It gives us a MUCH better fit to observations.
#
# But of course we still have no stratosphere.

# %% [markdown]
# ____________
# <a id='section8'></a>
#
# ## 8. Putting stratospheric ozone in the grey-gas model
# ____________
#
# Our model has no equivalent of the stratosphere, where temperature increases with height. That's because our model has been completely transparent to shortwave radiation up until now.
#
# We can load the observed ozone climatology from the input files for the CESM model:

# %%
datapath = "http://thredds.atmos.albany.edu:8080/thredds/dodsC/CESMA/"
ozone = xr.open_dataset( datapath + "som_input/ozone_1.9x2.5_L26_2000clim_c091112.nc")

# %%
print(ozone)

# %% [markdown]
# The pressure levels in this dataset are:

# %%
print(ozone.lev)

# %% [markdown]
# ### Take the global average of the ozone climatology, and plot it as a function of pressure (or height)

# %%
#  Take global, annual average and convert to Kelvin
weight_ozone = cos(deg2rad(ozone.lat)) / cos(deg2rad(ozone.lat)).mean(dim='lat')
O3_global = (ozone.O3 * weight_ozone).mean(dim=('lat','lon','time'))
print(O3_global)

# %%
ax = plt.figure(figsize=(10,8)).add_subplot(111)
ax.plot( O3_global * 1.E6, -np.log(ozone.lev/climlab.constants.ps) )
ax.set_xlabel('Ozone (ppm)', fontsize=16)
ax.set_ylabel('Pressure (hPa)', fontsize=16 )
yticks = np.array([1000., 750., 500., 250., 100., 50., 20., 10., 5.])
ax.set_yticks(-np.log(yticks/1000.))
ax.set_yticklabels(yticks)
ax.grid()
ax.set_title('Global, annual mean ozone concentration', fontsize = 24);

# %% [markdown]
# This shows that most of the ozone is indeed in the stratosphere, and peaks near the top of the stratosphere.
#
# Now create a new column model object **on the same pressure levels as the ozone data**.  We are also going set an adjusted lapse rate of 6 K / km.

# %%
# the RadiativeConvectiveModel is pre-defined in climlab
#  It contains the same components are our previous model
#   But here we are specifying a different set of vertical levels.
oz_col = climlab.RadiativeConvectiveModel(lev = ozone.lev, adj_lapse_rate=6)
print(oz_col)

# %% [markdown]
# Now we will do something new: let the column absorb some shortwave radiation. We will assume that the shortwave absorptivity is proportional to the ozone concentration we plotted above. 

# %% [markdown]
# Now we need to weight the absorptivity by the pressure (mass) of each layer.

# %%
# This number is an arbitrary parameter that scales how absorptive we are making the ozone
# in our grey gas model
ozonefactor = 75
dp = oz_col.Tatm.domain.lev.delta
epsSW = O3_global.values * dp * ozonefactor

# %% [markdown]
# We want to use the field `epsSW` as the absorptivity for our SW radiation model.
#
# Let's see what the absorptivity is current set to:

# %%
print(oz_col.subprocess['SW'].absorptivity)

# %% [markdown]
# It defaults to zero.
#
# Before changing this (putting in the ozone), let's take a look at the shortwave absorption in the column:

# %%
oz_col.compute_diagnostics()

# %%
oz_col.diagnostics['SW_absorbed_atm']

# %% [markdown]
# Let's now put in the ozone:

# %%
oz_col.subprocess['SW'].absorptivity = epsSW
print(oz_col.subprocess['SW'].absorptivity)

# %% [markdown]
# Let's check how this changes the SW absorption:

# %%
oz_col.compute_diagnostics()
oz_col.SW_absorbed_atm

# %% [markdown]
# It is now non-zero, and largest near the top of the column (also top of the array) where the ozone concentration is highest.

# %% [markdown]
# Now it's time to run the model out to radiative-convective equilibrium

# %%
oz_col.integrate_years(1.)

# %%
print(oz_col.ASR - oz_col.OLR)

# %% [markdown]
# And let's now see what we got!

# %%
result_list.append(oz_col.state)
name_list.append('Radiative-Convective equilibrium with O3')

# %%
#  Make a plot to compare observations, Radiative Equilibrium, Radiative-Convective Equilibrium, and RCE with ozone!
plot_soundings(result_list, name_list)

# %% [markdown]
# And we finally have something that looks looks like the tropopause, with temperature increasing above at approximately the correct rate. 
#
# There are still plenty of discrepancies between this model solution and the observations, including:
#
# - Tropopause temperature is too warm, by about 15 degrees.
# - Surface temperature is too cold
#
# There are a number of parameters we might adjust if we wanted to improve the fit, including:
#
# - Longwave absorptivity
# - Surface albedo
#
# Feel free to experiment! (That's what models are for, after all).

# %% [markdown]
# ### The take home message
#
# The dominant effect of stratospheric ozone is to vastly increase the radiative equilibrium temperature in the ozone layer. The temperature needs to be higher so that the longwave emission can balance the shortwave absorption.
#
# Without ozone to absorb incoming solar radiation, the **temperature does not increase with height**.
#
# This simple grey-gas model illustrates this principle very clearly.

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

# %%
