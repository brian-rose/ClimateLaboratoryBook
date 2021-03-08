---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.12
    jupytext_version: 1.9.1
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

+++ {"slideshow": {"slide_type": "slide"}}

(nb:coupdyn)=
# Coupled Dynamics in the CESM

This notebook is an extension of [The Climate Laboratory](https://brian-rose.github.io/ClimateLaboratoryBook) by [Brian E. J. Rose](http://www.atmos.albany.edu/facstaff/brose/index.html), University at Albany. Notebook by Rachel H. White, University of British Columbia (https://www.eoas.ubc.ca/people/rachelwhite)

There are 'Discussion points' and 'Exercises' throughout these notebooks. You should come to class prepared to discuss your thoughts on the Discussion points.

Learning goals:
- Be able to analyse coupled (atmosphere-ocean) dynamics in the CESM climate model data
- Understand how the coupled system produces low-frequency climate variability, and consider the implications of this for understanding climate change
- Evaluate differences in low-frequency climate variability between slab-ocean and fully coupled simulations
     
**You need to be connected to the internet to run the code in this notebook**

You can browse the available data through a web interface here:

http://thredds.atmos.albany.edu:8080/thredds/catalog.html

Within this folder called `CESM archive`, you will find another folder called `som_input` which contains all the input files.

________
## Low frequency variability in the CESM
________

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import xarray as xr
import scipy as sp
from scipy import stats
import Ngl
import cartopy
import cartopy.util
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from eofs.standard import Eof

%matplotlib inline
```

```{code-cell} ipython3
cesm_data_path = "http://thredds.atmos.albany.edu:8080/thredds/dodsC/CESMA/"
```

```{code-cell} ipython3
# Read in slab ocean data
atmfile = xr.open_dataset( cesm_data_path + 'som_1850_f19/concatenated/' + 'som_1850_f19.cam.h0.nc')
#atmfile = xr.open_dataset( cesm_data_path + "cpl_1850_f19/concatenated/cpl_1850_f19.cam.h0.nc")
atmfile
```

This data is a concatenated dataset of monthly data - we expect that it's monthly data because of the file name - with the CESM model the 'h0' in the file name is short for 'history file 0'. The default is for 'history file 0' to be monthly data. You can change the CESM model to output additional history files (h1, h2, h3...) at a different time resolution. The default for 'h1' is daily data. If you are interested in looking at storm tracks, and their influence on heat transport and surface weather, you might have h1 be outputting daily data for just a few variables of interest to eddy dynamics (winds, geopotential height), and h2 to be outputting 6-hourly data for a few 2D fields such as precipitation, surface temperature and surface pressure (outputting 6-hourly data on 3D fields will take up a lot of space very quickly).

We can confirm that it is monthly data by looking at the times in the file above. Compare this to the h1 files that are also available from this thredds directory:

```{code-cell} ipython3
atmfileh1_0001 = xr.open_dataset(cesm_data_path + 'som_1850_f19/atm/hist/' + 
                                 'som_1850_f19.cam.h1.0001-01-01-00000.nc')
#atmfile = xr.open_dataset( cesm_data_path + "cpl_1850_f19/concatenated/cpl_1850_f19.cam.h0.nc")
atmfileh1_0001
```

**Discussion:** _What is the time resolution of the h1 files?_

As discussed in Hartmann chapter 8, single point correlation maps are one way of looking at the variability - these show how values of a variables at places all around the globe vary together with that variable at a particular point; that is, they show spatial patterns of variability. Let's try to reproduce figure 8.4b.

```{code-cell} ipython3
# First calculate new arrays that hold seasonal data
Z3_seas = {}
for label,data in atmfile.Z3.groupby('time.season'):
    Z3_seas[label] = data
    
PS_seas = {}
for label,data in atmfile.PS.groupby('time.season'):
    PS_seas[label] = data
    
```

```{code-cell} ipython3
# First we want to convert to pressure levels 
def hybrid2pres(filein,varin,PSin,plevels,timedim=True):
    # the parameters hyam and hybm are parameters used to calculate the pressure from the level value
    hyam = filein['hyam']
    hybm = filein['hybm']
    p0mb = filein['P0']/100.0
    
    varpres = Ngl.vinth2p(varin, hyam, hybm, plevels, PSin, 1, p0mb, 1, False)
    # This has set values below the surface to 1E30. We want these to be nan:
    varpres = np.where(varpres>=1E30,np.nan,varpres)

    # Create xarray from this numpy ndarray:
    if timedim:
        varpres_xr = xr.DataArray(varpres,
                              dims=['time','plev','lat','lon'],
                              coords={'time':varin.time,'plev':plevels,
                                      'lat':varin.lat,'lon':varin.lon})
    else:
        varpres_xr = xr.DataArray(varpres,
                              dims=['plev','lat','lon'],
                              coords={'plev':plevels,
                                      'lat':varin.lat,'lon':varin.lon})
        
    return(varpres_xr)

# we're interested in the 500mb level, so we can just select that level 
# For DJF:
Z500_DJF = hybrid2pres(atmfile,Z3_seas['DJF'],PS_seas['DJF'],[500])
```

```{code-cell} ipython3
# Select the point that we want to calculate correlations from: (fig. 8.4c)
# Estimate that P is at: 45N, 200E (
# Warning - when using new datasets you should always check whether the
# longitudes are 0-360, not -180 to 180)

# Because the latitudes are not spaced such that there is a grid box centred on 45N, if
# we use .sel(lat=45) it will fail:

# pointvals = Z500_DJF.sel(lat=45).sel(lon=200)

# We can either look at the data and select a latitude value that does exist,
# or ask xarray to just pick the nearest point to the value we have asked for:
pointvals = Z500_DJF.sel(lat=45,method='nearest').sel(lon=200)
```

```{code-cell} ipython3
# Now correlate this timeseries with that from a nearby gridpoint:
tocorr = Z500_DJF.sel(lat=45,method='nearest').sel(lon=210)
#print(pointvals.squeeze())
corr,r = sp.stats.pearsonr(pointvals.squeeze(),tocorr.squeeze())

print(corr,r)

# We can see there is a very strong correlation, that has a very low p-value (r; note
# this assumes your data are normally distrubuted which may not be the case!)
```

```{code-cell} ipython3
# To build the 1-point correlation maps we can repeat this for every point
nlats = len(Z500_DJF.lat)
nlons = len(Z500_DJF.lon)

corrarray = np.zeros([nlats,nlons],float)
rarray = np.zeros([nlats,nlons],float)

for ilat in range(0,nlats):
    for ilon in range(0,nlons):
        # if we use isel instead of sel, we select on indices, instead of values:
        tocorr = Z500_DJF.isel(lat=ilat).isel(lon=ilon)
        corrarray[ilat,ilon],rarray[ilat,ilon] = sp.stats.pearsonr(pointvals.squeeze(),tocorr.squeeze())
```

```{code-cell} ipython3
# We can now plot this 1-point correlation array for comparison with fig. 8.4c in Hartmann
toplot = corrarray
ncols=1
nrows=1
n=1

title='DJF 1-point correlation map Z500 monthly data'

proj=ccrs.Orthographic(central_latitude=90)
ax = plt.subplot(ncols,nrows,n,projection=proj)
ax.coastlines()
gl = ax.gridlines(crs=ccrs.PlateCarree())

cp = plt.contourf(Z500_DJF.lon,Z500_DJF.lat,toplot,levels=np.arange(-1,1.01,0.2),extend='both',
                  transform=ccrs.PlateCarree(),cmap='RdBu_r')

# Add colorbar
cb = plt.colorbar(cp)
plt.title(title)
plt.show()
```

It is often useful to mask your data for statistical significance, and this can be done fairly easily with python:

```{code-cell} ipython3
# We can now plot this 1-point correlation array for comparison with fig. 8.4c in Hartmann

# Set the p-value for which we want to show the data:
p=0.05

toplot = corrarray
mask = np.where(rarray<p,1.0,0.0)

ncols=1
nrows=1
n=1

title='DJF 1-point correlation map Z500 monthly data'

proj=ccrs.Orthographic(central_latitude=90)
ax = plt.subplot(nrows,ncols,n,projection=proj)
ax.coastlines()
gl = ax.gridlines(crs=ccrs.PlateCarree())

cp = plt.contourf(Z500_DJF.lon,Z500_DJF.lat,toplot,levels=np.arange(-1,1.01,0.2),extend='both',
                  transform=ccrs.PlateCarree(),cmap='RdBu_r')
cb = plt.colorbar(cp)

# Choose to hatch where the data is NOT statistically significant at our chosen level
cp = plt.contourf(Z500_DJF.lon,Z500_DJF.lat,mask,levels=[0,0.99],hatches=['/',None],
                  transform=ccrs.PlateCarree(),colors='none')

plt.title(title + '; p<' + str(p))
plt.show()
```

**Exercise:** _Repeat this analysis for a 1-point correlation for point A on Figure 8.4d. Add the letters A and P onto
these figures in the correct places to illustrate the point used for the correlations._
##Discussion:** _Why are we only looking at figure 8.4c and 8.4d. What are the additional steps required to reproduce
figures 8.4a and b?

## Slab ocean and coupled ocean low frequency variability

```{code-cell} ipython3
# Read in fully coupled ocean data
atmfile_cpl = xr.open_dataset( cesm_data_path + 'cpl_1850_f19/concatenated/' + 'cpl_1850_f19.cam.h0.nc')
#atmfile = xr.open_dataset( cesm_data_path + "cpl_1850_f19/concatenated/cpl_1850_f19.cam.h0.nc")
atmfile_cpl
```

**Exercise:** _Calculate the single point correlation maps for the coupled data, and compare to the slab ocean plots._
**Discussion:** _Are these plots significantly different? Is this what you would expect? Why/why not?_

## The El Nino Southern Oscillation

If you are not familiar with the El Nino Southern Oscillation (ENSO) I suggest you read through section 8.3 of the Hartmann book before attempting this section.

First, let's check that the model correctly simulates the average zonally asymmetric circulation patterns in the tropics (for comparison with figure 8.9). 

OMEGA is the variable containing the vertical (pressure) velocity, in Pa/s

```{code-cell} ipython3
# Because there isn't a grid box centred on 0, we take an average across the equator. We first check that
# this is symmetrical about the equator:
print(atmfile.sel(lat=slice(-2,2)).lat)

omega = atmfile.OMEGA.sel(lat=slice(-2,2)).mean(dim='time')
PS = atmfile.PS.sel(lat=slice(-2,2)).mean(dim='time')
omega_cpl = atmfile_cpl.OMEGA.sel(lat=slice(-2,2)).mean(dim='time')
PS_cpl = atmfile_cpl.PS.sel(lat=slice(-2,2)).mean(dim='time')

# convert to pressure levels
pnew = [1000.,850.,700.,600.,500.,400.,300.,250.,200.,150.,100.,70.,50.,30.,20.,10.,5.]

omega_pres = hybrid2pres(atmfile,omega,PS,pnew,timedim=False).mean(dim='lat')
omega_cpl_pres = hybrid2pres(atmfile_cpl,omega_cpl,PS_cpl,pnew,timedim=False).mean(dim='lat')
```

```{code-cell} ipython3
# Plot the equatorial cross-section
omega_pres.plot.contour(levels = np.arange(0,0.1,0.02),colors='r')
omega_pres.plot.contour(levels = np.arange(-0.1,0,0.02),colors='b',linestyles='-')
plt.yscale('log')
# invert the axis so it represents height, but shows pressure
plt.gca().invert_yaxis()
# set the top and bottom pressure of the plot
plt.ylim(1000,100)
plt.title('Slab ocean equatorial vertical pressure velocity, annual mean')
plt.show()

omega_cpl_pres.plot.contour(levels = np.arange(0,0.1,0.02),colors='r')
omega_cpl_pres.plot.contour(levels = np.arange(-0.1,0,0.02),colors='b',linestyles='-')
plt.yscale('log')
# invert the axis so it represents height, but shows pressure
plt.gca().invert_yaxis()
# set the top and bottom pressure of the plot
plt.ylim(1000,100)
plt.title('Coupled ocean equatorial vertical pressure velocity, annual mean')
plt.show()
```

**Discussion:** _Compare the model results to the observations shown in the Hartmann textbook and to each other._

Now let's calculate indices of the ENSO.

```{code-cell} ipython3
# We can calculate the Nino3 index in these models and compare the variability.
# Convert from K to C on the way
Nino3 = atmfile.TS.sel(lat=slice(-5,5),lon=slice(210,270)).mean(dim=['lat','lon']) - 273.15
Nino3_cpl = atmfile_cpl.TS.sel(lat=slice(-5,5),lon=slice(210,270)).mean(dim=['lat','lon']) - 273.15
```

```{code-cell} ipython3
# Calculate climatologies and compare
def create_clim(indata):
    nyears = int(len(indata.time)/12)
    # reshape data
    indata_years = np.reshape(indata.values,(nyears,12))
    clim = indata_years.mean(axis=0)
    return(clim)

Nino3_clim = create_clim(Nino3)
Nino3_cpl_clim = create_clim(Nino3_cpl)
```

```{code-cell} ipython3
# Plot to compare the Nino3 climatologies of the two models.
plt.plot(np.arange(1,13),Nino3_clim,label='slab ocean',color='k')
plt.plot(np.arange(1,13),Nino3_cpl_clim,label='coupled ocean',color='b')
plt.legend()
plt.xlabel('month of year')
plt.ylabel('Temperature (C)')
plt.title('Nino3 climatology')
plt.show()
```

We can see that both models follow a similar climatology in the Nino3 index, which is largely driven by the seasonal cycle. It makes sense that both oceans reproduce the seasonal cycle in surface temperature as this is, at least in tropics, strongly forced by incoming solar radiation. Note that this seasonal cycle shows two peaks (Dec/Jan and May) and two troughs (Feb and Sep) per year.


**Discussion:** _Why does the climatology of tropical SSTs show two peaks per year? Is that what you would expect to see in observations, or do you think there is something wrong with this model?_

```{code-cell} ipython3
# Now calculate the anomalies from this climatology:
# need to repeat the climatology for each year in order to subtract arrays
nyears = 30
nyears_cpl=20
Nino3_clim_all = np.tile(Nino3_clim,nyears)
Nino3_anoms = Nino3 - Nino3_clim_all

Nino3_cpl_clim_all = np.tile(Nino3_cpl_clim,nyears_cpl)
Nino3_cpl_anoms = Nino3_cpl - Nino3_cpl_clim_all
```

**Exercise:** _Create a plot to compare the anomalies in the slab ocean and fully coupled ocean experiments. Note that the coupled ocean has only 20 years, while the slab ocean has 30._


**Discussion:** _Which model has more variability? Is this what you would expect? Which model has more low frequency variability? What does this tell you about variability of ocean surface tempertures in the Nino3 region?_


Rather than estimating the variability, we can calculate the power specturm using fast fourier transforms.

```{code-cell} ipython3
# Plot a simple (non-normalized) power density spectrum using Fourier analysis
Nino3_fft = np.fft.rfft(Nino3_anoms)

Nino3_powerspec = np.square(np.abs(Nino3_fft))
sampling_rate = 12 # cycles per year
frequency = np.linspace(0, sampling_rate/2, len(Nino3_powerspec))

plt.plot(frequency,Nino3_powerspec,color='k',label='slab ocean')

# Repeat for coupled experiment
Nino3_cpl_fft = np.fft.rfft(Nino3_cpl_anoms)

Nino3_cpl_powerspec = np.square(np.abs(Nino3_cpl_fft))
sampling_rate = 12 # cycles per year
frequency = np.linspace(0, sampling_rate/2, len(Nino3_cpl_powerspec))

plt.plot(frequency,Nino3_cpl_powerspec,color='b',label='coupled ocean')

plt.ylim(0,20000)
plt.xlim(0,2)
plt.legend()
plt.show()
```

**Discussion:** _Do the two models simulate any realistic ENSO variance? What are the differences between the 2 spectra shown above and between that shown in Fig. 8.12 in the Hartmann book for the observations? Think about why these differences might come about, and what they tell us about the models?_

If we want a more detailed spectra for the coupled ocean we need more than 20 years. You can find a simulation of 80 years with CO2 ramping here:

```{code-cell} ipython3
atmfile_cpl_ramp = xr.open_dataset( cesm_data_path + 
                    'cpl_CO2ramp_f19/concatenated/' + 'cpl_CO2ramp_f19.cam.h0.nc')
```

This starts off at year 20 of the cpl_1850_f19 simulation, and ramps up CO2, similar to the real World, which gives us a test of climate change as well. This means we also need to remove a linear trend from the TS data before calculating the power spectrum.

```{code-cell} ipython3
Nino3_cpl_ramp = (atmfile_cpl_ramp.TS
                      .sel(lat=slice(-5,5),lon=slice(210,270))
                      .mean(dim=['lat','lon']) - 273.15)
Nino3_cpl_ramp_clim = create_clim(Nino3_cpl_ramp)

nyears_cpl_ramp=80
Nino3_cpl_anoms = Nino3_cpl_ramp - np.tile(Nino3_cpl_ramp_clim,nyears_cpl_ramp)

# Calculate the linear slope using regression:
x = np.arange(0,80,1/12)
regress = sp.stats.linregress(x,Nino3_cpl_anoms)
```

```{code-cell} ipython3
# Plot anomalies and linear regression
plt.plot(x,Nino3_cpl_anoms)
plt.plot(x,regress.slope*x + regress.intercept,color='k')
plt.show()

# Now remove this linear slope
Nino3_cpl_anoms_detrend = Nino3_cpl_anoms - regress.slope*x + regress.intercept
plt.plot(x,Nino3_cpl_anoms_detrend)
plt.show()
```

**Exercise:** _Calculate and plot the power spectrum for these de-trended data for comparison with the 20 year dataset and the observations in the Hartmann book._

```{code-cell} ipython3
# Plot a simple (non-normalized) power density spectrum using Fourier analysis
```

## ENSO and the PDO

+++

We can now look at the spatial signal of the ENSO using Empirical Orthogonal Functions (EOFs), a form of Principal Component Analysis. This webpage: https://climatedataguide.ucar.edu/climate-data-tools-and-analysis/empirical-orthogonal-function-eof-analysis-and-rotated-eof-analysis provides a brief overview of EOFs for those not familiar with them. For those who are familiar with them, there is a key sentence here:
**EOF analysis is _not_ based on physical principles**. This means that just because you find an EOF pattern in your data does NOT mean there is necessarily a physical process that pattern represents. EOFs are a useful tool, but need to be combined with physical understanding.
For a more in-depth review, see: https://rmets.onlinelibrary.wiley.com/doi/epdf/10.1002/joc.1499

```{code-cell} ipython3
indata=atmfile_cpl_ramp.TS - 273.15

# Mask over land values
landmask = np.where(atmfile_cpl_ramp.LANDFRAC>0,np.nan,1)

SST = indata * landmask

nlons = len(SST.lon)
nlats = len(SST.lat)
nyears_cpl_ramp = int(len(SST.time)/12)

monthly = np.reshape(indata.values,(nyears_cpl_ramp,12,nlats,nlons))
clim = monthly.mean(axis=0)
print(clim.shape)

global_SST_anoms = SST - np.tile(clim,[nyears_cpl_ramp,1,1])
```

**Note: we are using surface temperature from the atmospheric files, rather than the surface temperature from the ocean files: this is because the ocean data are on a different grid, that would require more complex re-gridding**


We are going to calculate EOFs using the EOF package written by Andrew Dawson: https://github.com/ajdawson/eofs

I recommend trying to follow the example here: https://github.com/ajdawson/eofs/blob/master/examples/standard/sst_example.py to find the ENSO signal in our temperature anomalies. You will have to make some changes due to changes in syntax from older version of python.

If you get stuck, have a look at the code below.

```{code-cell} ipython3

```

```{code-cell} ipython3
# Create an EOF solver to do the EOF analysis. Square-root of cosine of
# latitude weights are applied before the computation of EOFs.
coslat = np.cos(np.deg2rad(global_SST_anoms.lat))
wgts = np.sqrt(coslat)
wgts_tile = np.transpose(np.tile(wgts,(nlons,1)))

# Check weights:
plt.contourf(global_SST_anoms.lon,global_SST_anoms.lat,wgts_tile)
plt.colorbar()
# Calculate EOFs
solver = Eof(global_SST_anoms.values, weights=wgts_tile)
```

```{code-cell} ipython3
eof1 = solver.eofsAsCorrelation(neofs=1)
pc1 = solver.pcs(npcs=1, pcscaling=1)

# Plot the leading EOF expressed as correlation in the Pacific domain.
clevs = np.linspace(-1, 1, 11)
ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=190))
fill = ax.contourf(global_SST_anoms.lon, global_SST_anoms.lat, eof1.squeeze(), clevs,
                   transform=ccrs.PlateCarree(), cmap=plt.cm.RdBu_r)
