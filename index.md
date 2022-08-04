---
layout: default
title: "Constraining gravitational wave amplitude birefringence with GWTC-3"
---

<script type="text/javascript" async
    src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-MML-AM_CHTML">
</script>

**Thomas C.K. Ng** (The Chinese University of Hong Kong),
**Maximiliano Isi** (Flatiron Institute),
**Kaze Wong** (Flatiron Institute),
**Will M. Farr** (Flatiron Institute, Stony Brook)

## Abstract

1. Motivation: **constrain Chern-Simons gravity** and other theories that predict gravitational-wave (GW) amplitude birefringence.
2. **Amplitude birefringence** consists of the **enhancement of one GW polarisation over the other** during propagation of the signal.
3. By performing **parameter estimation** on GW events in GWTC-3, the third LIGO-Virgo catalog, we can **constrain the strength of birefringence**.
4. What's new? **Previous studies** often assumed birefringence is **frequency independent**, which is a zeroth-order approximation; **we include** the predicted **frequency dependence**, allowing us to further constrain the strength of birefringence, and we study more events than previous studies.

## Main Poster (~3 mins read)

### GW Amplitude Birefringence

GW amplitude birefringence is a property of space suggested by some theories beyond general relativity (GR) such as Chern-Simons gravity;
in contrast, **GR predicts there is no birefringence**.

**According to GR**, the observed **amplitude ratio** of the two circular polarisations **depends only on the inclination $$\iota$$** for a nonprecessing binary,
where $$\iota$$ is the angle between our line of sight and the orbital angular momentum of the binary.
**With birefringence**, the amplitude of one GW polarisation is enhanced while the other is suppressed during propagation of the GW.
As a result, the observed amplitude ratio under birefringence **depends not only on $$\iota$$, but also on $$\kappa$$**,
the dimensionless opacity parameter that encodes the strength of birefringence in a frequency-dependent way.

### Implementation with Frequency Dependence

<style>
.video-wrapper {
  position: relative;
  width: 100%;
  height: 0;
  padding-bottom: 56.25%;
}
.video-wrapper iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border: 0;
}
</style>

<div class="video-wrapper">
    <iframe src="{{site.baseurl}}/public/video/birefringence.mp4" allowfullscreen></iframe>
</div>

To implement this modification to the waveform, **we assume that GWs are generated as GR described**,
and the effect of **birefringence** is taken into account **during the propagation**.
During the propagation, the amplitude of two polarisations will be enhanced or suppressed as given by:

$$h_\mathrm{L,R}^{\mathrm{Biref}}=h_\mathrm{L,R}^{\mathrm{GR}}\times\exp\left(\pm\kappa\frac{d_C}{1\mathrm{ Gpc}}\frac{f}{100\mathrm{ Hz}}\right)\,$$

where $$h_L$$ and $$h_R$$ are the Fourier amplitudes of the left and right polarisations of the GW respectively, $$d_C$$ is the comoving distance to the merger,
and $$f$$ is the Fourier frequency. This equation describes the effect of birefringence after GWs are generated following GR,
which is also shown in the video. The amplitude of one polarisation is enhanced exponentially as the GW travels **longer distance**,
and there is **larger enhancement for the higher frequency** part of the GW, vice versa for the other polarisation.
Note that some previous studies have ignored the frequency dependence.

To constrain $$\kappa$$, we perform **parameter estimation** with data from the third LIGO-Virgo catalog,
**GWTC-3**, using <a href="https://lscsoft.docs.ligo.org/bilby/">Bilby</a>,
a Bayesian toolkit for GW data analysis which is able to calculate posteriors of GW parameters based on interferometer data
and priors for the parameters in question.

### Result for GW150914

<img src="{{site.baseurl}}/public/image/GW150914_3_parameters.png"/> 
<a href="{{site.baseurl}}/public/image/GW150914_9_parameters.png">more parameters</a>

With the frequency independent birefringence model (<a href="https://arxiv.org/abs/2101.11153">previous studies</a>),
the **posterior for $$\cos\iota$$ looks different** from the posterior assuming GR.
This is because, for a nonprecessing system, there is a **degeneracy between $$\kappa$$ and $$\iota$$** if the frequency dependence is not included.
To reconstruct the amplitude ratio from the interferometer data, a more face-on $\iota$ can pair with a positive $\kappa$,
or a more face-off $\iota$ with a negative $\kappa$. As a result, many pairs of $\iota$ and $\kappa$ can be plausible with the frequency independence.
On the other hand, with the frequency-dependent birefringence model, the posterior looks similar to the GR posterior.
This is because the degeneracy was broken by the frequency dependence, as the effect of the birefringence will be different from the one of changing $\iota$.
In this case, the posteriors can recover the GR distributions for the binary parameters,
and **the most probable value of $$\kappa$$ is close to $$0$$**, which means the birefringence is weak or absent, and **GR can be recovered**.

### Preliminary Result on GWTC-3

We are performing parameter estimations on $$76$$ events in GWTC-3 to further constrain $$\kappa$$.
The preliminary results show $$\kappa$$ can be **well constrained around $$0$$**,
which can then be used to constrain multiple beyond-GR theories.
We are currently finalizing the parameter estimation results to make sure all estimations on each event are correctly preformed.

## More about the author

<img src="{{site.baseurl}}/public/image/Thomas.jpg"/> 

Thomas Ng is an undergraduate student at The Chinese University of Hong Kong, who will graduate in summer 2023.
He is currently working at Flatiron Institute for this summer. [GitHub](https://github.com/thomasckng)
