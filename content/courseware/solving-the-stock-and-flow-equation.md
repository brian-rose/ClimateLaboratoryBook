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


+++

### Stock and flow with feedback

---

Below we use the approach of Math 102 chapters 11 and 12 to show that for our stock and flow equation with
constant climate sensitivity $\lambda$ and forcing $\Delta F$ the temperature response is given by

$$\Delta T = \lambda \Delta F \left (1 - \exp (-t/\tau ) \right )$$

1\.  Start with the definition for the energy in a 1 $m^2$ column of the ocean mixed layer, compared to a reference
temperature $T_{ref}$ like the average temperature between 1960-1980:

$$E = \rho_w c_p H \Delta T\ (J\,m^{-2})$$

where $\rho_w\ (kg\,m^{-3})$ and $c_p\ (J\,kg^{-1}\,K^{-1})$ are the density and heat capacity of liquid
water, H (m) is the depth of the mixed layer and $\Delta T = T - T_{ref}$ is the temperature difference.  Note that
since $T_{ref}$ is a constant, $\frac{d\Delta T}{dt} = \frac{d (T - T_{ref})}{dt} = \frac{dT}{dt}$

---

+++

2\. We know that the energy in the column is going to change due to the combination of forcing and feedbacks:

$$\frac{dE}{dt} = \Delta F - \frac{\Delta T}{\lambda}$$

or expanding E:

$$\rho_w c_p H \frac{\Delta T}{dt} =\Delta F - \frac{\Delta T}{\lambda}$$

---

+++

3\. First rearrange the terms:

$$\frac{d \Delta T}{dt} = \frac{\lambda \Delta F}{\tau} - \frac{\Delta T}{\tau}$$

where we define the time constant $\tau = \lambda \rho_w c_p H$.

Then transform to the new variable $z$:

$$z = \lambda \Delta F - \Delta T$$  

where, since $\lambda \Delta F$ is constant:

$$\frac{dz}{dt} = - \frac{\Delta T}{dt}$$

So the stock and flow equation becomes:

$$\frac{dz}{dt} = -\frac{z}{\tau}$$

---

+++

4\. Substitute $z = C \exp(-t/\tau)$.   To find the constant $C$ recognize
that at time $t=0$ $\Delta T = 0$, so $z(0) = C = \lambda \Delta F$.   That means that:

$$z = C \exp(-t/\tau) = \lambda \Delta F \exp (-t/\tau) = \lambda \Delta F - \Delta T$$

and solving for $\Delta T$:

$$ \lambda \Delta F \left ( \exp (-t/\tau) - 1 \right ) = - \Delta T$$

and rearranging gives the answer:


$$ \Delta T = \lambda \Delta F \left (1 - \exp (-t/\tau) \right ) $$


