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

+++ {"slideshow": {"slide_type": "slide"}}

# Who needs spectral bands? We do. Some baby steps...

This notebook is part of [The Climate Laboratory](https://brian-rose.github.io/ClimateLaboratoryBook) by [Brian E. J. Rose](http://www.atmos.albany.edu/facstaff/brose/index.html), University at Albany.

+++ {"slideshow": {"slide_type": "slide"}}

____________
<a id='section1'></a>

## 1. What if CO$_2$ actually behaved like a Grey Gas?
____________

+++ {"slideshow": {"slide_type": "slide"}}

Suppose that CO$_2$ actually behaved as a grey gas. In other words, no spectral dependence in absorptivity.

If we then **double the CO2 concentration** in the atmosphere, we double the number of absorbers. This should imply that we also **double the absorption cross-section** $\kappa$. Following the notation from our [lecture on grey-gas radiative transfer](https://brian-rose.github.io/ClimateLaboratoryBook/courseware/radiative-transfer.html#2.-The-Grey-Gas-Model), we have:

$$ \kappa^\prime = 2 ~ \kappa $$

+++ {"slideshow": {"slide_type": "slide"}}

This would imply that we **double the optical thickness of every layer**:

$$ \Delta \tau^\prime  = 2 \left( -\frac{\kappa}{g} \Delta p \right) = 2 ~ \Delta \tau$$ 

+++ {"slideshow": {"slide_type": "slide"}}

And since [the absorptivity / emissivity of each layer](https://brian-rose.github.io/ClimateLaboratoryBook/courseware/radiative-transfer.html#Emissivity) is

$$  \epsilon = 1 - \exp\big( - \Delta \tau \big)  $$

the **modified absorptivity** is

$$ \epsilon^\prime = 1 - \exp\big( - 2\Delta \tau \big) = 1 - \left( \exp\big( - \Delta \tau \big)\right)^2 = 1 - (1-\epsilon)^2 $$
or simply
$$ \epsilon^\prime = 2 \epsilon  - \epsilon^2 $$

(Note that $\epsilon^\prime = 2 \epsilon$ for very thin layers, for which $\epsilon$ is small).

+++ {"slideshow": {"slide_type": "slide"}}

### What does our 2-layer analytical model then say about the radiative forcing?

Recall that [we tuned the two-layer grey gas model](https://brian-rose.github.io/ClimateLaboratoryBook/courseware/elementary-greenhouse.html#4.-Tuning-the-grey-gas-model-to-observations) with

$$ \epsilon = 0.586 $$

to get the observed OLR with observed temperatures.

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
---
#  Applying the above formula
eps = 0.586
print('Doubling a grey gas absorber would change the absorptivity from {:.3} to {:.3}'.format(eps, 2*eps - eps**2))
```

+++ {"slideshow": {"slide_type": "-"}}

**If CO2 behaved like a grey gas**, doubling it would cause a huge increase in the absorptivity of each layer!

+++ {"slideshow": {"slide_type": "slide"}}

[We previously worked out that the radiative forcing in this model](https://brian-rose.github.io/ClimateLaboratoryBook/courseware/elementary-greenhouse.html#The-radiative-forcing-(change-in-OLR)-depends-on-the-lapse-rate!) (with the observed lapse rate) is about +2.6 W m$^{-2}$ for a 2% increase in $\epsilon$.

```{code-cell} ipython3
forcing_rate = 2.6 / 0.02   # W/m2 forcing per fractional increase in epsilon
```

Our hypothetical doubling of "grey CO$_2$" yields an increase from 0.586 to 0.829, or more than 40%:

```{code-cell} ipython3
fractional_increase = (0.829 - 0.586) / 0.586
```

So roughly speaking, this should yield a radiative forcing 20 times larger than +2.6 W m$^{-2}$:

```{code-cell} ipython3
radiative_forcing = forcing_rate * fractional_increase  # W/m2
print(radiative_forcing)
```

**Our hypothetical doubling of "grey CO$_2$" gives a radiative forcing greater than 50 W m$^{-2}$.** 

This is an absolutely enormous number. Assuming a [net climate feedback of -1.3 W m$^{-2}$ K$^{-1}$](https://brian-rose.github.io/ClimateLaboratoryBook/courseware/sensitivity-feedback.html#7.-Feedbacks-diagnosed-from-complex-climate-models) (consistent with the CMIP5 model ensemble)
would then give us a truly astronomical **equilibrium climate sensitivity of 41 K**:

```{code-cell} ipython3
lambda_net = -1.3  #  W/m2/K
ecs = radiative_forcing / -(lambda_net)  # K
print(ecs)
```

+++ {"slideshow": {"slide_type": "slide"}}

### Conclusions:

1. **If CO2 did behave like a grey gas, we would be toast\*!** 
2. The Grey Gas model is insufficient for understanding radiative forcing and feedback.

\* *Phrase borrowed with great respect from [R. Pierrehumbert (2010), Principles of Planetary Climate, Cambridge University Press.](https://geosci.uchicago.edu/~rtp1/PrinciplesPlanetaryClimate/), which is easily to best textbook that exists on this subject.*

+++ {"slideshow": {"slide_type": "slide"}}

____________
<a id='section2'></a>

## 2. Another look at observed spectra
____________

It's time to move away from the Grey Gas approximation and look more carefully at the actual observed spectra of solar and terrestrial radiation.

+++ {"slideshow": {"slide_type": "slide"}}

### Observed solar spectra

The following figure shows observed spectra of solar radiation at TOA and at the surface, along with the theoretical Planck function for a blackbody at 5525 K.

+++

<img src='https://upload.wikimedia.org/wikipedia/commons/e/e7/Solar_spectrum_en.svg'>

+++ {"slideshow": {"slide_type": "slide"}}

> This figure shows the solar radiation spectrum for direct light at both the top of the Earth's atmosphere and at sea level. The sun produces light with a distribution similar to what would be expected from a 5525 K (5250 °C) blackbody, which is approximately the sun's surface temperature. As light passes through the atmosphere, some is absorbed by gases with specific absorption bands. Additional light is redistributed by Raleigh scattering, which is responsible for the atmosphere's blue color. These curves are based on the American Society for Testing and Materials (ASTM) Terrestrial Reference Spectra, which are standards adopted by the photovoltaics industry to ensure consistent test conditions and are similar to the light that could be expected in North America. Regions for ultraviolet, visible and infrared light are indicated.

Source: http://commons.wikimedia.org/wiki/File:Solar_spectrum_en.svg

+++ {"slideshow": {"slide_type": "slide"}}

- The figure shows that that the incident beam at TOA has the shape of a blackbody radiator. 
- By the time the beam arrives at the surface, it is strongly depleted at specific wavelengths.
- Absorption by O$_3$ (ozone) depletes almost the entire ultraviolet spectrum.
- Weaker absorption features, mostly due to H$_2$O, deplete some parts of the near-infrared.
- Note that the depletion in the visible band is mostly due to scattering, which depletes the direct beam but contributes diffuse radiation (so we can still see when it's cloudy!)

+++ {"slideshow": {"slide_type": "slide"}}

### Observed terrestrial spectra

This figure shows the Planck function for Earth's surface temperature compared with the spectrum observed from space.

+++

<img src='../images/Terrestrial_spectrum.png'>

+++

Source: https://www.e-education.psu.edu/earth103/node/671

+++ {"slideshow": {"slide_type": "slide"}}

Careful: I'm pretty sure what is plotted here is not the **total** observed spectrum, but rather the part of the **emissions from the surface** that **actual make it out to space**.

As we now, the terrestrial beam from the surface is depleted by absorption by many greenhouse gases, but principally CO$_2$ and H$_2$O.

However there is a spectral band centered on 10 $\mu$m in which the greenhouse effect is very weak. This is the so-called **window region** in the spectrum.

Since absorption is so strong across most of the rest of the infrared spectrum, this window region is a key determinant of the overall greenhouse effect.

+++ {"slideshow": {"slide_type": "slide"}}

#### One very big shortcoming of the Grey Gas model: it ignores the window region

We would therefore like to start using a model that includes enough spectral information that it represents

- the mostly strong CO2 absorption outside the window region
- the weak absorption inside the window region

+++ {"slideshow": {"slide_type": "slide"}}

____________
<a id='section3'></a>

## 3. Water vapor changes under global warming
____________

+++ {"slideshow": {"slide_type": "slide"}}

Another big shortcoming of the Grey Gas model is that it cannot represent the **water vapor feedback**.

We have seen above that H$_2$O is an important absorber in both longwave and shortwave spectra.

We also know that the water vapor load in the atmosphere increases as the climate warms. The primary reason is that the **saturation vapor pressure** increases strongly with temperature.

+++ {"slideshow": {"slide_type": "slide"}}

### Evidence from CESM simulations

Let's take at changes in the mean water vapor fields in the CESM model after a doubling of CO$_2$

```{code-cell} ipython3
---
slideshow:
  slide_type: '-'
---
%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from numpy import cos, deg2rad, log
```

```{code-cell} ipython3
#  Open handles to the data files
#  These files are climatologies calculated over the final years of each simulation
datapath = "http://thredds.atmos.albany.edu:8080/thredds/dodsC/CESMA/"        
ctrl = xr.open_dataset(datapath + 'som_1850_f19/clim/som_1850_f19.cam.h0.clim.nc', decode_times=False)
co2 = xr.open_dataset(datapath + 'som_1850_2xCO2/clim/som_1850_2xCO2.cam.h0.clim.nc', decode_times=False)
```

```{code-cell} ipython3
---
slideshow:
  slide_type: '-'
---
#  Plot cross-sections of the following anomalies under 2xCO2:
#   - Temperature 
#   - Specific humidity
#   - Relative humidity

fig, axes = plt.subplots(1,3, figsize=(16,6))

ax = axes[0]
CS = ax.contourf(ctrl.lat, ctrl.lev, (co2['T'] - ctrl['T']).mean(dim=('time','lon')), 
                 levels=np.arange(-11,12,1), cmap=plt.cm.seismic)
ax.set_title('Temperature (K)')
fig.colorbar(CS, orientation='horizontal', ax=ax)

ax = axes[1]
CS = ax.contourf(ctrl.lat, ctrl.lev, (co2['Q'] - ctrl['Q']).mean(dim=('time','lon'))*1000,
                 levels=np.arange(-3,3.25,0.25), cmap=plt.cm.seismic)
ax.set_title('Specific humidity (g/kg)')
fig.colorbar(CS, orientation='horizontal', ax=ax)

ax = axes[2]
CS = ax.contourf(ctrl.lat, ctrl.lev, (co2['RELHUM'] - ctrl['RELHUM']).mean(dim=('time','lon')),
                 levels=np.arange(-11,12,1), cmap=plt.cm.seismic)
ax.set_title('Relative humidity (%)')
fig.colorbar(CS, orientation='horizontal', ax=ax)

for ax in axes:
    ax.invert_yaxis()
    ax.set_xticks([-90, -60, -30, 0, 30, 60, 90]);
    ax.set_xlabel('Latitude')
    ax.set_ylabel('Pressure')
    
fig.suptitle('Anomalies for 2xCO2 in CESM slab ocean simulations', fontsize=16);
```

+++ {"slideshow": {"slide_type": "slide"}}

### What do you see here?

- Where does the largest warming occur?
- Where does the largest moistening occur?

+++ {"slideshow": {"slide_type": "slide"}}

In fact the specific humidity anomaly has roughly the same shape of the specific humidity field itself -- **it is largest where the temperature is highest**. This is a consequence of the Clausius-Clapeyron relation.

The **relative humidity** anomaly is

- overall rather small (just a few percent)
- Largest in places cold places where the specific humidity is very small.

+++ {"slideshow": {"slide_type": "slide"}}

The smallness of the relative humidity change is a rather remarkable result.

This is not something we can derive from first principles. It is an emergent property of the GCMs. However it is a very robust feature of global warming simulations.

+++ {"slideshow": {"slide_type": "slide"}}

____________
<a id='section4'></a>

## 4. A simple water vapor parameterization
____________

+++ {"slideshow": {"slide_type": "slide"}}

### A credible climate model needs a water vapor feedback

If relative humidity is nearly constant under global warming, and water vapor is a greenhouse gas, this implies a positive feedback that will amplify the warming for a given radiative forcing.

Thus far our simple models have ignored this process, and we have not been able to use them to assess the climate sensitivity.

+++ {"slideshow": {"slide_type": "slide"}}

To proceed towards more realistic models, we have two options:

- **Simulate** all the evaporation, condensation and transport processes that determine the time-mean water vapor field (as is done in the CESM).
- **Parameterize** the dependence of water vapor on temperature by insisting that relative humidity stays constant as the climate changes.

We will now explore this second option, so that we can continue to think of the global energy budget under climate change as a process occurring in a single column.

+++ {"slideshow": {"slide_type": "slide"}}

### Manabe's constant relative humidity parameterization

We are going to adopt a parameterization first used in a very famous paper:

> Manabe, S. and Wetherald, R. T. (1967). Thermal equilibrium of the atmosphere with a given distribution of relative humidity. J. Atmos. Sci., 24(3):241–259.

This paper was the first to give a really credible calculation of climate sensitivity to a doubling of CO2 by accounting for the known spectral properties of CO2 and H2O absorption, as well as the water vapor feedback!

+++ {"slideshow": {"slide_type": "slide"}}

The parameterization is very simple:

We assume that the relative humidity $r$ is a linear function of pressure $p$:

$$ r = r_s \left( \frac{p/p_s - 0.02}{1 - 0.02} \right) $$

where $p_s = 1000$ hPa is the surface pressure, and $r_s$ is a prescribed surface value of relative humidity. Manabe and Wetherald set $r_s = 0.77$, but we should consider this a tunable parameter in our parameterization.

+++ {"slideshow": {"slide_type": "slide"}}

Since this formula gives a negative number above 20 hPa, we also assume that the **specific humidity** has a minimum value of $0.005$ g/kg (a typical stratospheric value).

This formula is implemented in `climlab.radiation.ManabeWaterVapor()`

Using this parameterization, the surface and tropospheric specific humidity will always increase as the temperature increases.

+++ {"slideshow": {"slide_type": "slide"}}

____________
<a id='section5'></a>

## 5. Modeling spectral bands with the `climlab.BandRCModel` process
____________

+++ {"slideshow": {"slide_type": "slide"}}

Here is a brief introduction to the `climlab.BandRCModel` process.

This is a model that divides the spectrum into 7 distinct bands: three shortwave and four longwave.

As we will see, the process works much like the familiar `climlab.RadiativeConvectiveModel`.

+++ {"slideshow": {"slide_type": "slide"}}

## About the spectra

### Shortwave

The shortwave is divided into three channels:

- Channel 0 is the Hartley and Huggins band (extreme UV, 200 - 340 nm, 1% of total flux, strong ozone absorption)
- Channel 1 is Chappuis band (450 - 800 nm, 27% of total flux, moderate ozone absorption)
- Channel 2 is remaining radiation (72% of total flux, largely in the visible range, no ozone absorption)



+++ {"slideshow": {"slide_type": "slide"}}

### Longwave

The longwave is divided into four bands:

- Band 0 is the **window region** (between 8.5 and 11 $\mu$m), 17% of total flux.
- Band 1 is the CO2 absorption channel (the band of strong absorption by CO2 around 15 $\mu$m), 15% of total flux
- Band 2 is a weak water vapor absorption channel, 35% of total flux
- Band 3 is a strong water vapor absorption channel, 33% of total flux

The longwave decomposition is not as easily related to specific wavelengths, as in reality there is a lot of overlap between H$_2$O and CO$_2$ absorption features (as well as absorption by other greenhouse gases such as CH$_4$ and N$_2$O that we are not representing).

+++ {"slideshow": {"slide_type": "slide"}}

### Example usage of the spectral model

```{code-cell} ipython3
import climlab
from climlab import constants as const
```

First try a model with all default parameters. Usage is very similar to the familiar `RadiativeConvectiveModel`.

```{code-cell} ipython3
col1 = climlab.BandRCModel()
print(col1)
```

+++ {"slideshow": {"slide_type": "slide"}}

Check out the list of subprocesses.

We now have a process called `H2O`, in addition to things we've seen before.

The state variables are still just temperatures:

```{code-cell} ipython3
col1.state
```

+++ {"slideshow": {"slide_type": "slide"}}

But the model has a new input field for specific humidity:

```{code-cell} ipython3
col1.q
```

+++ {"slideshow": {"slide_type": "slide"}}

The `H2O` process sets the specific humidity field at every timestep to a specified profile, determined by air temperatures. More on that below. For now, let's compute a radiative equilibrium state.

```{code-cell} ipython3
col1.integrate_years(2)
```

```{code-cell} ipython3
# Check for energy balance
col1.ASR - col1.OLR
```

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
---
fig, ax = plt.subplots()
ax.plot(col1.Tatm, col1.lev, 'c-', label='default')
ax.plot(col1.Ts, climlab.constants.ps, 'co', markersize=16)
ax.invert_yaxis()
ax.set_xlabel('Temperature (K)', fontsize=16)
ax.set_ylabel('Pressure (hPa)', fontsize=16 )
ax.set_title('Temperature profiles', fontsize = 18)
ax.grid()
```

+++ {"slideshow": {"slide_type": "slide"}}

By default this model has convective adjustment.  We can set the adjusted lapse rate by passing a parameter when we create the model.

The model currently has no ozone (so there is no stratosphere). Not very realistic!

+++ {"slideshow": {"slide_type": "slide"}}

### About the radiatively active gases

+++

The Band model is aware of three different absorbing gases: O3 (ozone), CO2, and H2O (water vapor). The abundances of these gases are stored in a dictionary of arrays as follows:

```{code-cell} ipython3
col1.absorber_vmr
```

+++ {"slideshow": {"slide_type": "slide"}}

Ozone and CO2 are both specified in the model. The default, as you see above, is zero ozone, and constant (well-mixed) CO2 at a volume mixing ratio of 3.8E-4 or 380 ppm.

+++ {"slideshow": {"slide_type": "slide"}}

Water vapor is handled differently: it is determined by the model at each timestep. We make the following assumptions, following a classic paper on radiative-convective equilibrium by Manabe and Wetherald (J. Atmos. Sci. 1967):

- the relative humidity just above the surface is fixed at 77% (can be changed of course... see the parameter `col1.relative_humidity`
- water vapor drops off linearly with pressure
- there is a small specified amount of water vapor in the stratosphere.

+++ {"slideshow": {"slide_type": "slide"}}

## Putting in some ozone

+++

We need to provide some ozone data to the model in order to simulate a stratosphere. We will read in some ozone data just as we did in [the previous lecture on grey-gas modeling in climlab](https://brian-rose.github.io/ClimateLaboratoryBook/courseware/grey-radiation-climlab.html#8.-Putting-stratospheric-ozone-in-the-grey-gas-model).

```{code-cell} ipython3
ozone = xr.open_dataset( datapath + 'som_input/ozone_1.9x2.5_L26_2000clim_c091112.nc')
```

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
---
#  Take global (area-weighted) and annual average
weight_ozone = cos(deg2rad(ozone.lat)) / cos(deg2rad(ozone.lat)).mean(dim='lat')
O3_global = (ozone.O3 * weight_ozone).mean(dim=('lat','lon','time'))
print(O3_global)
```

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
---
fig, ax = plt.subplots()
ax.plot( O3_global*1E6, ozone.lev)
ax.invert_yaxis()
ax.set_xlabel('Ozone (ppm)', fontsize=16)
ax.set_ylabel('Pressure (hPa)', fontsize=16 )
ax.set_title('Global, annual mean ozone concentration', fontsize = 16);
```

+++ {"slideshow": {"slide_type": "slide"}}

We are going to create another instance of the model, this time using the same vertical coordinates as the ozone data.

```{code-cell} ipython3
#  Create the column with appropriate vertical coordinate, surface albedo and convective adjustment
col2 = climlab.BandRCModel(lev=ozone.lev)
print( col2)
```

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
---
#  Set the ozone mixing ratio
col2.absorber_vmr['O3'] = O3_global.values
```

```{code-cell} ipython3
#  Run the model out to equilibrium!
col2.integrate_years(2.)
```

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
---
fig, ax = plt.subplots()
ax.plot( col1.Tatm, np.log(col1.lev/1000), 'c-', label='RCE' )
ax.plot( col1.Ts, 0, 'co', markersize=16 )
ax.plot(col2.Tatm, np.log(col2.lev/1000), 'r-', label='RCE O3' )
ax.plot(col2.Ts, 0, 'ro', markersize=16 )
ax.invert_yaxis()
ax.set_xlabel('Temperature (K)', fontsize=16)
ax.set_ylabel('log(Pressure)', fontsize=16 )
ax.set_title('Temperature profiles', fontsize = 18)
ax.grid(); ax.legend()
```

+++ {"slideshow": {"slide_type": "slide"}}

Once we include ozone we get a well-defined stratosphere. 

Things to consider / try:

- Here we used the global annual mean Q = 341.3 W m$^{-2}$. We might want to consider latitudinal or seasonal variations in Q.
- We also used the global annual mean ozone profile! Ozone varies tremendously in latitude and by season. That information is all contained in the ozone data file we opened above. We might explore the effects of those variations.
- We can calculate climate sensitivity in this model by doubling the CO2 concentration and re-running out to the new equilibrium. Does the amount of ozone affect the climate sensitivity?  (example below)
- An important shortcoming of the model: there are no clouds! (that would be the next step in the hierarchy of column models)
- Clouds would act both in the shortwave (increasing the albedo, cooling the climate) and in the longwave (greenhouse effect, warming the climate). Which effect is stronger depends on the vertical structure of the clouds (high or low clouds) and their optical properties (e.g. thin cirrus clouds are nearly transparent to solar radiation but are good longwave absorbers).

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
---
col3 = climlab.process_like(col2)
print( col3)
```

```{code-cell} ipython3
# Let's double CO2.
col3.absorber_vmr['CO2'] *= 2.
```

```{code-cell} ipython3
col3.compute_diagnostics()
print( 'The radiative forcing for doubling CO2 is %f W/m2.' % (col2.diagnostics['OLR'] - col3.diagnostics['OLR']))
```

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
---
col3.integrate_years(3)
```

```{code-cell} ipython3
col3.ASR - col3.OLR
```

```{code-cell} ipython3
print( 'The Equilibrium Climate Sensitivity is %f K.' % (col3.Ts - col2.Ts))
```

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
---
#  An example with no ozone
col4 = climlab.process_like(col1)
print( col4)
```

```{code-cell} ipython3
col4.absorber_vmr['CO2'] *= 2.
col4.compute_diagnostics()
print( 'The radiative forcing for doubling CO2 is %f W/m2.' % (col1.OLR - col4.OLR))
```

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
---
col4.integrate_years(3.)
col4.ASR - col4.OLR
```

```{code-cell} ipython3
print( 'The Equilibrium Climate Sensitivity is %f K.' % (col4.Ts - col1.Ts))
```

Interesting that the model is MORE sensitive when ozone is set to zero.

+++ {"slideshow": {"slide_type": "skip"}}

____________

## Credits

This notebook is part of [The Climate Laboratory](https://brian-rose.github.io/ClimateLaboratoryBook), an open-source textbook developed and maintained by [Brian E. J. Rose](http://www.atmos.albany.edu/facstaff/brose/index.html), University at Albany.

It is licensed for free and open consumption under the
[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/) license.

Development of these notes and the [climlab software](https://github.com/brian-rose/climlab) is partially supported by the National Science Foundation under award AGS-1455071 to Brian Rose. Any opinions, findings, conclusions or recommendations expressed here are mine and do not necessarily reflect the views of the National Science Foundation.
____________

```{code-cell} ipython3
---
slideshow:
  slide_type: skip
---

```
