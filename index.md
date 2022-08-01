---
layout: default
title: "Constraining gravitational wave amplitude birefringence with GWTC-3"
---

<script type="text/javascript" async
    src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-MML-AM_CHTML">
</script>

**Thomas C.K. Ng** (The Chinese University of Hong Kong)

## Abstract

1. Motivation: Verify Chern-Simons Theory which suggest there is gravitational wave (GW) amplitude birefringence.
2. GW amplitude birefringence is a property of space that enhance one polarisation and suppress another during propagation of GW.
3. By performing parameter estimation on GW events in GWTC-3, the third LIGO-Virgo catalog, we can constrain the strength of birefringence.
4. What's new? Previous studies usually assume birefringence is frequency independent, which is a preliminary assumption. We include the frequency dependence, which allows us to further constrain the strength of birefringence.

## Main Poster

### GW Amplitude Birefringence

GW amplitude birefringence is a property of space suggested by some beyong-GR theories such as Chern-Simons Theory,
while GR suggest there is not.
With birefringence, amplitude of one GW polarisation is enhanced while the other is suppressed during propagation of the GW.
As a result, the observed amplitude ratio of the two polarsation under birefringence depends not only on $$\iota$$,
the angle between our line of sight and the orbital angular momentum of the binary black holes,
but also $$\kappa$$, the dimensionless opacity parameter that represent the strength of the birefringence,
while this ratio only depends on $$\iota$$ in GR.

We assume GWs are generated as GR described, and the effect of birefringence was took into account during the propagation.
During the propagation, the amlitude of two polarisation will be enhanced or suppressed as:

$$h_\mathrm{L,R}^{\mathrm{Biref}}=h_\mathrm{L,R}^{\mathrm{GR}}\times\exp\left(\pm\kappa\frac{d_C}{1\mathrm{ Gpc}}\frac{f}{100\mathrm{ Hz}}\right)\,,$$

where $$h_L$$ and $$h_R$$ are the amplitude of left and right polarizations of the GWs respectively, $$d_C$$ is the comoving distance to the merger,
and $$f$$ is the frequency component of the GWs.
Note that, previous studies usually ingore the frequency term.

To constrain $$\kappa$$, parameter estimations with data from the third LIGO-Virgo catalog, GWTC-3, was performed using Bilby,
a bayesian toolkit for GW analysis which is able to calculate posterior of GW parameters based on signals from
interferometer and priors of the parameters provided.

### Result on GW150914

With the frequency independent birefringence model (previous studies), the posteriors look different from the posteriors with GR.
This is because there is a degeneracy between $$\kappa$$ and $$\iota$$ without the frequency dependence,
so $$\iota$$ was less constrained compared to the PE with GR.
On the other hand, with the frequency dependent birefringence model, the posteriors look similar to the posteriors with GR.
This is because the degeneracy was broken by the frequency dependence. In this case, the posteriors can recover the PE with GR,
and the most probable value of $$\kappa$$ is close to $$0$$, which means the birefringence is weak or absent, and GR can be recovered.

### Preliminary Result on GWTC-3



## More about the author

<img src="{{site.baseurl}}/public/image/Thomas.jpg"/> 

Thomas Ng is a undergraduate student at The Chinese University of Hong Kong, who will graduate in summer 2023.
He is currently working at Flatiron Institute for this summer. [GitHub](https://github.com/thomasckng)
