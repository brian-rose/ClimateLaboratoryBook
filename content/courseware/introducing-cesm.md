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

# Introducing the Community Earth System Model (CESM)

This notebook is part of [The Climate Laboratory](https://brian-rose.github.io/ClimateLaboratoryBook) by [Brian E. J. Rose](http://www.atmos.albany.edu/facstaff/brose/index.html), University at Albany.

+++

____________
## About the CESM
____________

+++ {"slideshow": {"slide_type": "slide"}}

### What is it?

- CESM is one of a handful of complex coupled GCMs that are used as part of the IPCC process.
- Developed and maintained at NCAR (Boulder CO) by a group of climate scientists and software engineers.
- “Community” refers to the fact that the code is open-source, with new pieces contributed by a wide variety of users. 

I use CESM in my own research. We are going to be using CESM in this course. For lots more information about CESM:

http://www.cesm.ucar.edu/models/

+++ {"slideshow": {"slide_type": "slide"}}

### Key components of CESM:

see http://www.cesm.ucar.edu/models/cesm1.2/ for more info
 
 - Atmospheric model (AGCM)
     - Community Atmsophere Model (CAM)
 - Ocean model (OGCM)
     - Parallel Ocean Program (POP)
 - Land surface model
     - Community Land Model (CLM)
 - Sea ice model
     - Community Ice CodE (CICE)
     
The software is somewhat modular, so different submodels can be combined together depending on the nature of the scientific problem at hand and the available computer power.

+++ {"slideshow": {"slide_type": "-"}}

Recall that we saw this schematic of different ways to represent the ocean in climate models:

+++ {"slideshow": {"slide_type": "slide"}}

____________
<a id='section6'></a>
## Our numerical experiments with CESM
____________

+++ {"slideshow": {"slide_type": "slide"}}

### Atmosphere

 - Horizontal resolution about 2º lat/lon
 - AGCM solves the fundamental equations:
    - Conservation of momentum, mass, energy, water, equation of state
 - At 2º we resolve the **synoptic-scale dynamics**
     - storm tracks and cyclones. 
 - We do NOT resolve the mesoscale and smaller
     - thunderstorms, individual convective events, clouds
 - These all must be parameterized.
 - Model also solves equations of radiative transfer. This takes account of
     - composition of the atmosphere and the absorption properties of different gases
     - radiative effects of clouds.

+++ {"slideshow": {"slide_type": "slide"}}

### Sea ice

- Resolution of 1º.
- Thermodynamics (conservation of energy, water and salt)
    - determines freezing and melting
- Dynamics (momentum equations) 
    - determine ice motion and deformation.
- Complex! Sea ice is sort of a mixture of a fluid and a solid.

+++ {"slideshow": {"slide_type": "slide"}}

### Land surface model

- Same resolution as atmosphere. 
- Determines surface fluxes of heat, water, momentum (friction) based on prescribed vegetation types.
- Don’t actually know much about how it works!
- Great topic for someone to dig in to for their term project.

+++ {"slideshow": {"slide_type": "slide"}}

### Ocean

- Same grid as sea ice, 1º.
- Exchanges heat, water, and momentum with the atmosphere and sea ice
- Receives runoff from the land surface (rivers)
- Full 3D simulation of the currents.

+++ {"slideshow": {"slide_type": "slide"}}

### Experimental setup

Model is given realistic atmospheric composition, realistic solar radiation, etc.

We perform a **preindustrial control run** to get a baseline simulation, and take **averages of several years** (because the model has internal variability – every year is a little bit different)

We then (later) we will change something, e.g. double the atmospheric $CO_2$!

And allow the model to adjust toward a new equilibrium, just as we did with the toy energy balance model.

+++ {"slideshow": {"slide_type": "slide"}}

## Browsing input data with xarray

First, let's take a look at some of the ingredients that go into the control run. **All of the necessary data will be served up by a special data server sitting in the department**, so you should be able to run this code to interact with the data on any computer that is connected to the internet.

+++ {"slideshow": {"slide_type": "slide"}}

### You need to be connected to the internet to run the code in this notebook ###

You can browse the available data through a web interface here:

http://thredds.atmos.albany.edu:8080/thredds/catalog.html

Within this folder called `CESM archive`, you will find another folder called `som_input` which contains all the input files.

The data are all stored in `NetCDF` files, a standard file format for self-describing gridded data.

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
---
%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
```

We are going to use a package called [xarray](http://xarray.pydata.org) (abbreviated here as `xr`) to work with the datasets.

+++ {"slideshow": {"slide_type": "slide"}}

### Boundary conditions: continents and topography

Here we are going to load the input topography file and take a look at what's inside. 

In this case we are passing it a URL to our online dataserver. We'll put the URL in a string variable called `datapath` to simplify things later on.

```{code-cell} ipython3
cesm_data_path = "http://thredds.atmos.albany.edu:8080/thredds/dodsC/CESMA/"
cesm_input_path = cesm_data_path + "som_input/"
#  Notice that in Python we can easily concatenate strings together just by `adding` them
fullURL = cesm_input_path + "USGS-gtopo30_1.9x2.5_remap_c050602.nc"
print( fullURL)
```

```{code-cell} ipython3
#  Now we actually open the dataset
topo = xr.open_dataset( fullURL )
print(topo)
```

The `Dataset` object has several important attributes. Much of this should look familiar if you have worked with `netCDF` data before. The `xarray` package gives a very powerful and easy to use interface to the data.

+++

We can access individual variables within the `xarray.Dataset` object as follows:

```{code-cell} ipython3
topo.PHIS
```

### Plotting the topography

We will now read the geopotential and make a plot of the topography of the Earth's surface as represented on the 2º grid. The code below makes a colorful plot of the topography. We also use the land-sea mask in order to plot nothing at grid points that are entirely ocean-covered. 

Execute this code exactly as written first, and then play around with it to see how you might customize the graph. 

```{code-cell} ipython3
g = 9.8  # gravity in m/s2
meters_per_kilometer = 1E3 
height = topo.PHIS / g / meters_per_kilometer  # in kilometers
#  Note that we have just created a new xarray.DataArray object that preserves the axis labels
#  Let's go ahead and give it some useful metadata:
height.attrs['units'] = 'km'
height.name = 'height'
height
```

Let's make a plot! `xarray` is able to automatically generate labeled plots. This is very handy for "quick and dirty" investigation of the data:

```{code-cell} ipython3
height.plot()
```

If we want more control over the appearance of the plot, we can use features of `matplotlib`

```{code-cell} ipython3
#  A filled contour plot of topography with contours every 500 m
lev = np.arange(0., 6., 0.5)
fig1, ax1 = plt.subplots(figsize=(8,4))
# Here we are masking the data to exclude points where the land fraction is zero (water only)
cax1 = ax1.contourf( height.lon, height.lat, 
                    height.where(topo.LANDFRAC>0), levels=lev)
ax1.set_title('Topography (km) and land-sea mask in CESM')
ax1.set_xlabel('Longitude')
ax1.set_ylabel('Latitude')
cbar1 = fig1.colorbar(cax1)
```

Note that at 2º resolution we can see many smaller features (e.g. Pacific islands). The model is given a fractional land cover for each grid point. 

Here let's plot the land-sea mask itself so we can see where there is at least "some" water:

```{code-cell} ipython3
fig2, ax2 = plt.subplots()
cax2 = ax2.pcolormesh( topo.lon, topo.lat, topo.LANDFRAC )
ax2.set_title('Ocean mask in CESM')
ax2.set_xlabel('Longitude'); ax2.set_ylabel('Latitude')
cbar2 = fig2.colorbar(cax2);
```

### Making nicer maps

Notice that to make these plots we've just plotted the lat-lon array without using any map projection.

There are nice tools available to make better maps. We'll leave that as a topic for another day. But if you're keen to read ahead, check out:

<http://scitools.org.uk/cartopy/>

+++

## Ocean boundary conditions

Let's load another file that contains some information about the ocean and its interaction with the atmosphere.

```{code-cell} ipython3
som_input = xr.open_dataset( cesm_input_path + "pop_frc.1x1d.090130.nc")
print(som_input)
```

The ocean / sea ice models exist on different grids than the atmosphere (1º instead of 2º resolution).

+++

Now we are going to look at the **annual mean heat flux out of the ocean**.

It is stored in the field `qdp` in the dataset we just opened. 

The sign convention in CESM is that `qdp > 0` where **heat is going IN to the ocean**. We will change the sign to plot heat going OUT of the ocean INTO the atmosphere (a more atmosphere-centric viewpoint). 

```{code-cell} ipython3
som_input.qdp
```

Unfortunately, here is a case in which the metadata are not very useful. There is no text description of what variable `qdp` actually is, or what its units are.  (It is actually in units of W m$^{-2}$)

We can see that there are 12 x 180 x 360 data points. One 180 x 360 grid for each calendar month!

+++

Now we are going to take the average over the year at each point. 

We will use the power of `xarray` here to take the average over the time dimension, leaving us with a single grid on 180 latitude points by 360 longitude points:

```{code-cell} ipython3
(-som_input.qdp.mean(dim='time')).plot()
```

Now make a nice plot of the annual mean q-flux. 

```{code-cell} ipython3
#  We can always set a non-standard size for our figure window
fig3, ax3 = plt.subplots(figsize=(10, 6))
lev = np.arange(-700., 750., 50.)
cax3 = ax3.contourf(som_input.xc, som_input.yc, 
                    -som_input.qdp.mean(dim='time'), 
                    levels=lev, cmap=plt.cm.bwr)
cbar3 = fig3.colorbar(cax3)
ax3.set_title( 'CESM: Prescribed heat flux out of ocean (W m$^{-2}$), annual mean', 
              fontsize=14 )
ax3.set_xlabel('Longitude', fontsize=14)
ax3.set_ylabel('Latitude', fontsize=14)
ax3.text(65, 50, 'Annual', fontsize=16 )
ax3.contour(topo.lon, topo.lat, topo.LANDFRAC, levels=[0.5], colors='k');
```

Notice all the spatial structure here: 

- Lots of heat is going in to the oceans at the equator, particularly in the eastern Pacific Ocean.
- The red hot spots show where lots of heat is coming out of the ocean.
- Hot spots include the mid-latitudes off the eastern coasts of Asia and North America
- And also the northern North Atlantic. 

**All this structure is determined by ocean circulation, which we are not modeling here.** Instead, we are prescribing these heat flux patterns as an input to the atmosphere.

This pattern changes throughout the year. Recall that we just averaged over all months to make this plot. We might want to look at just one month:

```{code-cell} ipython3
# select by month index (0 through 11)
som_input.qdp.isel(time=0)
```

```{code-cell} ipython3
#  select by array slicing (but for this you have to know the axis order!)
som_input.qdp[0,:,:]
```

Here we got just the first month (January) by specifying `[0,:,:]` after the variable name. This is called *slicing* or *indexing* an array. We are saying "give me everything for month number 0". Now make the plot:

```{code-cell} ipython3
fig4, ax4 = plt.subplots(figsize=(10,4)) 
cax4 = ax4.contourf( som_input.xc, som_input.yc, 
                    -som_input.qdp.isel(time=0), 
                      levels=lev, cmap=plt.cm.bwr)
cbar4 = plt.colorbar(cax4)
ax4.set_title( 'CESM: Prescribed heat flux out of ocean (W m$^{-2}$)', 
              fontsize=14 )
ax3.set_xlabel('Longitude', fontsize=14)
ax3.set_ylabel('Latitude', fontsize=14)
ax4.text(65, 50, 'January', fontsize=12 );
ax4.contour(topo.lon, topo.lat, topo.LANDFRAC, levels=[0.5], colors='k');
```

For lots more help with using xarray to slice and dice your dataset, look at the online documentation:

http://xarray.pydata.org

+++

## The "pre-industrial" control run

Our control run is set up to simulate the climate of the "pre-industrial era", meaning before significant human-induced changes to the composition of the atmosphere, nominally the year 1850.

Output from the control run is available on the same data server as above. Look in the folder called `cpl_1850_f19` (Here `cpl` stands for "coupled model" with interactive ocean, 1850 indicated pre-industrial conditions, and `f19` is a code for 2º the horizontal grid resolution).

There are output files for each active model component:

- atmosphere
- ocean
- sea ice
- land surface 

The model produces **monthly average** output files for each component. We can load datasets from individual months, but there are also large **concatenated** files available that contain the entire output.

Let's take a look at the atmosphere file. The file is called

`cpl_1850_f19.cam.h0.nc`

(the file extension `.nc` is used to indicate NetCDF format).

```{code-cell} ipython3
atm_control = xr.open_dataset(cesm_data_path + "cpl_1850_f19/concatenated/cpl_1850_f19.cam.h0.nc")
print(atm_control)
```

Lots of different stuff! These are all the different quantities that are calculated as part of the model simulation. **Every quantity represents a monthly average**. 

Want to get more information about a particular variable?

```{code-cell} ipython3
atm_control.co2vmr
```

This is the amount of CO2 in the atmosphere (about 285 parts per million by volume). It is prescribed in these simulations and does not change.

One nice thing about `xarray.DataArray` objects is that we can do simple arithmetic with them (already seen several examples of this in the notes above). For example, change the units of CO2 amount to ppm:

```{code-cell} ipython3
atm_control.co2vmr * 1E6
```

Here's another variable:

```{code-cell} ipython3
atm_control.SOLIN
```

Apparently this is the incoming solar radiation or **insolation**, with shape (240,96,144) meaning it's got 240 months, 96 latitude points and 144 longitude points. 

+++

___________________________
## Exercise: Taking a time average
____________________________

+++

- Take the **time average** of the `SOLIN` field. Store the result as a new variable.
- What are the **dimensions** of the resulting data array? What would be a good way to visualize this quantity?

```{code-cell} ipython3
atm_control.SOLIN.mean(dim='time')
```

___________________________
## Exercise: Plotting the time average insolation
____________________________

+++

1. Make a well-labeled plot of the time-averaged insolation (using the variable you stored above).
2. Is there a way to **further reduce the dimensionality** of the data, and plot the information in a different way?

Remember that you can apply the `.mean()` operation across any number of named dimensions in a data array.

```{code-cell} ipython3

```

## Comparing the control run with the observed energy budget

Recall that our investigations so far have been guided by this figure of the observed **annual, global mean energy budget**:

+++

![Observed global energy budget](http://www.atmos.albany.edu/facstaff/brose/classes/ENV415_Spring2018/images/GlobalEnergyBudget.png)

+++

___________________________
## Exercise: Thinking about how to compute a global average
____________________________

In order to compare these numbers with the control run, **we need to take global averages** of the data. What do we mean by **global average**?

Before proceeding with these notes, try to answer the following question:

**Why does it not make sense to simply average over each data point on a latitude-longitude grid?**

+++



+++

## Weighting for global average

The global average needs to weighted by the area of each grid cell, which is proportional to the **cosine of latitude** (do you understand why?)

We can implement this in xarray as follows:

```{code-cell} ipython3
#  Take the cosine of latitude (first converting to radians)
coslat = np.cos(np.deg2rad(atm_control.lat))
print(coslat)
```

```{code-cell} ipython3
#  And divide by its mean value
weight_factor = coslat / coslat.mean(dim='lat') 
#  Want to see what we just created?
print(weight_factor)
```

```{code-cell} ipython3

```

### An alternative: use weights already provided in the dataset

You will find that many gridded datasets already provide a field that gives accurate area weighting.

In the case of the CESM output, the field is called `gw`

```{code-cell} ipython3
weight_factor2 = atm_control.gw / atm_control.gw.mean(dim='lat')
```

```{code-cell} ipython3
weight_factor2
```

### Compute the global, time average insolation

```{code-cell} ipython3
#  Compute the global, time average insolation using our two different weight factors
#  Notice that we can apply the .mean() operation simultaneously over several dimensions!
print( (atm_control.SOLIN * weight_factor).mean(dim=('time', 'lon', 'lat')))
print( (atm_control.SOLIN * weight_factor2).mean(dim=('time', 'lon', 'lat')))
```

These numbers should both be very close to 340.3

This value is the global average insolation in units of W m$^{-2}$.

+++

___________________________
## Exercise: plotting a global average timeseries

Plot a **timeseries** of the **global average surface temperature** in the control simulation.

Surface temperature is called `'TS'` in the dataset.

Make a plot of the global average `TS` with time on the x axis. *Make sure your global average is properly weighted as discussed above.*
____________________________

```{code-cell} ipython3
TSglobal = (atm_control.TS * weight_factor).mean(dim=('lon','lat'))
TSglobal
```

```{code-cell} ipython3
TSglobal.plot()
```

### Discussion point

What do you see in this graph? Do you have any ideas about why the global average temperature looks like this?

Also, what is the **time average** global-average surface temperature in this simulation?

```{code-cell} ipython3
TSglobal.mean(dim='time')
```

### Finding the radiative fluxes in the model output

Now that you can take global averages and time averages, we can compare some energy budget values against observations.

The model output contains lots of diagnostics about the radiative fluxes. Here are some CESM naming conventions to help you find the appropriate output fields:

- All variables whose names being with `'F'` are an **energy flux** of some kind. 
- Most have a four-letter code, e.g. `'FLNT'`
- `'FL'` means **longwave flux** (i.e. terrestrial)
- `'FS'` means **shortwave flux** (i.e. solar)
- The third letter indicates **direction** of the flux:
    - `'U'` = up
    - `'D'` = down
    - `'N'` = net
- The fourth letter indicates the **location** of the flux:
    - `'T'` = top of atmosphere
    - `'S'` = surface
- So `'FLNT'` means 'net longwave flux at the top of atmosphere', i.e. the outgoing longwave radiation or OLR.

You wil see that these are all 240 x 96 x 144 -- i.e. a two-dimensional grid for every month in the simulation.

```{code-cell} ipython3
atm_control.FLNT
```

__________________________
## Exercise: compute terms in the planetary energy budget

Compute annual, global averages of the following four quantities. 

1. Incoming solar radiation (or insolation)
2. Absorbed solar radiation (ASR)
3. Planetary albedo *(remember this is a **ratio** of outgoing to incoming solar radiation)*
4. Outgoing longwave radiation (OLR)

Compare your results briefly to the observations.
____________________________

```{code-cell} ipython3

```

## A few more tidbits

Feel free to keep exploring the data!

Many other fields are four-dimensional (time, level, latitude, longitude). 

For example, here the **air temperature** at every point and every month:

```{code-cell} ipython3
atm_control.T
```

Often we want to sample the data **at a particular place and time**. xarray gives us simple ways to do that.

For example, we can **interpolate** to a particular location in latitude and longitude (here it's the coordinates of Albany NY):

```{code-cell} ipython3
Tlocal = atm_control.T.interp(lat=42.75, lon=(360-73.8))
print(Tlocal)
```

We can also use **time indexing** to pick out a particular year and month:

```{code-cell} ipython3
#  The .sel notation mean "select" along the given coordinate
#  The string that follows is year-month. Our simulation begins in year 0001.
Tlocal.sel(time='0020-01')  # a particular January
```

Now, for example, we can plot the temperature as a function of pressure at this place and time:

```{code-cell} ipython3
Tlocal.sel(time='0020-01').plot()
```

____________

## Credits

This notebook is part of [The Climate Laboratory](https://brian-rose.github.io/ClimateLaboratoryBook), an open-source textbook developed and maintained by [Brian E. J. Rose](http://www.atmos.albany.edu/facstaff/brose/index.html), University at Albany.

It is licensed for free and open consumption under the
[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/) license.

Development of these notes and the [climlab software](https://github.com/brian-rose/climlab) is partially supported by the National Science Foundation under award AGS-1455071 to Brian Rose. Any opinions, findings, conclusions or recommendations expressed here are mine and do not necessarily reflect the views of the National Science Foundation.
____________

```{code-cell} ipython3

```
