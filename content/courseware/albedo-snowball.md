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
(nb:snowball)=
# Ice-albedo feedback and Snowball Earth in the EBM

This notebook is part of [The Climate Laboratory](https://brian-rose.github.io/ClimateLaboratoryBook) by [Brian E. J. Rose](http://www.atmos.albany.edu/facstaff/brose/index.html), University at Albany.

+++

____________

## 1. Review of the 1D EBM
____________

+++

Last time we derived the equation for the one-dimensional EBM with diffusive heat transport:

+++

$$ C \frac{\partial T}{\partial t} = (1-\alpha) ~ Q - \left( A + B~T \right) + \frac{D}{\cos⁡\phi } \frac{\partial }{\partial \phi} \left(   \cos⁡\phi  ~ \frac{\partial T}{\partial \phi} \right) $$

+++

We have chosen the following parameter values, which seems to give a reasonable fit to the observed **annual mean temperature and energy budget**:

- $ A = 210 ~ \text{W m}^{-2}$ (emission at 0$^\circ$C)
- $ B = 2 ~ \text{W m}^{-2}~^\circ\text{C}^{-1} $ (increase in emission per degree, related to net longwave climate feedback)
- $ D = 0.6 ~ \text{W m}^{-2}~^\circ\text{C}^{-1} $ (thermal diffusivity of the climate system)

+++

We looked at the adjustment of this model to equilibrium, with annual mean insolation $\overline{Q(\phi)}$ and specified albedo $\alpha(\phi)$ (giving a reasonable fit to observations).

We also tuned the diffuvisity $D$ so that our annual mean solution has a reasonable pole-to-equator temperature gradient and peak poleward heat transport.

Actually for the new version of this model with interactive ice line, we are going to reduce the diffusivity down to $ D = 0.55 ~ \text{W m}^{-2}~^\circ\text{C}^{-1} $.

+++

____________
<a id='section2'></a>

## 2. Interactive snow/ice line in the EBM
____________

+++

What we want to do today is introduce another process into our model: an **interactive snow and ice line**. 

The idea is simply that, as the climate gets warmer, the snow and ice will retreat poleward, and the planetary albedo will decrease (or vice-versa).

+++

We modeled this in the zero-dimensional model by using a kind of ramp function for the global mean albedo as a function of global mean temperature.

+++

Here, since our model resolves temperature at each latitude, we want to do something more physical: *suppose that the surface is covered in ice and snow wherever the temperature is below some threshold $T_f$.*

+++

### Temperature-dependent ice line

Let the surface albedo be larger wherever the temperature is below some threshold $T_f$:

$$ \alpha\left(\phi, T(\phi) \right) = \left\{\begin{array}{ccc} 
\alpha_0 + \alpha_2 P_2(\sin\phi) & ~ & T(\phi) > T_f  & \text{(no ice)} \\
a_i & ~ & T(\phi) \le T_f & \text{(ice-covered)} \\
\end{array} \right. $$

where $P_2(\sin\phi) = \frac{1}{2}\left( 3\left(\sin\phi\right)^2 - 1 \right) $ is called the *second Legendre Polynomial* (just a mathematically convenient description of a smooth variation between the equator and pole).

+++

Empirically, we follow classic work by Budyko and set the threshold temperature

$$ T_f = -10^\circ\text{C} $$

+++

This is known as a "step function" formula, because the value of $\alpha$ steps or jumps up to a higher value as we cross the ice line.

+++

____________
<a id='section3'></a>

## 3. Solving the EBM with variable snow/ice line in CLIMLAB
____________

```{code-cell} ipython3
%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
import climlab
from climlab import constants as const
```

```{code-cell} ipython3
#  for convenience, set up a dictionary with our reference parameters
param = {'D':0.55, 'A':210, 'B':2, 'a0':0.3, 'a2':0.078, 'ai':0.62, 'Tf':-10.}
model1 = climlab.EBM_annual(name='EBM with interactive ice line',
                            num_lat=180, 
                            D=0.55, 
                            A=210., 
                            B=2., 
                            Tf=-10., 
                            a0=0.3, 
                            a2=0.078, 
                            ai=0.62)
print(model1)
```

Because we provided a parameter `ai` for the icy albedo, our model now contains several sub-processes contained within the process called `albedo`. Together these implement the step-function formula above.

The process called `iceline` simply looks for grid cells with temperature below $T_f$.

```{code-cell} ipython3
print(model1.param)
```

```{code-cell} ipython3
#  A python shortcut... we can use the dictionary to pass lots of input arguments simultaneously:

#  same thing as before, but written differently:
model1 = climlab.EBM_annual(name='EBM with interactive ice line',
                            num_lat=180,
                            **param)
print(model1)
```

```{code-cell} ipython3
def ebm_plot(e, return_fig=False):    
    templimits = -60,32
    radlimits = -340, 340
    htlimits = -6,6
    latlimits = -90,90
    lat_ticks = np.arange(-90,90,30)
    
    fig = plt.figure(figsize=(8,12))

    ax1 = fig.add_subplot(3,1,1)
    ax1.plot(e.lat, e.Ts)
    ax1.set_ylim(templimits)
    ax1.set_ylabel('Temperature (deg C)')
    
    ax2 = fig.add_subplot(3,1,2)
    ax2.plot(e.lat, e.ASR, 'k--', label='SW' )
    ax2.plot(e.lat, -e.OLR, 'r--', label='LW' )
    ax2.plot(e.lat, e.net_radiation, 'c-', label='net rad' )
    ax2.plot(e.lat, e.heat_transport_convergence, 'g--', label='dyn' )
    ax2.plot(e.lat, e.net_radiation + e.heat_transport_convergence, 'b-', label='total' )
    ax2.set_ylim(radlimits)
    ax2.set_ylabel('Energy budget (W m$^{-2}$)')
    ax2.legend()
    
    ax3 = fig.add_subplot(3,1,3)
    ax3.plot(e.lat_bounds, e.heat_transport )
    ax3.set_ylim(htlimits)
    ax3.set_ylabel('Heat transport (PW)')
    
    for ax in [ax1, ax2, ax3]:
        ax.set_xlabel('Latitude')
        ax.set_xlim(latlimits)
        ax.set_xticks(lat_ticks)
        ax.grid()
    
    if return_fig:
        return fig
```

```{code-cell} ipython3
model1.integrate_years(5)
```

Diagnostics in this model are mostly on the latitude axis, e.g.:

```{code-cell} ipython3
model1.ASR.to_xarray()
```

There is a built-in utility to take properly area-weighted global averages!

+++

This gives us the net global energy imbalance:

```{code-cell} ipython3
climlab.global_mean(model1.ASR - model1.OLR)
```

There is also a built-in diagnostic `net_radiation` that has the same information (i.e. ASR - OLR):

```{code-cell} ipython3
climlab.global_mean(model1.net_radiation)
```

Since it's not fully equilibrated yet, we can run it out a little longer:

```{code-cell} ipython3
# Integrate out to equilibrium.
model1.integrate_years(5)
#  Check for energy balance
print(climlab.global_mean(model1.net_radiation))
f = ebm_plot(model1)
```

```{code-cell} ipython3
#  There is a diagnostic that tells us the current location of the ice edge:
model1.icelat
```

This model is tuned up to reasonable "present-day" conditions.

+++

____________
<a id='section4'></a>

## 4. Polar-amplified warming in the EBM
____________

+++

### Add a small radiative forcing

The equivalent of doubling CO2 in this model is something like 

$$ A \rightarrow A - \delta A $$

where $\delta A = 4$ W m$^{-2}$.


```{code-cell} ipython3
model1.subprocess['LW'].A
```

```{code-cell} ipython3
deltaA = 4.

#  This is a very handy way to "clone" an existing model:
model2 = climlab.process_like(model1)

#  Now change the longwave parameter:
model2.subprocess['LW'].A = param['A'] - deltaA
#  and integrate out to equilibrium again
model2.integrate_years(5, verbose=False)

plt.plot(model1.lat, model1.Ts, label='model1')
plt.plot(model2.lat, model2.Ts, label='model2')
plt.legend(); plt.grid()
```

**The warming is polar-amplified**:  more warming at the poles than elsewhere.

Why?

Also, the current ice line is now:

```{code-cell} ipython3
model2.icelat
```

There is no ice left!

+++

Let's do some more greenhouse warming:

```{code-cell} ipython3
model3 = climlab.process_like(model1)
model3.subprocess['LW'].A = param['A'] - 2*deltaA
model3.integrate_years(5, verbose=False)

plt.plot(model1.lat, model1.Ts, label='model1')
plt.plot(model2.lat, model2.Ts, label='model2')
plt.plot(model3.lat, model3.Ts, label='model3')
plt.xlim(-90, 90)
plt.grid()
plt.legend()
```

In the ice-free regime, there is no polar-amplified warming. A uniform radiative forcing produces a uniform warming.

+++

____________
<a id='section5'></a>

## 5. A different kind of climate forcing: changing the solar constant
____________

+++

Historically EBMs have been used to study the climatic response to a change in the energy output from the Sun.

We can do that easily with `climlab`:

```{code-cell} ipython3
m = climlab.EBM_annual(num_lat=180, **param)
#  The current (default) solar constant, corresponding to present-day conditions:
m.subprocess.insolation.S0
```

###  What happens if we decrease $S_0$?

```{code-cell} ipython3
#  First, get to equilibrium
m.integrate_years(5.)
#  Check for energy balance
climlab.global_mean(m.net_radiation)
```

```{code-cell} ipython3
m.icelat
```

```{code-cell} ipython3
#  Now make the solar constant smaller:
m.subprocess.insolation.S0 = 1300.
```

```{code-cell} ipython3
#  Integrate to new equilibrium
m.integrate_years(10.)
#  Check for energy balance
climlab.global_mean(m.net_radiation)
```

```{code-cell} ipython3
m.icelat
```

```{code-cell} ipython3
ebm_plot(m)
```

A much colder climate!  The ice line is sitting at 54º. The heat transport shows that the atmosphere is moving lots of energy across the ice line, trying hard to compensate for the strong radiative cooling everywhere poleward of the ice line.

+++

____________
<a id='section6'></a>

## 6. The large ice cap instability
____________

+++

###  What happens if we decrease $S_0$ even more?

```{code-cell} ipython3
#  Now make the solar constant smaller:
m.subprocess.insolation.S0 = 1200.
#  First, get to equilibrium
m.integrate_years(5.)
#  Check for energy balance
climlab.global_mean(m.net_radiation)
```

```{code-cell} ipython3
m.integrate_years(10.)
#  Check for energy balance
climlab.global_mean(m.net_radiation)
```

```{code-cell} ipython3
ebm_plot(m)
```

Something very different happened! Where is the ice line now?

```{code-cell} ipython3
m.icelat
```

### Now what happens if we set $S_0$ back to its present-day value?

```{code-cell} ipython3
#  Now make the solar constant smaller:
m.subprocess.insolation.S0 = 1365.2
#  First, get to equilibrium
m.integrate_years(5.)
#  Check for energy balance
climlab.global_mean(m.net_radiation)
```

```{code-cell} ipython3
ebm_plot(m)
```

Is this the same climate we started with?

+++

This is an example of a **hysteresis** in the climate system:  the state of the climate depends on its history!

- A global cooling caused snow and ice to expand to the equator
- External conditions (i.e. the solar constant) returned back to its present-day value
- The climate stayed cold and completely ice-covered.

If the oceans froze over and the Earth were covered in ice and snow today, it would remain that way!

+++

____________
<a id='section7'></a>

## 7. The Neoproterozoic Snowball Earth
____________

+++

### The Geologic Time Scale

First, some information on the nomenclature for Earth history:

+++

<img src='../images/GeoTimeScale2009.png'>

Source: Walker, J. and Geissman, J. (2009). Geologic time scale. Technical report, Geological Society of America.

+++

The long view of glacial epochs on Earth:

+++

<img src='../images/Hoffman_etal_SciAdv_Fig2.pdf' width="800">

Source: [Hoffman et al. (2017), Science Advances 3:e1600983, doi:10.1126/sciadv.1600983](https://advances.sciencemag.org/lookup/doi/10.1126/sciadv.1600983)

+++

### Extensive evidence for large glaciers at sea level in the tropics 

Evidently the climate was **very cold** at these times (635 Ma and 715 Ma)

+++

<img src='../images/Hoffman_Li_2009.png'>

Source: [Hoffman, P. F. and Li, Z.-X. (2009). A palaeogeographic context for Neoproterozoic glaciation. Palaeogeogr. Palaeoclimatol. Palaeoecol., 277:158–172.](https://doi.org/10.1016/j.palaeo.2009.03.013)

+++

###  The Snowball Earth hypothesis

Various bizarre features in the geological record from 635 and 715 Ma ago indicate that the Earth underwent some very extreme environmental changes… at least twice. The **Snowball Earth hypothesis** postulates that:

- The Earth was completely ice-covered (including the oceans)
- The total glaciation endured for millions of years
- CO$_2$ slowly accumulated in the atmosphere from volcanoes
- Weathering of rocks (normally acting to reduce CO$_2$) extremely slow due to cold, dry climate
- Eventually the extreme greenhouse effect is enough to melt back the ice
- The Earth then enters a period of extremely hot climate.

+++

The hypothesis rests on a phenomenon first discovered by climate modelers in the Budyko-Sellers EBM: **runaway ice-albedo feedback** or **large ice cap instability**.

+++

____________
<a id='section8'></a>

## 8. Computing the complete hysteresis curve for the 1D diffusive EBM
____________

+++

<div class="alert alert-warning">
The calculations in this section may take a long time to complete, depending on the speed of your computer.
</div>

+++

The ice edge in our model is always where the temperature crosses $T_f = -10^\circ$C. The system is at **equilibrium** when the temperature is such that there is a balance between ASR, OLR, and heat transport convergence everywhere. 

Suppose that sun was hotter or cooler at different times (in fact it was significantly cooler during early Earth history). That would mean that the solar constant $S_0 = 4Q$ was larger or smaller. We should expect that the temperature (and thus the ice edge) should increase and decrease as we change $S_0$. 

+++

$S_0$ during the Neoproterozoic Snowball Earth events is believed to be about 93% of its present-day value, or about 1270 W m$^{-2}$.

We are going to look at how the **equilibrium** ice edge depends on $S_0$, by integrating the model out to equilibrium for lots of different values of $S_0$. We will start by slowly decreasing $S_0$, and then slowly increasing $S_0$.

```{code-cell} ipython3
model2 = climlab.EBM_annual(num_lat = 360, **param)
S0array = np.linspace(1400., 1200., 200)
model2.integrate_years(5)
icelat_cooling = np.empty_like(S0array)
icelat_warming = np.empty_like(S0array)
# First cool....
for n in range(S0array.size):
    model2.subprocess['insolation'].S0 = S0array[n]
    model2.integrate_years(10, verbose=False)
    icelat_cooling[n] = np.max(model2.icelat)
# Then warm...
for n in range(S0array.size):
    model2.subprocess['insolation'].S0 = np.flipud(S0array)[n]
    model2.integrate_years(10, verbose=False)
    icelat_warming[n] = np.max(model2.icelat)
# For completeness -- also start from present-day conditions and warm up.
model3 = climlab.EBM_annual(num_lat=360, **param)
S0array3 = np.linspace(1350., 1400., 50)
icelat3 = np.empty_like(S0array3)
for n in range(S0array3.size):
    model3.subprocess['insolation'].S0 = S0array3[n]
    model3.integrate_years(10, verbose=False)
    icelat3[n] = np.max(model3.icelat)
```

```{code-cell} ipython3
fig = plt.figure( figsize=(10,6) )
ax = fig.add_subplot(111)
ax.plot(S0array, icelat_cooling, 'r-', label='cooling' )
ax.plot(S0array, icelat_warming, 'b-', label='warming' )
ax.plot(S0array3, icelat3, 'g-', label='warming' )
ax.set_ylim(-10,100)
ax.set_yticks((0,15,30,45,60,75,90))
ax.grid()
ax.set_ylabel('Ice edge latitude', fontsize=16)
ax.set_xlabel('Solar constant (W m$^{-2}$)', fontsize=16)
ax.plot( [const.S0, const.S0], [-10, 100], 'k--', label='present-day' )
ax.legend(loc='upper left')
ax.set_title('Solar constant versus ice edge latitude in the EBM with albedo feedback', fontsize=16);
```

There are actually up to 3 different climates possible for a given value of $S_0$!

+++

### How to un-freeze the Snowball

+++

The graph indicates that if the Earth were completely frozen over, it would be perfectly happy to stay that way even if the sun were brighter and hotter than it is today.

Our EBM predicts that (with present-day parameters) the equilibrium temperature at the equator in the Snowball state is about -33ºC, which is much colder than the threshold temperature $T_f = -10^\circ$C. How can we melt the Snowball?

+++

We need to increase the avaible energy sufficiently to get the equatorial temperatures above this threshold! That is going to require a much larger increase in $S_0$ (could also increase the greenhouse gases, which would have a similar effect)!

Let's crank up the sun to 1830 W m$^{-2}$ (about a 35% increase from present-day).

```{code-cell} ipython3
my_ticks = [-90,-60,-30,0,30,60,90]

model4 = climlab.process_like(model2)  # initialize with cold Snowball temperature
model4.subprocess['insolation'].S0 = 1830.
model4.integrate_years(40)
plt.plot(model4.lat, model4.Ts)
plt.xlim(-90,90); plt.ylabel('Temperature'); plt.xlabel('Latitude')
plt.grid(); plt.xticks(my_ticks)
print('The ice edge is at ' + str(model4.icelat) + ' degrees latitude.' )
```

Still a Snowball... but just barely! The temperature at the equator is just below the threshold.

Try to imagine what might happen once it starts to melt. The solar constant is huge, and if it weren't for the highly reflective ice and snow, the climate would be really really hot!

We're going to increase $S_0$ one more time...

```{code-cell} ipython3
model4.subprocess['insolation'].S0 = 1840.
model4.integrate_years(10)
plt.plot(model4.lat, model4.Ts)
plt.xlim(-90,90); plt.ylabel('Temperature'); plt.xlabel('Latitude')
plt.grid(); plt.xticks(my_ticks);
```

Suddenly the climate looks very very different again! The global mean temperature is

```{code-cell} ipython3
model4.global_mean_temperature()
```

A roasty 58ºC, and the poles are above 20ºC. A tiny increase in $S_0$ has led to a very drastic change in the climate.

+++

Now we will complete the plot of ice edge versus solar constant.

```{code-cell} ipython3
S0array_snowballmelt = np.linspace(1400., 1900., 50)
icelat_snowballmelt = np.empty_like(S0array_snowballmelt)
icelat_snowballmelt_cooling = np.empty_like(S0array_snowballmelt)

for n in range(S0array_snowballmelt.size):
    model2.subprocess['insolation'].S0 = S0array_snowballmelt[n]
    model2.integrate_years(10, verbose=False)
    icelat_snowballmelt[n] = np.max(model2.icelat)
    
for n in range(S0array_snowballmelt.size):
    model2.subprocess['insolation'].S0 = np.flipud(S0array_snowballmelt)[n]
    model2.integrate_years(10, verbose=False)
    icelat_snowballmelt_cooling[n] = np.max(model2.icelat)
```

```{code-cell} ipython3
fig = plt.figure( figsize=(18,6) )
ax = fig.add_subplot(111)
ax.plot(S0array, icelat_cooling, 'r-', label='cooling' )
ax.plot(S0array, icelat_warming, 'b-', label='warming' )
ax.plot(S0array3, icelat3, 'g-', label='warming' )
ax.plot(S0array_snowballmelt, icelat_snowballmelt, 'b-' )
ax.plot(S0array_snowballmelt, icelat_snowballmelt_cooling, 'r-' )
ax.set_ylim(-10,100)
ax.set_yticks((0,15,30,45,60,75,90))
ax.grid()
ax.set_ylabel('Ice edge latitude', fontsize=16)
ax.set_xlabel('Solar constant (W m$^{-2}$)', fontsize=16)
ax.plot( [const.S0, const.S0], [-10, 100], 'k--', label='present-day' )
ax.legend(loc='upper left')
ax.set_title('Solar constant versus ice edge latitude in the EBM with albedo feedback', fontsize=16);
```

The upshot:

- For extremely large $S_0$, the only possible climate is a hot Earth with no ice.
- For extremely small $S_0$, the only possible climate is a cold Earth completely covered in ice.
- For a large range of $S_0$ including the present-day value, more than one climate is possible!
- Once we get into a Snowball Earth state, getting out again is rather difficult!

+++

____________

## Credits

This notebook is part of [The Climate Laboratory](https://brian-rose.github.io/ClimateLaboratoryBook), an open-source textbook developed and maintained by [Brian E. J. Rose](http://www.atmos.albany.edu/facstaff/brose/index.html), University at Albany.

It is licensed for free and open consumption under the
[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/) license.

Development of these notes and the [climlab software](https://github.com/brian-rose/climlab) is partially supported by the National Science Foundation under award AGS-1455071 to Brian Rose. Any opinions, findings, conclusions or recommendations expressed here are mine and do not necessarily reflect the views of the National Science Foundation.
____________

```{code-cell} ipython3

```
