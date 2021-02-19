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
(nb:transCESM)=
# Examing the transient and equilibrium CO$_2$ response in the CESM

This notebook is part of [The Climate Laboratory](https://brian-rose.github.io/ClimateLaboratoryBook) by [Brian E. J. Rose](http://www.atmos.albany.edu/facstaff/brose/index.html), University at Albany.

+++

I have run two sets of experiments with the CESM model:

- The fully coupled model:
    - pre-industrial control
    - 1%/year CO2 ramp scenario for 80 years 
- The slab ocean model:
    - pre-industrial control with prescribed q-flux
    - 2xCO2 scenario run out to equilibrium

+++

Our main first task is to compute the two canonical measures of climate sensitivity for this model:

- Equilibrium Climate Sensitivity (ECS)
- Transient Climate Response (TCR)

+++

From the IPCC AR5 WG1 report, Chapter 9, page 817:

> Equilibrium climate sensitivity (ECS) is the equilibrium change in global and annual mean surface air temperature after doubling the atmos- pheric concentration of CO2 relative to pre-industrial levels. 

> The transient climate response (TCR) is the change in global and annual mean surface temperature from an experiment in which the CO2 concentration is increased by 1% yr$^{–1}$, and calculated using the difference between the start of the experiment and a 20-year period centred on the time of CO2 doubling. 

+++

### First, a quick demonstration that 1%/year compounded increase reaches doubling after 70 years

```{code-cell} ipython3
startingamount = 1.
amount = startingamount
for n in range(70):
    amount *= 1.01
amount
```

TCR is always smaller than ECS due to the transient effects of ocean heat uptake.

We are going to **estimate** the ECS of the fully coupled model by using the equilibrium response of the Slab Ocean .

```{code-cell} ipython3
%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
```

## Load the concatenated output from the CAM output (atmosphere)

```{code-cell} ipython3
casenames = {'cpl_control': 'cpl_1850_f19',
             'cpl_CO2ramp': 'cpl_CO2ramp_f19',
             'som_control': 'som_1850_f19',
             'som_2xCO2':   'som_1850_2xCO2',
            }
# The path to the THREDDS server, should work from anywhere
basepath = 'http://thredds.atmos.albany.edu:8080/thredds/dodsC/CESMA/'
# For better performance if you can access the roselab_rit filesystem (e.g. from JupyterHub)
#basepath = '/roselab_rit/cesm_archive/'
casepaths = {}
for name in casenames:
    casepaths[name] = basepath + casenames[name] + '/concatenated/'
```

```{code-cell} ipython3
# make a dictionary of all the CAM atmosphere output
atm = {}
for name in casenames:
    path = casepaths[name] + casenames[name] + '.cam.h0.nc'
    print('Attempting to open the dataset ', path)
    atm[name] = xr.open_dataset(path, decode_times=False)
```

###  A plot of the prescribed CO2 concentrations in the coupled simulations

```{code-cell} ipython3
days_per_year = 365
fig, ax = plt.subplots()
for name in ['cpl_control', 'cpl_CO2ramp']:
    ax.plot(atm[name].time/days_per_year, atm[name].co2vmr*1E6, label=name)
ax.set_title('CO2 volume mixing ratio (CESM coupled simulations)')
ax.set_xlabel('Years')
ax.set_ylabel('pCO2 (ppm)')
ax.grid()
ax.legend();
```

Issues to think about:

- Why do we talk about fractional changes in CO2, such as "doubling atmospheric CO2", and "1%/year compounded CO2 increase?
- Why not instead talk about changes in absolute amounts of CO2?

The answer is closely related to the fact that the **radiative forcing** associated with CO2 increase is approximately **logarithmic** in CO2 amount. So a doubling of CO2 represents roughly the same radiative forcing *regardless of the initial CO2 concentration*.

+++

## Compute and plot time series of global, annual mean near-surface air temperature in all four simulations

```{code-cell} ipython3
# The surface air temperature, which we will use for our sensitivity metrics
atm['cpl_control'].TREFHT
```

```{code-cell} ipython3
#  The area weighting needed for global averaging
gw = atm['som_control'].gw
print(gw)
```

```{code-cell} ipython3
def global_mean(field, weight=gw):
    '''Return the area-weighted global average of the input field'''
    return (field*weight).mean(dim=('lat','lon'))/weight.mean(dim='lat')
```

```{code-cell} ipython3
#  Loop through the four simulations and produce the global mean timeseries
TREFHT_global = {}
for name in casenames:
    TREFHT_global[name] = global_mean(atm[name].TREFHT)
```

#### Make some pretty timeseries plots, including an **approximate** running annual average

```{code-cell} ipython3
fig, axes = plt.subplots(2,1,figsize=(10,8))
for name in casenames:
    if 'cpl' in name:
        ax = axes[0]
        ax.set_title('Fully coupled ocean')
    else:
        ax = axes[1]
        ax.set_title('Slab ocean')
    field = TREFHT_global[name]
    field_running = field.rolling(time=12, center=True).mean()
    line = ax.plot(field.time / days_per_year, 
                   field, 
                   label=name,
                   linewidth=0.75,
                   )
    ax.plot(field_running.time / days_per_year, 
            field_running, 
            color=line[0].get_color(),
            linewidth=2,
           )
for ax in axes:
    ax.legend();
    ax.set_xlabel('Years')
    ax.set_ylabel('Temperature (K)')
    ax.grid();
    ax.set_xlim(0,100)
fig.suptitle('Global mean surface air temperature in CESM simulations', fontsize=16);
```

Issues to think about here include:

- Why is the annual average here only approximate? *(think about the calendar)*
- Why is there an annual cycle in the global average temperature? (planet is coldest during NH winter)
- Different character of the temperature **variability** in the coupled vs. slab model
- Much more rapid warming in the Slab Ocean Model

+++

## Now we can work on computing ECS and TCR

```{code-cell} ipython3
# extract the last 10 years from the slab ocean control simulation
# and the last 20 years from the coupled control
nyears_slab = 10
nyears_cpl = 20
clim_slice_slab = slice(-(nyears_slab*12),None)
clim_slice_cpl = slice(-(nyears_cpl*12),None)
```

```{code-cell} ipython3
# extract the last 10 years from the slab ocean control simulation
T0_slab = TREFHT_global['som_control'].isel(time=clim_slice_slab).mean(dim='time')
T0_slab
```

```{code-cell} ipython3
# and the last 20 years from the coupled control
T0_cpl = TREFHT_global['cpl_control'].isel(time=clim_slice_cpl).mean(dim='time')
T0_cpl
```

```{code-cell} ipython3
# extract the last 10 years from the slab 2xCO2 simulation
T2x_slab = TREFHT_global['som_2xCO2'].isel(time=clim_slice_slab).mean(dim='time')
T2x_slab
```

```{code-cell} ipython3
# extract the last 20 years from the coupled CO2 ramp simulation
T2x_cpl = TREFHT_global['cpl_CO2ramp'].isel(time=clim_slice_cpl).mean(dim='time')
T2x_cpl
```

```{code-cell} ipython3
ECS = T2x_slab - T0_slab
TCR = T2x_cpl - T0_cpl
print('The Equilibrium Climate Sensitivity is {:.3} K.'.format(float(ECS)))
print('The Transient Climate Response is {:.3} K.'.format(float(TCR)))
```

## Some CMIP climate sensitivity results to compare against

+++

<img src='http://www.climatechange2013.org/images/figures/WGI_AR5_Fig9-43.jpg' width=800>

+++

<img src='../images/AR5_Table9.5.png'>

+++

Comparing against the multi-model mean of the ECS and TCR, our model is apparently slightly less sensitive than the CMIP5 mean.

+++

## Let's make some maps to compare spatial patterns of transient vs. equilibrium warming

+++

Here is a helper function that takes a 2D lat/lon field and renders it as a nice contour map with accompanying zonal average line plot.

```{code-cell} ipython3
# The map projection capabilities come from the cartopy package. There are many possible projections
import cartopy.crs as ccrs
```

```{code-cell} ipython3
def make_map(field):
    '''input field should be a 2D xarray.DataArray on a lat/lon grid.
        Make a filled contour plot of the field, and a line plot of the zonal mean
    '''
    fig = plt.figure(figsize=(14,6))
    nrows = 10; ncols = 3
    mapax = plt.subplot2grid((nrows,ncols), (0,0), colspan=ncols-1, rowspan=nrows-1, projection=ccrs.Robinson())
    barax = plt.subplot2grid((nrows,ncols), (nrows-1,0), colspan=ncols-1)
    plotax = plt.subplot2grid((nrows,ncols), (0,ncols-1), rowspan=nrows-1)
    cx = mapax.contourf(field.lon, field.lat, field, transform=ccrs.PlateCarree())
    mapax.set_global(); mapax.coastlines();
    plt.colorbar(cx, cax=barax, orientation='horizontal')
    plotax.plot(field.mean(dim='lon'), field.lat)
    plotax.set_ylabel('Latitude')
    plotax.grid()
    return fig, (mapax, plotax, barax), cx
```

```{code-cell} ipython3
# Plot a single time slice of surface air temperature just as example
fig, axes, cx = make_map(atm['cpl_control'].TREFHT.isel(time=0))
```

### Make maps of the surface air temperature anomaly due to CO2 doubling in both the slab and coupled models

```{code-cell} ipython3
Tmap_cpl_2x = atm['cpl_CO2ramp'].TREFHT.isel(time=clim_slice_cpl).mean(dim='time')
Tmap_cpl_control = atm['cpl_control'].TREFHT.isel(time=clim_slice_cpl).mean(dim='time')
DeltaT_cpl = Tmap_cpl_2x - Tmap_cpl_control

Tmap_som_2x = atm['som_2xCO2'].TREFHT.isel(time=clim_slice_slab).mean(dim='time')
Tmap_som_control = atm['som_control'].TREFHT.isel(time=clim_slice_slab).mean(dim='time')
DeltaT_som = Tmap_som_2x - Tmap_som_control
```

```{code-cell} ipython3
fig, axes, cx = make_map(DeltaT_cpl)
fig.suptitle('Surface air temperature anomaly (coupled transient)', fontsize=16);
axes[1].set_xlim(0,7)  # ensure the line plots have same axes
cx.set_clim([0, 8])    # ensure the contour maps have the same color intervals

fig, axes,cx  = make_map(DeltaT_som)
fig.suptitle('Surface air temperature anomaly (equilibrium SOM)', fontsize=16);
axes[1].set_xlim(0,7)
cx.set_clim([0, 8])
```

Lots of intersting phenomena to think about here, including:

- Polar amplification of surface warming
- Reduction in equator-to-pole temperature gradients
- Much larger polar amplification in SOM than in transient -- especially over the Southern Ocean (the *delayed warming of the Southern Ocean*)
- North Atlantic *warming hole* present in transient but not in equilibrium SOM.
- Land-ocean warming contrast: larger in transient, but still present in equilibrium

+++

## Appendix: for later reference, here is how you can open the other output types

The following will open the rest of the CESM output (land, sea ice, river routing, ocean).

These are not needed for the above homework assignment, but may be useful later on.

```{code-cell} ipython3
# # make a dictionary of all the CLM land model output
# land = {}
# for name in casenames:
#     path = casepaths[name] + casenames[name] + '.clm2.h0.nc'
#     print('Attempting to open the dataset ', path)
#     land[name] = xr.open_dataset(path)
```

```{code-cell} ipython3
# # make a dictionary of all the sea ice model output
# ice = {}
# for name in casenames:
#     path = casepaths[name] + casenames[name] + '.cice.h.nc'
#     print('Attempting to open the dataset ', path)
#     ice[name] = xr.open_dataset(path)
```

```{code-cell} ipython3
# # make a dictionary of all the river transport output
# rtm = {}
# for name in casenames:
#     path = casepaths[name] + casenames[name] + '.rtm.h0.nc'
#     print('Attempting to open the dataset ', path)
#     rtm[name] = xr.open_dataset(path)
```

```{code-cell} ipython3
# ocn = {}
# for name in casenames:
#     if 'cpl' in name:
#         path = casepaths[name] + casenames[name] + '.pop.h.nc'
#         print('Attempting to open the dataset ', path)
#         ocn[name] = xr.open_dataset(path)
```

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
