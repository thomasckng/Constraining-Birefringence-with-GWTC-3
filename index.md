---
layout: default
title: "Constraining gravitational wave amplitude birefringence with GWTC-3"
---

<script type="text/javascript" async
    src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-MML-AM_CHTML">
</script>

**Thomas C.K. Ng** (The Chinese University of Hong Kong)
**Maximiliano Isi** (Flatiron Institute)
**Kaze Wong** (Flatiron Institute)
**Will M. Farr** (Flatiron Institute, Stony Brook)

## Abstract

1. Motivation: constrain Chern-Simons gravity and other theories that predict gravitational-wave (GW) amplitude birefringence.
2. Amplitude birefringence consists of the enhancement of one GW polarisation over the other during propagation of the signal.
3. By performing parameter estimation on GW events in GWTC-3, the third LIGO-Virgo catalog, we can constrain the strength of birefringence.
4. What's new? Previous studies often assumed birefringence is frequency independent, which is a zeroth-order approximation; we include the predicted frequency dependence, allowing us to further constrain the strength of birefringence, and study more events than previous studies.

## Main Poster

### GW Amplitude Birefringence

GW amplitude birefringence is a property of space suggested by some theories beyond general relativity (GR) such as Chern-Simons gravity;
in contrast, GR predicts there is no birefringence.
With birefringence, amplitude of one GW polarisation is enhanced while the other is suppressed during propagation of the GW.
As a result, the observed amplitude ratio of the two polarisations under birefringence depends not only on the inclination $$\iota$$,
the angle between our line of sight and the orbital angular momentum of the binary black holes,
but also on $$\kappa$$, the dimensionless opacity parameter that represent the strength of the birefringence,
while this ratio only depends on $$\iota$$ in GR.
**[MI: this explanation is a bit backwards: you should first explain that the observed ratio of R vs L in GR only depends on the inclination (for a nonprecessing binary); then state that's no longer true if there is birefringence]**

**[MI: this paragraph starts abruptly; say something like "To implement this modification to the waveform, we assume that..."]**
We assume GWs are generated as GR described, and the effect of birefringence is taken into account during the propagation.
During the propagation, the amplitude of two polarisations will be enhanced or suppressed as given by:

$$h_\mathrm{L,R}^{\mathrm{Biref}}=h_\mathrm{L,R}^{\mathrm{GR}}\times\exp\left(\pm\kappa\frac{d_C}{1\mathrm{ Gpc}}\frac{f}{100\mathrm{ Hz}}\right)\,,$$

where $$h_L$$ and $$h_R$$ are the amplitude of left and right polarisations of the GWs respectively, $$d_C$$ is the comoving distance to the merger,
and $$f$$ is the frequency component of the GWs.
Note that, previous studies usually ingore the frequency term.
**[MI: you need to explain with the superscripts "GR" and "Biref" mean]**

To constrain $$\kappa$$, we perform parameter estimations with data from the third LIGO-Virgo catalog, GWTC-3 using Bilby, **[MI: link to Bilby url]**
a Bayesian toolkit for GW data analysis which is able to calculate posteriors of GW parameters based on data from
interferometer and priors of the parameters in question.

### Result on GW150914

<img src="{{site.baseurl}}/public/image/GW150914_3_parameters.png"/> 
<a href="{{site.baseurl}}/public/image/GW150914_9_parameters.png">More Parameters</a>

With the frequency independent birefringence model (previous studies **[MI: link to a previous study]**), the posterior **[MI: for which parameters]** looks different from the posteriors with GR.
This is because, for a nonprecessing system, there is a degeneracy between $$\kappa$$ and $$\iota$$ without the frequency dependence,
so $$\iota$$ was less constrained compared to the PE with GR.
**[MI: not only it was less constrained: there are some specific degeneracies between $$\kappa$$ and $$\iota$$---can you explain them?]**
On the other hand, with the frequency dependent birefringence model, the posteriors look similar to the posteriors with GR.
This is because the degeneracy was broken by the frequency dependence. In this case, the posteriors can recover the PE with GR,
and the most probable value of $$\kappa$$ is close to $$0$$, which means the birefringence is weak or absent, and GR can be recovered.
**[MI: the most important thing to highlight is that the constraint on $$\kappa$$ is very tight]**

### Preliminary Result on GWTC-3



## More about the author

<img src="{{site.baseurl}}/public/image/Thomas.jpg"/> 

Thomas Ng is an undergraduate student at The Chinese University of Hong Kong, who will graduate in summer 2023.
He is currently working at Flatiron Institute for this summer. [GitHub](https://github.com/thomasckng)
