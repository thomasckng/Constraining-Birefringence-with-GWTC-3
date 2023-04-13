import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy
import paths

rng = np.random.default_rng(12345)

sns.set_theme(palette='colorblind', font_scale=1.5)

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"]
})

def normal_distribution(x, mu, sigma):
    return (1/(sigma*np.sqrt(2*np.pi)))*np.exp(-0.5*((x-mu)/sigma)**2)

# Result with GW200129
result_dict = {}
result_DataFrame = pd.read_feather(paths.data/"samples_posterior_birefringence.feather")
for event in result_DataFrame['event'].unique():
    result_dict[event] = result_DataFrame[result_DataFrame.event == event]

samples_original = np.load(paths.data/"samples_Gaussian.npz")["chains"]
samples_all = samples_original.reshape(-1, 2)

df_Gaussian_samples_all = pd.DataFrame()
df_Gaussian_samples_all['mu'] = samples_all[:,0]
df_Gaussian_samples_all['sigma'] = samples_all[:,1]

samples_reweighted = []
for _ in range(5000):
    Gaussian = np.full(shape=(len(result_DataFrame), 2), fill_value=df_Gaussian_samples_all.sample(1, random_state=rng))
    weight = normal_distribution(result_DataFrame['kappa'], Gaussian[:,0], Gaussian[:,1])
    weight /= weight.sum()
    samples_reweighted.append(rng.choice(a=np.array(result_DataFrame['kappa']), size=1, p=weight))

events = result_DataFrame['event'].unique()
kernels = [scipy.stats.gaussian_kde(result_dict[event]['kappa']) for event in events]
kappa = np.linspace(-.1, .1, 1000)
ll = [np.sum([np.log(ker(k)) for ker in kernels]) for k in kappa]
ll = ll - np.max(ll)
likelihood = np.exp(ll)
likelihood = likelihood / np.trapz(likelihood, x=kappa)

fs = (6.807804068078041, 4.207454302822033)
fig, ax = plt.subplots(1, figsize=fs)
plt.axvline(0, color='k', lw=2, ls='--')
sns.kdeplot(np.array(samples_reweighted).reshape(-1), label="generic", color=sns.color_palette()[3])
# plt.axvline(np.percentile(a=np.array(samples_reweighted).reshape(-1),q=5), color=sns.color_palette()[3], linestyle=':')
# plt.axvline(np.percentile(a=np.array(samples_reweighted).reshape(-1),q=95), color=sns.color_palette()[3], linestyle=':')
plt.plot(kappa,likelihood, label="restricted", color=sns.color_palette()[0])
yl = plt.gca().get_ylim()
plt.fill_between(kappa, likelihood, color=sns.color_palette()[0], alpha=0.2)
plt.ylim(yl)
# plt.axvline(np.interp(0.05,[np.trapz(likelihood[0:i],kappa[0:i]) for i in range(1000)],kappa), color=sns.color_palette()[0], linestyle=':')
# plt.axvline(np.interp(0.95,[np.trapz(likelihood[0:i],kappa[0:i]) for i in range(1000)],kappa), color=sns.color_palette()[0], linestyle=':')

# Result without GW200129
result_dict = {}
result_DataFrame = pd.read_feather(paths.data/"samples_posterior_birefringence.feather")
result_DataFrame = result_DataFrame[result_DataFrame.event != 'GW200129_065458']
for event in result_DataFrame['event'].unique():
    result_dict[event] = result_DataFrame[result_DataFrame.event == event]

samples_original = np.load(paths.data/"samples_Gaussian_without_GW200129.npz")["chains"]
samples_all = samples_original.reshape(-1, 2)

df_Gaussian_samples_all = pd.DataFrame()
df_Gaussian_samples_all['mu'] = samples_all[:,0]
df_Gaussian_samples_all['sigma'] = samples_all[:,1]

samples_reweighted = []
for _ in range(5000):
    Gaussian = np.full(shape=(len(result_DataFrame), 2), fill_value=df_Gaussian_samples_all.sample(1, random_state=rng))
    weight = normal_distribution(result_DataFrame['kappa'], Gaussian[:,0], Gaussian[:,1])
    weight /= weight.sum()
    samples_reweighted.append(rng.choice(a=np.array(result_DataFrame['kappa']), size=1, p=weight))

events = result_DataFrame['event'].unique()
kernels = [scipy.stats.gaussian_kde(result_dict[event]['kappa']) for event in events]
kappa = np.linspace(-.1, .1, 1000)
ll = [np.sum([np.log(ker(k)) for ker in kernels]) for k in kappa]
ll = ll - np.max(ll)
likelihood = np.exp(ll)
likelihood = likelihood / np.trapz(likelihood, x=kappa)

sns.kdeplot(np.array(samples_reweighted).reshape(-1), color=sns.color_palette()[3], linestyle='--')
# plt.axvline(np.percentile(a=np.array(samples_reweighted).reshape(-1),q=5), color=sns.color_palette()[3], linestyle='-.')
# plt.axvline(np.percentile(a=np.array(samples_reweighted).reshape(-1),q=95), color=sns.color_palette()[3], linestyle='-.')
plt.plot(kappa,likelihood, color=sns.color_palette()[0], linestyle='--')
# plt.axvline(np.interp(0.05,[np.trapz(likelihood[0:i],kappa[0:i]) for i in range(1000)],kappa), color=sns.color_palette()[0], linestyle='-.')
# plt.axvline(np.interp(0.95,[np.trapz(likelihood[0:i],kappa[0:i]) for i in range(1000)],kappa), color=sns.color_palette()[0], linestyle='-.')

plt.xlim(-.15, .15)
plt.ylabel("$p(\kappa|\{d\})$")
plt.xlabel(r"$\kappa$ ($\mathrm{Gpc}^{-1}$)")
plt.legend()

plt.savefig(fname=paths.figures/"posterior_kappa.pdf", bbox_inches="tight", dpi=300)
