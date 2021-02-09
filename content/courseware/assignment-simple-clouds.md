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

(nb:simple-clouds)=
# Assignment: Clouds in the Leaky Greenhouse Model

This notebook is part of [The Climate Laboratory](https://brian-rose.github.io/ClimateLaboratoryBook) by [Brian E. J. Rose](http://www.atmos.albany.edu/facstaff/brose/index.html), University at Albany.

+++

## Learning goals

Students completing this assignment will gain the following skills and concepts:

- Continued practice working with the Jupyter notebook
- Familiarity with the toy "leaky greenhouse" model
- Conceptual understanding of the role of clouds in the planetary energy budget

+++

## Instructions

***This assignment requires some mathematics. You can present your work in this notebook, on hand-written paper, or a combination. Just make sure you communicate clearly which answers belong to which question.***

For answers presented in the notebook, follow the usual procedures to ensure that your code is well commented and runs clearly without errors (see previous assignment instructions).

+++

## Introduction

Consider the two-layer "leaky greenhouse" (or grey radiation) model from [these lecture notes](https://brian-rose.github.io/ClimateLaboratoryBook/courseware/elementary-greenhouse.html).

Here you will use this model to investigate the **radiative effects of clouds**.

Clouds simultaneously **reflect shortwave radiation** and **absorb longwave radiation**. These two effects often oppose each other in nature, and which one is stronger depends (among other things) on whether the clouds are **low** or **high** (i.e. in layer 0 or layer 1).

For this question we will suppose (as we did in the lecture notes) that there is **no absorption of shortwave radiation** in the atmosphere.

+++

## Question 1

Suppose a cloud reflects a fraction $\alpha_c$ of the shortwave beam incoming from above. $\alpha_c$ is a number between 0 and 1. Provide a coherent argument (in words, sketches, and/or equations) for why the **shortwave** effects cloud should alway be a **cooling** on the surface. Is this cooling effect different if the cloud is low or high? Explain.

```{code-cell} ipython3

```

## Question 2

Because the liquid water droplets in a cloud are effective absorbers of longwave radiation, a cloud will **increase the longwave absorptivity / emissivity** of the layer in which it resides. 

We can represent this in the two-layer atmosphere by letting the absorptivity of a cloudy layer be $\epsilon + \epsilon_c$, where $\epsilon_c$ is an additional absorptivity due to the cloud. Derive a formula (i.e. an algebraic expression) for the OLR in terms of the temperatures $T_s, T_0, T_1$ and the emissivities $\epsilon, \epsilon_c$ for two different cases:

- a low cloud (the additional $\epsilon_c$ is in layer 0)
- a high cloud (the additional $\epsilon_c$ is in layer 1)

```{code-cell} ipython3

```

## Question 3

Now use the tuned numerical values we used in class:

- $T_s = 288$ K
- $T_0 = 275$ K
- $T_1 = 230$ K
- $\epsilon = 0.586$

and take $\epsilon_c = 0.2$

(a) Repeat the following for both a high cloud and a low cloud:

- Calculate the **difference in OLR** due to the presence of the cloud, compared to the case with no cloud. 
- Does this represent a warming or cooling effect?

(b) Which one has a larger effect, the low cloud or the high cloud?

```{code-cell} ipython3

```

## Question 4

Based on your results in questions 1-3, which do you think is more likely to produce a **net warming effect** on the climate: a low cloud or a high cloud? Give an explanation in words.

```{code-cell} ipython3

```

## Question 5

How would your answer change if the atmosphere were **isothermal**, i.e. $T_s = T_0 = T_1$?

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
