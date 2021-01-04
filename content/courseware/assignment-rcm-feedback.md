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

# Assignment: Feedbacks in the Radiative-Convective Model

This notebook is part of [The Climate Laboratory](https://brian-rose.github.io/ClimateLaboratoryBook) by [Brian E. J. Rose](http://www.atmos.albany.edu/facstaff/brose/index.html), University at Albany.

+++

## Learning goals

Students completing this assignment will gain the following skills and concepts:

- Familiarity with setting up and running a single-column Radiative-Convective Model using climlab
- Familiarity with plotting and interpreting vertical air temperature data on meteorological Skew-T charts
- Use of climlab to perform controlled parameter-sensitivity experiments
- Understanding of the lapse rate feedback concept
- Calculation of radiative forcing and climate feedback parameters

+++

## Question 1

Here you look at the effects of doubling CO$_2$ in the single-column Radiative-Convective model. 

*This exercise just repeats what we did in the lecture notes. You want to ensure that you can reproduce the same results before starting the next question, because you will need these results below.*

Following the lecture notes on climate sensitivity, do the following:

- set up a single-column radiative-convective model with specific humidity taken from the CESM control simulation
- Run this control model out to equilibrium
- Using a clone of the control model, calculate the stratosphere-adjusted radiative forcing $\Delta R$.
- Using another model clone, timestep the model out to equilibrium **with fixed specific humidity**
- Calculate the no-feedback Equilibrium Climate Sensitivity (ECS)
- Also calculate the no-feedback climate response parameter $\lambda_0$

Verify and show that you get the same results as we did in the lecture notes.

```{code-cell} ipython3

```

## Question 2: combined lapse rate and water vapor feedback in the RCM

### Instructions

A typical, expected feature of global warming is that the **upper troposphere warms more than the surface**. (Later we will see that this does occur in the CESM simulations).

This feature is **not represented in our radiative-convective model**, which is forced to a single prescribed lapse rate due to our convective adjustment.

Here you will suppose that other physical processes modify this lapse rate as the climate warms. 

**Repeat the RCM global warming calculation, but implement two different feedbacks:**

- a water vapor feedback using **fixed relative humidity**
- a **lapse rate feedback** using this formula:

$$ \Gamma = \Gamma_{ref} - (0.3 \text{ km}) \Delta T_s $$

where $\Gamma_{ref}$ is the critical lapse rate you used in your control model, probably 6.5 K / km, and $\Delta T_s$ is the **current value of the surface warming relative to the control** in units of K. 

So, for example if the model has warmed by 1 K at the surface, then our parameterization says that the critical lapse rate should be 6.5 - 0.3 = 6.2 K / km.

Follow the example in the lecture notes where we implemented the fixed relative humidity. In addition to adjusting the `specific_humidity` at each timestep, you should also change the attribute

```
adj_lapse_rate
```
of the convection process at each timestep.

For example, if you have a model called `mymodel` that contains a `ConvectiveAdjustment` process called `Convection`:
```
mymodel.subprocess['Convection'].adj_lapse_rate = newvalue
```
where `newvalue` is a number in K / km.

### Specific questions:

1. Make a nice skew-T plot that shows three temperature profiles:
    - RCM control
    - RCM, equilibrium after doubling CO$_2$ without feedback
    - RCM, equilibrium after doubling CO$_2$ with combined water vapor and lapse rate feedback
2. Based on your plot, where in the column do you find the greatest warming?
3. Calculate the ECS of the new version of the model with combined water vapor and lapse rate feedback
4. Is this sensitivity larger or smaller than the "no feedback" ECS? Is it larger or smaller than the ECS with water vapor feedback alone (which we calculated in the lecture notes)?
5. Calculate the combined feedback parameter for (water vapor plus lapse rate).
6. Compare this result to the IPCC figure with feedback results from comprehensive models in our lecture notes (labeled "WV+LR"). Do you find a similar number?
7. Would you describe the **lapse rate feedback** as positive or negative?


```{code-cell} ipython3

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
