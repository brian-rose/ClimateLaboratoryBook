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

# Stock and flow with feedback

---

Below we derive Hartmann equation 13.7  with
constant climate sensitivity $\lambda$ and forcing $Q_0$ the temperature response is given by

$$\Delta T = \lambda Q_0 \left (1 - \exp (-t/\tau ) \right )$$

1\.  Start with the definition for the energy in a 1 $m^2$ column of the ocean mixed layer, compared to a reference
temperature $T_{ref}$ like the average temperature between 1960-1980:

$$E = \rho_w c_p H \Delta T\ (J\,m^{-2})$$

where $\rho_w\ (kg\,m^{-3})$ and $c_p\ (J\,kg^{-1}\,K^{-1})$ are the density and heat capacity of liquid
water, H (m) is the depth of the mixed layer and $\Delta T = T - T_{ref}$ is the temperature difference.  Note that
since $T_{ref}$ is a constant, $\frac{d\Delta T}{dt} = \frac{d (T - T_{ref})}{dt} = \frac{dT}{dt}$

---

+++

2\. We know that the energy in the column is going to change due to the combination of forcing and feedbacks:

$$\frac{dE}{dt} = Q_0 - \frac{\Delta T}{\lambda}$$

or expanding E:

$$\rho_w c_p H \frac{\Delta T}{dt} =Q_0 - \frac{\Delta T}{\lambda}$$

---

+++

3\. First rearrange the terms:

$$\frac{d \Delta T}{dt} = \frac{\lambda Q_0}{\tau} - \frac{\Delta T}{\tau}$$

where we define the time constant $\tau = \lambda \rho_w c_p H$.

Then transform to the new variable $z$:

$$z = \lambda Q_0 - \Delta T$$  

where, since $\lambda Q_0$ is constant:

$$\frac{dz}{dt} = - \frac{\Delta T}{dt}$$

So the stock and flow equation becomes:

$$\frac{dz}{dt} = -\frac{z}{\tau}$$

---

+++

4\. Substitute $z = C \exp(-t/\tau)$.   To find the constant $C$ recognize
that at time $t=0$ $\Delta T = 0$, so $z(0) = C = \lambda Q_0$.   That means that:

$$z = C \exp(-t/\tau) = \lambda Q_0 \exp (-t/\tau) = \lambda Q_0 - \Delta T$$

and solving for $\Delta T$:

$$ \lambda Q_0 \left ( \exp (-t/\tau) - 1 \right ) = - \Delta T$$

and rearranging gives the answer:


$$ \Delta T = \lambda Q_0 \left (1 - \exp (-t/\tau) \right ) $$


