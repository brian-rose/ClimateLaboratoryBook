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

(nb:radiative-transfer)=
# Modeling non-scattering radiative transfer

This notebook is part of [The Climate Laboratory](https://brian-rose.github.io/ClimateLaboratoryBook) by [Brian E. J. Rose](http://www.atmos.albany.edu/facstaff/brose/index.html), University at Albany.

+++ {"slideshow": {"slide_type": "slide"}}

____________
<a id='section1'></a>

## 1. The two-stream Schwarschild equations
____________

Here we are going to introduce the governing equations of radiative transfer to put what we've been doing on a more solid theoretical footing.

Our derivations here will also serve as a coherent documentation for how some of the radiation solvers are implemented in `climlab`.

+++ {"slideshow": {"slide_type": "slide"}}

### Optical thickness

The **optical thickness** of a layer of absorbers is $\Delta \tau_\nu$. It is the emissivity and absorptivity of a layer of atmosphere.

Passing to the limit of very thin layers, we define $\tau_\nu$ through

$$ \frac{d \tau_\nu}{dp} = -\frac{1}{g} \kappa_\nu $$

where **$\kappa_\nu$ is an absorption cross-section** per unit mass at frequency $\nu$. It has units m$^2$ kg$^{-1}$. $\kappa$ is a measure of the area taken out of the incident beam by absorbers in a unit mass of atmosphere.

In general **$\tau_\nu$ depends on the frequency of the radiation**, as indicated here by the subscript $\nu$.

+++ {"slideshow": {"slide_type": "slide"}}

### Using optical depth as vertical coordinate

Since pressure decreases with altitude, $\tau_\nu$ increases with altitude.

The equations of radiative transfer can be simplified by using $\tau_\nu$ as vertical coordinate instead of pressure.

+++ {"slideshow": {"slide_type": "slide"}}

### Absorption cross-section

The specific absorption cross section $\kappa$ depends on the number of molecules of each greenhouse gas encountered by the beam and the absorption properties characteristic to each kind of greenhouse gas molecule. Letting $q_k$ be the mass-specific concentration of greenhouse gas $k$, we may write in general

$$ \kappa(\nu, p, T) = \sum_{k=1}^n \kappa_k\big(\nu, p, T \big) q_k(p) $$

+++ {"slideshow": {"slide_type": "slide"}}

For a well-mixed greenhouse gas, $q_k$ is a constant; for a non-well-mixed gas like water vapor we need to account for the vertical distribution of the gas through $q_k(p)$.

The dependence of $\kappa_k$ on temperature and pressure arises from certain aspects of the physics of molecular absorption. 

+++ {"slideshow": {"slide_type": "slide"}}

### Two-stream Schwarzschild equations

For climate modeling we almost always seperate the total flux into two beams: **upward** and **downward**. 

This involves taking integrals of the full angular dependence of the flux. We'll skip the details here.

+++ {"slideshow": {"slide_type": "slide"}}

Let $U_\nu$ be the upward beam, and $D_\nu$ be the downward beam. The governing equations for these beams are the *Schwarzschild equations*:

\begin{align}
\frac{d U_\nu}{d \tau_\nu} &= -U_\nu + E\big( \nu, T(\tau_\nu) \big) \\
\frac{d D_\nu}{d \tau_\nu} &= D_\nu - E\big( \nu, T(\tau_\nu) \big) 
\end{align}

where $E$ is the **blackbody emission** (both up and down), which in general depends on both **frequency** and **temperature**. We have written temperature as a function of the vertical coordinate (optical depth). 

+++ {"slideshow": {"slide_type": "slide"}}

The emissions are governed by the **Planck function**:
\begin{align}
E &= \pi~ B\big( \nu, T \big) \\
B\big( \nu, T \big) &= \frac{2 h \nu^3}{c^2} \frac{1}{\exp \left( \frac{h \nu}{k T} \right) -1} 
\end{align}

with these fundamental physical constants:

- $h = 6.626 \times 10^{-34} ~\text{J s} $ is Planck's constant
- $c = 3.00 \times 10^8 ~\text{m s}^{-1} $ is the speed of light
- $k = 1.38 \times 10^{-23} ~\text{J K}^{-1} $ is the Boltzmann Thermodynamic Constant

+++ {"slideshow": {"slide_type": "slide"}}

The two-stream equations basically say the beam is **attenuated by absorption** (first term) and **augmented by emission** (second term) in each thin layer of gas.

These equations are valid for beam that are **not affected by scattering**. We may come back to that later.

+++ {"slideshow": {"slide_type": "slide"}}

____________
<a id='section2'></a>

## 2. The Grey Gas Model
____________

+++ {"slideshow": {"slide_type": "slide"}}

The absorption properties $\kappa_i$ of most atmospheric gases varies enormously with the frequency of the radiation. Hence the optical thickness $\tau_\nu$ also has an intricate dependence on wavenumber or frequency. 

Our job as climate modelers is to calculate and understand the net atmospheric absorption and transmission of radiation. To do this thoroughly and accurately, the fluxes must be solved for individually on a very dense grid of wavenumbers, and then the results integrated over all wavenumbers.

+++ {"slideshow": {"slide_type": "slide"}}

Actual radiative transfer codes (as used in GCMs) apply a lot of tricks and shortcuts to simplify this brute-force approach, but lead to sets of equations that are difficult to understand.

However, there is a lot we can understand about the basics of radiative transfer and the greenhouse effect by ignoring the spectral dependence of the flux.

+++ {"slideshow": {"slide_type": "slide"}}

Specifically, we make the approximation

$$ \kappa(\nu, p, T) = \kappa(p) $$

so that the optical depth $\tau$ is now **independent of frequency**.

This is known as the **grey gas approximation**.

+++ {"slideshow": {"slide_type": "slide"}}

## Grey gas versions of the Schwarzschild equations

+++ {"slideshow": {"slide_type": "slide"}}

### Integrating the Planck function

If we assume $\tau_\nu$ is independent of frequency, we can then integrate the two-stream equations over all frequencies.

The integral of the Planck function gives our familiar Stefan-Boltzmann blackbody radiation law

$$ E(T) = \int_0^{\infty} \pi B\big( \nu, T \big) d\nu = \sigma T^4  $$

with 

$$ \sigma = \frac{2 \pi^5 k^4}{15 c^2 h^3} = 5.67 \times 10^{-8} ~\text{W m}^{-2}~\text{K}^{-4}$$

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
---
# climlab has these constants available, and actually calculates sigma from the above formula
import numpy as np
import climlab 

sigma = ((2*np.pi**5 * climlab.constants.kBoltzmann**4) / 
         (15 * climlab.constants.c_light**2 * climlab.constants.hPlanck**3) )
print( sigma)
sigma == climlab.constants.sigma
```

+++ {"slideshow": {"slide_type": "slide"}}

### The grey gas equations

This gives the governing equations for the grey gas model:

\begin{align}
\frac{d U}{d \tau} &= -U + \sigma T(\tau)^4 \\
\frac{d D}{d \tau} &= D - \sigma T(\tau)^4 
\end{align}

These equations now say that the beam is diminished by absorption in a thin layer (first term) and augmented by blackbody emission, where both processes are assumed to be independent of frequency.

+++ {"slideshow": {"slide_type": "slide"}}

### How do the fluxes change across a finite layer of absorbers?

+++ {"slideshow": {"slide_type": "slide"}}

The above equations are **linear, first order ODEs**, and they are uncoupled from each other (because we neglected scattering).

**Consider a layer of atmosphere** from optical level $\tau_{0}$ to $\tau_{1}$. The optical thickness of the layer is $\Delta \tau = \tau_{1} - \tau_{0}$.

The incident upwelling beam from below is denoted $U_{0}$; the upwelling beam that leaves the top of our layer is denoted $U_{1}$. We want to calculate $U_{1}$, which we can get by integrating the equation for $dU/d\tau$ over our layer.

+++ {"slideshow": {"slide_type": "slide"}}

The result is

$$ U_{1} = U_{0} \exp(-\Delta \tau) + \int_{\tau_{0}}^{\tau_{1}} E \exp \big( -(\tau_{1} - \tau) \big) d\tau $$

where $\tau$ is now a dummy variable of integration, and we've written the blackbody emissions as $E = \sigma T^4$.

+++ {"slideshow": {"slide_type": "slide"}}

The change in the downwelling beam is similar:

$$ D_{0} = D_{1} \exp(-\Delta \tau ) + \int_{\tau_0}^{\tau_1} E \exp\big( -(\tau - \tau_{0}) \big) d\tau $$

+++ {"slideshow": {"slide_type": "slide"}}

____________
<a id='section3'></a>

## 3. Discretizing the Grey-gas equations on a finite grid
____________


One particularly important reason to think about these changes over finite layers is that we will typically solve the radiative transfer equations in a numerical model where the temperature is represented on a discrete grid (often using pressure coordinates).

+++ {"slideshow": {"slide_type": "slide"}}

If we assume that **temperature is uniform everywhere in our layer** then the blackbody emission $E$ is also a constant across the layer, which we will denote $E_{0}$.

It can come out the integral and the expressions simplify to

\begin{align}
U_1 &= U_0 ~ \exp(-\Delta \tau )  + E_{0} ~\Big( 1 - \exp(-\Delta \tau) \Big)  \\
D_0 &= D_1 ~ \exp(-\Delta \tau )  + E_{0} ~\Big( 1 - \exp(-\Delta \tau) \Big)
\end{align}

+++ {"slideshow": {"slide_type": "slide"}}

### Transmissitivity
The first term is the **transmission** of radition from the bottom to the top of the layer (or vice-versa). We can define the **transmissivity** of the layer (denoted $t_{0}$) as the fraction of the incident beam that is passed on to the next layer:

\begin{align}
t_{0} &= \frac{U_{0} \exp(-\Delta \tau)}{U_{0}}  \\
 &= \exp(-\Delta \tau)\\
\end{align}

+++ {"slideshow": {"slide_type": "slide"}}

### Emissivity
The second term is the net change in the beam due to **emissions** in the layer. 

We can the define the **emissivity** $\epsilon_0$ of the layer analogously

\begin{align}
\epsilon_{0} &=  1 - \exp(-\Delta \tau) \\
  &= 1 - t_{0} 
\end{align}

+++ {"slideshow": {"slide_type": "slide"}}

### The discrete two-stream equations on a finite pressure grid

Putting this all together gives us two simple equations that govern changes in the upwelling and downwelling beams across a discrete layer of optical depth $\Delta \tau$:

\begin{align}
U_{1} &= t_0 ~ U_{0} + \epsilon_{0} ~ E_{0}  \\
D_{0} &= t_0 ~ D_{1} + \epsilon_{0} ~ E_{0}  \\
\end{align}

+++ {"slideshow": {"slide_type": "slide"}}

Our model will typically be discretized in pressure coordinates. Suppose the thickness of the layer is $\Delta p$, then the optical depth is

$$ \Delta \tau  = -\frac{\kappa}{g} \Delta p$$ 
(the minus sign accounts for the opposite sign conventions of the two coordinates).

+++ {"slideshow": {"slide_type": "slide"}}

Thus the emissivity of the layer is

$$  \epsilon_{0} = 1 - \exp\big( \frac{\kappa}{g} \Delta p \big)  $$

In the grey gas approximation we ignore all spectral dependence of the flux, so $\kappa$ is a constant (we could let it vary in the vertical to represent non-well-mixed greenhouse gases like water vapor), and the blackbody emissions are simply

$$ E_0 = \sigma T_0^4 $$

+++ {"slideshow": {"slide_type": "slide"}}

____________
<a id='section4'></a>

## 4. Matrix equations for the grey gas model
____________

+++ {"slideshow": {"slide_type": "slide"}}

`climlab` implements the discretized two-stream equations as written above. 

We will now write out the equations on a discretized pressure grid with $N$ layers. 

Let the **upwelling flux** be a column vector 

$${\bf{U}} = [U_0, U_1, ..., U_{N-1}, U_N]^T$$

+++ {"slideshow": {"slide_type": "slide"}}

If there are $N$ levels then $\bf{U}$ has $N+1$ elements (i.e. the fluxes are defined at the boundaries between levels). We will number the layers starting from 0 following `numpy` index conventions.

- $U_0$ is the upwelling flux from surface to layer 0.
- $U_1$ is the upwelling flux layer 0 to layer 1, etc.
- $U_N$ is the upwelling flux from layer N-1 (the top level) to space.

+++ {"slideshow": {"slide_type": "slide"}}

Same for the **downwelling flux**

$${\bf{D}} = [D_0, D_1, ..., D_N]^T$$

So $D_N$ is the flux down from space and $D_0$ is the back-radiation to the surface.

+++ {"slideshow": {"slide_type": "slide"}}

The **temperature** and **blackbody emissions** are defined for each $N$ pressure level, and are related by 

$$E_i = \sigma T_i^4$$

+++ {"slideshow": {"slide_type": "slide"}}

### Emissivity and Transmissivity vectors

Let the vector of absorptivity / emissivity be 

$$ {\bf{\epsilon}} = [\epsilon_0, \epsilon_1, ..., \epsilon_{N-1}] $$

where each element is determined by the thickness of the layer and the absorption cross-section for this particular spectral band:

$$ \epsilon_{i} = 1 - \exp\big( \frac{\kappa}{g} \Delta p_i \big) $$

+++ {"slideshow": {"slide_type": "slide"}}

And the transmissivity of individual layers is 

$$ t_{i} = 1 - \epsilon_{i} $$

It is convenient to define a vector of transmissivities ${\bf{t}}$ with $N+1$ elements:

$$ {\bf{t}} = [1, t_0, t_1, ..., t_{N-1}] $$

+++ {"slideshow": {"slide_type": "slide"}}

### The downwelling beam

For the downwelling beam, we define a column vector of emissions with $N+1$ elements:

$$ {\bf{E_{down}}} = [E_0, E_1, ..., E_{N-1}, E_N]^{T} $$

where we define the last element $E_N$ as the **incident flux at the TOA**.

For a longwave model, we would usually set $E_N = 0$. For a shortwave model, this would be the incident solar radiation.

+++ {"slideshow": {"slide_type": "slide"}}

We want a matrix ${\bf{T_{down}}}$ that, when multiplied by $E_N$, gives the downwelling beam at each of the $N+1$ layer interfaces:

$${\bf{D}} = {\bf{T_{down}}} ~ {\bf{E_{down}}} $$

+++ {"slideshow": {"slide_type": "slide"}}

### The upwelling beam

Define a vector of emissions for the upwelling beam thus:

$$ {\bf{E_{up}}} = [up_{sfc}, E_0, E_1, ..., E_{N-1}] $$

+++ {"slideshow": {"slide_type": "slide"}}

We need to add the reflected part of the downwelling beam at the surface to any emissions from the surface:

$$ up_{sfc} = E_{sfc} + \alpha_{sfc} ~ D[0] $$

+++ {"slideshow": {"slide_type": "slide"}}

Now we want a matrix ${\bf{T_{up}}}$ such that the upwelling beam is

$${\bf{U}} = {\bf{T_{up}}} ~ {\bf{E_{up}}} $$

+++ {"slideshow": {"slide_type": "slide"}}

### The transmissivity matrices

$$ {\bf{T_{up}}} = \left[ \begin{array}{ccccc} 1 & 0 & 0 &... & 0 & 0 \\  
                                             t_0 & 1 & 0 & ... & 0 & 0 \\
                                         t_1 t_0 & t_1 & 1 & ... & 0 & 0 \\
                                     t_2 t_1 t_0 & t_2 t_1 & t_2 & ... & 0 & 0 \\
                                     ... & ... & ... & ... & ... & ... \\
 \prod_0^{N-1} t_i & \prod_1^{N-1} t_i & \prod_2^{N-1} t_i & ... & t_{N-1} & 1 
   \end{array} \right] $$
   
 and
 
$$ {\bf{T_{down}}} = {\bf{T_{up}}}^T  $$

These formulas have been implemented in `climlab.radiation.transmissivity.Transmissivity()` using vectorized `numpy` array operations.

```{code-cell} ipython3
---
slideshow:
  slide_type: slide
---
# example with N=2 layers and constant absorptivity
#  we construct an array of absorptivities
eps = np.array([0.58, 0.58])
#  and pass these as argument to the Transmissivity class
trans = climlab.radiation.transmissivity.Transmissivity(eps)
print( 'Matrix Tup is ')
print( trans.Tup)
print( 'Matrix Tdown is ')
print( trans.Tdown)
```

+++ {"slideshow": {"slide_type": "slide"}}

____________
<a id='section5'></a>

## 5. Band-averaged radiation models in `climlab`
____________

The Grey Gas model is a useful first step in understanding how radiation shapes the global energy balance. But we quickly run up against its limitations when trying to understand what really determines climate sensitivity.

What's the next step in the model hierarchy?

+++ {"slideshow": {"slide_type": "slide"}}

Suppose we break up the spectrum into a discrete number $M$ of **spectral bands**. The idea is that we find parts of the spectrum in which the absorption characteristics of the important gases are relatively uniform. We then write the **band-averaged absorption cross section** for gas $k$ and band $j$ as

$$ \kappa_{kj} \big(p, T \big) = \frac{\int_{\nu_j} \kappa_j \big(\nu, p, T \big) d \nu }{  \int_{\nu_j} d \nu } $$

where we integrate over whatever part of the spectrum we have chosen to define band $j$. 

+++ {"slideshow": {"slide_type": "slide"}}

In our band models we will typically ignore any dependence of $\kappa$ on temperature. The total absorption cross section for our band is thus (summing over all absorbing gases):

$$ \kappa_j(p) = \sum_{k=1}^n \kappa_{kj}(p) q_k(p) $$

Notice that once we make this defintion, all of the formulas we wrote down above for the grey gas model can be written nearly identically for the fluxes in each band.

+++ {"slideshow": {"slide_type": "slide"}}

The optical depth in band $j$ is

$$ \Delta \tau_j  = -\frac{\kappa_j}{g} \Delta p$$ 

from which we can define emissivity and transmissivity for band $j$ just as above.

+++ {"slideshow": {"slide_type": "slide"}}

The only difference from the Grey Gas formulas is that the **blackbody emission** in band $j$ (denoted $E_j$) is now only a fraction of $\sigma T^4$.

We will denote this fraction as $b_j$.

+++ {"slideshow": {"slide_type": "slide"}}

The fraction $b_j$ is temperature-dependent, and can be solved by integrating the Planck function:

$$ E_j(T) = \int_{\nu_j} \pi B\big( \nu, T \big) d\nu $$

To simplify our band models, we might choose to fix $b_j$ in advance and just assume

$$ E_j(T) = b_j ~ \sigma ~ T^4 $$

which is sensible if the temperatures don't vary too much.

+++ {"slideshow": {"slide_type": "slide"}}

Regardless of how we calculate $b_j$, they must add up to one over all the bands in our model:

$$ \sum_0^{M-1} b_j = 1 $$

+++ {"slideshow": {"slide_type": "slide"}}

Once we've figured out this division of the total flux into multiple bands, and we know the absorption cross-sections of each band, we can calculate the upwelling and downwelling fluxes independently for each band, **using the same formulas (same code!) as we use in the grey gas model**.

+++ {"slideshow": {"slide_type": "slide"}}

To get the total flux, we just need to sum the beams over all bands:

\begin{align}
U &= \sum_0^{M-1} U_j  \\
D &= \sum_0^{M-1} D_j  
\end{align}

+++ {"slideshow": {"slide_type": "slide"}}

____________
<a id='references'></a>

## References
____________

For many more details about radiative transfer and a more careful derivation of the two-stream equations, see

> Pierrehumbert, R. T. (2010). Principles of Planetary Climate. Cambridge University Press.

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