ax.add_feature(cfeature.LAND, facecolor='w', edgecolor='k')
cb = plt.colorbar(fill, orientation='horizontal')
cb.set_label('correlation coefficient', fontsize=12)
plt.title('EOF1 expressed as correlation', fontsize=16)

# Plot the leading PC time series.
plt.figure()
months = range(1, 12*80+1)
plt.plot(months, pc1, color='b', linewidth=2)
plt.axhline(0, color='k')
plt.title('PC1 Time Series')
plt.xlabel('Year')
plt.ylabel('Normalized Units')
plt.ylim(-3, 3)

plt.show()
```

**Discussion:** _What is the main pattern that we see in the first EOF? Is this the ENSO signal? If not, what is it?_

**Exercise:** _Repeat the analysis above with the extra step required to get the ENSO signal as the first EOF_

+++

**Exercise:** _We have already seen that the power spectrum of the Nino3 variability in the slab ocean model does not match observations. Have a look at the first EOF of SST in the slab ocean model. What does this tell you about the spatial distribution of variability in the slab ocean model?_


### Further Exploration
**Open-ended exercise:** _Read section 8.4 of the Hartmann book. Use the tools provided in this notebook to create one or two more plots exploring the variability in the CESM data. You could:_
- look at the effect of CO2 on the ENSO spectra and spatial distribution by comparing the first and last years of the cpl_CO2_ramp experiment. You could also look at the CO2 rampdown experiment in the Thredds catalogue
- Look at variability in different regions, investigating, for example, the PDO, or the AMO.
- Look at differences between in ENSO, PDO, AMO characteristics for different 30 year chunks of the 80 year simulations - what can this teach you about our confidence of low frequency variability from relatively short observation records?



To better understand low-frequency variability, particularly multi-decadal variability, we need more data than we have from observations. One way to get these data is by running ensembles of climate models. This is the theme of the next notebook, which will introduce you to the CESM Large Ensemble.

```{code-cell} ipython3

```
