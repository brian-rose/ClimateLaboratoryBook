---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.12
    jupytext_version: 1.6.0
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

(nb:grey-radiation)=
# Grey radiation modeling with climlab

This notebook is part of [The Climate Laboratory](https://brian-rose.github.io/ClimateLaboratoryBook) by [Brian E. J. Rose](http://www.atmos.albany.edu/facstaff/brose/index.html), University at Albany.

+++

____________
<a id='section1'></a>

## 1. Introducing `climlab`
____________

``climlab`` is a flexible engine for process-oriented climate modeling.
It is based on a very general concept of a model as a collection of individual, 
interacting processes. ``climlab`` defines a base class called ``Process``, which
can contain an arbitrarily complex tree of sub-processes (each also some 
sub-class of ``Process``). Every climate process (radiative, dynamical, 
physical, turbulent, convective, chemical, etc.) can be simulated as a stand-alone
process model given appropriate input, or as a sub-process of a more complex model. 
New classes of model can easily be defined and run interactively by putting together an
appropriate collection of sub-processes.

``climlab`` is a work-in-progress, and the code base will evolve substantially over the course of this semester.
The latest code can always be found on ``github``:

https://github.com/brian-rose/climlab

You are strongly encouraged to clone the ``climlab`` repository and use ``git`` to keep your local copy up-to-date.

Running this notebook requires that ``climlab`` is already installed on your system.

```{code-cell} ipython3
%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from numpy import cos, deg2rad, log
import climlab
```

____________
<a id='section2'></a>

## 2. Using `climlab` to implement the two-layer leaky greenhouse model
____________

One of the things that ``climlab`` is set up to do is the grey-radiation modeling we have already been discussing.

Since we already derived a [complete analytical solution to the two-layer leaky greenhouse model](Lecture06 -- Elementary greenhouse models.ipynb), we will use this to validate the `climlab` code.


+++

### Validation

We want to verify that the model reproduces the observed OLR given observed temperatures, and the absorptivity that we tuned in the analytical model. The target numbers are:

\begin{align}
T_s &= 288 \text{ K} \\
T_0 &= 275 \text{ K} \\
T_1 &= 230 \text{ K} \\
\end{align}

$$ \epsilon = 0.586  $$

$$ OLR = 238.5 \text{ W m}^{-2} $$

+++

### Initialize a model in `climlab`
The first thing we do is create a new model.

The following example code is sparsely commented but will hopefully orient you on the basics of defining and working with a `climlab Process` object.

```{code-cell} ipython3
#  Test in a 2-layer atmosphere
col = climlab.GreyRadiationModel(num_lev=2)
print( col)
```

```{code-cell} ipython3
col.subprocess
```

Every item in the above dictionary is itself an instance of the `climlab.Process` object:

```{code-cell} ipython3
print( col.subprocess['LW'])
```

The `state` dictionary holds the state variables of the model. In this case, temperatures:

```{code-cell} ipython3
climlab.to_xarray(col.state)
```

Access these either through dictionary methods or as attributes of the model object:

```{code-cell} ipython3
print( col.state['Ts'])
print( col.Ts)
col.Ts is col.state['Ts']
```

Now we are assigning the "observed" temperatures to our model state:

```{code-cell} ipython3
col.Ts[:] = 288.
col.Tatm[:] = np.array([230., 275.])
climlab.to_xarray(col.state)
```

```{code-cell} ipython3
LW = col.subprocess['LW']
print(LW)
```

```{code-cell} ipython3
LW.absorptivity
```

```{code-cell} ipython3
#  copying the tuned value of epsilon from Lecture 6 notes
LW.absorptivity = 0.586
LW.absorptivity
```

```{code-cell} ipython3
#  This does all the calculations that would be performed at each time step, 
#  but doesn't actually update the temperatures
col.compute_diagnostics()
#  Print out the dictionary
col.diagnostics
```

```{code-cell} ipython3
#  Check OLR against our analytical solution
col.OLR
```

```{code-cell} ipython3
# Like the state variables, the diagnostics can also be accessed in two different ways
col.diagnostics['OLR']
```

```{code-cell} ipython3
col.state
```

```{code-cell} ipython3
# perform a single time step
col.step_forward()
```

```{code-cell} ipython3
col.state
```

We just stepped forward one discreet unit in time. Because we didn't specify a timestep when we created the model, it is set to a default value:

```{code-cell} ipython3
col.timestep
```

which is 1 day (expressed in seconds).

+++

Now we will integrate the model out to equilibrium.

We could easily write a loop to call the `step_forward()` method many times.

Or use a handy shortcut that allows us to specify the integration length in physical time units:

```{code-cell} ipython3
# integrate out to radiative equilibrium
col.integrate_years(2.)
```

```{code-cell} ipython3
# Check for equilibrium
col.ASR - col.OLR
```

```{code-cell} ipython3
#  The temperatures at radiative equilibrium
col.state
```

Compare these to the analytical solutions for radiative equilibrium with $\epsilon = 0.58$:

\begin{align}
T_s &= 296.4 \text{ K} \\
T_0 &= 262.3 \text{ K} \\
T_1 &= 233.8 \text{ K} \\
\end{align}

+++

So it looks like `climlab` agrees with our analytical results to within 0.1 K. That's good.

+++

____________
<a id='section3'></a>

## 3. The observed annual, global mean temperature profile
____________

We want to model the OLR in a column whose temperatures match observations. As we've done before, we'll calculate the global, annual mean air temperature from the NCEP Reanalysis data.

```{code-cell} ipython3
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
```

```{code-cell} ipython3
#  Take global, annual average and convert to Kelvin
weight = cos(deg2rad(ncep_air.lat)) / cos(deg2rad(ncep_air.lat)).mean(dim='lat')
Tglobal = (ncep_air.air * weight).mean(dim=('lat','lon','time'))
print( Tglobal)
```

We're going to convert this to degrees Kelvin, using a handy list of pre-defined constants in `climlab.constants`

```{code-cell} ipython3
climlab.constants.tempCtoK
```

```{code-cell} ipython3
Tglobal += climlab.constants.tempCtoK
print(Tglobal)
```

```{code-cell} ipython3
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
```

```{code-cell} ipython3
plot_soundings([],[] );
```

____________
<a id='section4'></a>

## 4. A 30-layer model using the observed temperatures
____________


```{code-cell} ipython3
#  initialize a grey radiation model with 30 levels
col = climlab.GreyRadiationModel()
print(col)
```

```{code-cell} ipython3
col.lev
```

```{code-cell} ipython3
col.lev_bounds
```

```{code-cell} ipython3
# interpolate to 30 evenly spaced pressure levels
lev = col.lev
Tinterp = np.interp(lev, np.flipud(Tglobal.level), np.flipud(Tglobal))
Tinterp
#  Need to 'flipud' because the interpolation routine 
#  needs the pressure data to be in increasing order
```

```{code-cell} ipython3
# Initialize model with observed temperatures
col.Ts[:] = Tglobal[0]
col.Tatm[:] = Tinterp
```

```{code-cell} ipython3
# This should look just like the observations
result_list = [col.state]
name_list = ['Observed, interpolated']
plot_soundings(result_list, name_list);
```

### Tune absorptivity to get observed OLR

```{code-cell} ipython3
col.compute_diagnostics()
col.OLR
```

```{code-cell} ipython3
# Need to tune absorptivity to get OLR = 238.5
epsarray = np.linspace(0.01, 0.1, 100)
OLRarray = np.zeros_like(epsarray)
```

```{code-cell} ipython3
for i in range(epsarray.size):
    col.subprocess['LW'].absorptivity = epsarray[i]
    col.compute_diagnostics()
    OLRarray[i] = col.OLR

plt.plot(epsarray, OLRarray)
plt.grid()
plt.xlabel('epsilon')
plt.ylabel('OLR')
```

The necessary value seems to lie near 0.055 or so.

We can be more precise with a numerical root-finder.

```{code-cell} ipython3
def OLRanom(eps):
    col.subprocess['LW'].absorptivity = eps
    col.compute_diagnostics()
    return col.OLR - 238.5
```

```{code-cell} ipython3
# Use numerical root-finding to get the equilibria
from scipy.optimize import brentq
# brentq is a root-finding function
#  Need to give it a function and two end-points
#  It will look for a zero of the function between those end-points
eps = brentq(OLRanom, 0.01, 0.1)
print( eps)
```

```{code-cell} ipython3
col.subprocess.LW.absorptivity = eps
col.subprocess.LW.absorptivity
```

```{code-cell} ipython3
col.compute_diagnostics()
col.OLR
```

____________
<a id='section5'></a>

## 5. Radiative forcing in the 30-layer model
____________

Let's compute radiative forcing for a **2% increase in absorptivity**.

```{code-cell} ipython3
#  clone our model using a built-in climlab function
col2 = climlab.process_like(col)
print(col2)
```

```{code-cell} ipython3
col2.subprocess['LW'].absorptivity *= 1.02
col2.subprocess['LW'].absorptivity
```

```{code-cell} ipython3
#  Radiative forcing by definition is the change in TOA radiative flux,
# HOLDING THE TEMPERATURES FIXED.
col2.Ts - col.Ts
```

```{code-cell} ipython3
col2.Tatm - col.Tatm
```

```{code-cell} ipython3
col2.compute_diagnostics()
col2.OLR
```

The OLR decreased after we added the extra absorbers, as we expect. Now we can calculate the Radiative Forcing:

```{code-cell} ipython3
RF = -(col2.OLR - col.OLR)
print( 'The radiative forcing is %.2f W/m2.' %RF)
```

____________
<a id='section6'></a>

## 6. Radiative equilibrium in the 30-layer model
____________

```{code-cell} ipython3
re = climlab.process_like(col)
```

```{code-cell} ipython3
#  To get to equilibrium, we just time-step the model forward long enough
re.integrate_years(1.)
```

```{code-cell} ipython3
#  Check for energy balance
print( 'The net downward radiative flux at TOA is %.4f W/m2.' %(re.ASR - re.OLR))
```

```{code-cell} ipython3
result_list.append(re.state)
name_list.append('Radiative equilibrium (grey gas)')
plot_soundings(result_list, name_list)
```

Some properties of the **radiative equilibrium** temperature profile:

- The surface is warmer than observed.
- The lower troposphere is colder than observed.
- Very cold air is sitting immediately above the warm surface.
- There is no tropopause, no stratosphere.

+++

____________
<a id='section7'></a>

## 7. Radiative-Convective Equilibrium in the 30-layer model
____________

We recognize that the large drop in temperature just above the surface is unphysical. Parcels of air in direct contact with the ground will be warmed by mechansisms other than radiative transfer.

These warm air parcels will then become buoyant, and will convect upward, mixing their heat content with the environment.

We **parameterize** the statistical effects of this mixing through a **convective adjustment**. 

At each timestep, our model checks for any locations at which the **lapse rate** exceeds some threshold. Unstable layers are removed through an energy-conserving mixing formula.

This process is assumed to be fast relative to radiative heating. In the model, it is instantaneous.

+++

### Add the convective adjustment as an additional subprocess

```{code-cell} ipython3
#  Here is the existing model
print(re)
```

```{code-cell} ipython3
#  First we make a new clone
rce = climlab.process_like(re)
#  Then create a new ConvectiveAdjustment process
conv = climlab.convection.ConvectiveAdjustment(state=rce.state, 
                                               adj_lapse_rate=6.)
#  And add it to our model
rce.add_subprocess('Convective Adjustment', conv)
print( rce)
```

This model is exactly like our previous models, except for one additional subprocess called ``Convective Adjustment``. 

We passed a parameter ``adj_lapse_rate`` (in K / km) that sets the neutrally stable lapse rate -- in this case, 6 K / km.

This number is chosed to very loosely represent the net effect of **moist convection**.

```{code-cell} ipython3
#  Run out to equilibrium
rce.integrate_years(1.)
```

```{code-cell} ipython3
#  Check for energy balance
rce.ASR - rce.OLR
```

```{code-cell} ipython3
result_list.append(rce.state)
name_list.append('Radiatve-Convective equilibrium (grey gas)')
```

```{code-cell} ipython3
plot_soundings(result_list, name_list)
```

Introducing convective adjustment into the model cools the surface quite a bit (compared to Radiative Equilibrium, in green here) -- and warms the lower troposphere. It gives us a MUCH better fit to observations.

But of course we still have no stratosphere.

+++

____________
<a id='section8'></a>

## 8. Putting stratospheric ozone in the grey-gas model
____________

Our model has no equivalent of the stratosphere, where temperature increases with height. That's because our model has been completely transparent to shortwave radiation up until now.

We can load the observed ozone climatology from the input files for the CESM model:

```{code-cell} ipython3
datapath = "http://thredds.atmos.albany.edu:8080/thredds/dodsC/CESMA/"
ozone = xr.open_dataset( datapath + "som_input/ozone_1.9x2.5_L26_2000clim_c091112.nc")
```

```{code-cell} ipython3
print(ozone)
```

The pressure levels in this dataset are:

```{code-cell} ipython3
print(ozone.lev)
```

### Take the global average of the ozone climatology, and plot it as a function of pressure (or height)

```{code-cell} ipython3
#  Take global, annual average and convert to Kelvin
weight_ozone = cos(deg2rad(ozone.lat)) / cos(deg2rad(ozone.lat)).mean(dim='lat')
O3_global = (ozone.O3 * weight_ozone).mean(dim=('lat','lon','time'))
print(O3_global)
```

```{code-cell} ipython3
ax = plt.figure(figsize=(10,8)).add_subplot(111)
ax.plot( O3_global * 1.E6, -np.log(ozone.lev/climlab.constants.ps) )
ax.set_xlabel('Ozone (ppm)', fontsize=16)
ax.set_ylabel('Pressure (hPa)', fontsize=16 )
yticks = np.array([1000., 750., 500., 250., 100., 50., 20., 10., 5.])
ax.set_yticks(-np.log(yticks/1000.))
ax.set_yticklabels(yticks)
ax.grid()
ax.set_title('Global, annual mean ozone concentration', fontsize = 24);
```

This shows that most of the ozone is indeed in the stratosphere, and peaks near the top of the stratosphere.

Now create a new column model object **on the same pressure levels as the ozone data**.  We are also going set an adjusted lapse rate of 6 K / km.

```{code-cell} ipython3
# the RadiativeConvectiveModel is pre-defined in climlab
#  It contains the same components are our previous model
#   But here we are specifying a different set of vertical levels.
oz_col = climlab.RadiativeConvectiveModel(lev = ozone.lev, adj_lapse_rate=6)
print(oz_col)
```

Now we will do something new: let the column absorb some shortwave radiation. We will assume that the shortwave absorptivity is proportional to the ozone concentration we plotted above. 

+++

Now we need to weight the absorptivity by the pressure (mass) of each layer.

```{code-cell} ipython3
# This number is an arbitrary parameter that scales how absorptive we are making the ozone
# in our grey gas model
ozonefactor = 75
dp = oz_col.Tatm.domain.lev.delta
epsSW = O3_global.values * dp * ozonefactor
```

We want to use the field `epsSW` as the absorptivity for our SW radiation model.

Let's see what the absorptivity is current set to:

```{code-cell} ipython3
print(oz_col.subprocess['SW'].absorptivity)
```

It defaults to zero.

Before changing this (putting in the ozone), let's take a look at the shortwave absorption in the column:

```{code-cell} ipython3
oz_col.compute_diagnostics()
```

```{code-cell} ipython3
oz_col.diagnostics['SW_absorbed_atm']
```

Let's now put in the ozone:

```{code-cell} ipython3
oz_col.subprocess['SW'].absorptivity = epsSW
print(oz_col.subprocess['SW'].absorptivity)
```

Let's check how this changes the SW absorption:

```{code-cell} ipython3
oz_col.compute_diagnostics()
oz_col.SW_absorbed_atm
```

It is now non-zero, and largest near the top of the column (also top of the array) where the ozone concentration is highest.

+++

Now it's time to run the model out to radiative-convective equilibrium

```{code-cell} ipython3
oz_col.integrate_years(1.)
```

```{code-cell} ipython3
print(oz_col.ASR - oz_col.OLR)
```

And let's now see what we got!

```{code-cell} ipython3
result_list.append(oz_col.state)
name_list.append('Radiative-Convective equilibrium with O3')
```

```{code-cell} ipython3
#  Make a plot to compare observations, Radiative Equilibrium, Radiative-Convective Equilibrium, and RCE with ozone!
plot_soundings(result_list, name_list)
```

And we finally have something that looks looks like the tropopause, with temperature increasing above at approximately the correct rate. 

There are still plenty of discrepancies between this model solution and the observations, including:

- Tropopause temperature is too warm, by about 15 degrees.
- Surface temperature is too cold

There are a number of parameters we might adjust if we wanted to improve the fit, including:

- Longwave absorptivity
- Surface albedo

Feel free to experiment! (That's what models are for, after all).

+++

### The take home message

The dominant effect of stratospheric ozone is to vastly increase the radiative equilibrium temperature in the ozone layer. The temperature needs to be higher so that the longwave emission can balance the shortwave absorption.

Without ozone to absorb incoming solar radiation, the **temperature does not increase with height**.

This simple grey-gas model illustrates this principle very clearly.

+++ {"slideshow": {"slide_type": "skip"}}

____________

## Credits

This notebook is part of [The Climate Laboratory](https://brian-rose.github.io/ClimateLaboratoryBook), an open-source textbook developed and maintained by [Brian E. J. Rose](http://www.atmos.albany.edu/facstaff/brose/index.html), University at Albany.

It is licensed for free and open consumption under the
[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/) license.

Development of these notes and the [climlab software](https://github.com/brian-rose/climlab) is partially supported by the National Science Foundation under award AGS-1455071 to Brian Rose. Any opinions, findings, conclusions or recommendations expressed here are mine and do not necessarily reflect the views of the National Science Foundation.
____________

```{code-cell} ipython3

```
