# following script is used to generate reweighted_kappa_samples.feather and reweighted_kappa_samples_without_GW200129.feather

import pandas as pd
import numpy as np
import jax
import jax.numpy as jnp
from flowMC.nfmodel.rqSpline import RQSpline
from flowMC.sampler.MALA import MALA
from flowMC.sampler.Sampler import Sampler
from flowMC.utils.PRNG_keys import initialize_rng_keys
import corner
import paths

events = [
"GW150914",
"GW151012",
"GW151226",
"GW170104",
"GW170608", #lal
"GW170729",
"GW170809",
"GW170814",
"GW170818",
"GW170823",
"GW190408_181802",
"GW190412",
"GW190413_052954",
"GW190413_134308",
"GW190421_213856",
"GW190503_185404",
"GW190512_180714",
"GW190513_205428",
"GW190517_055101",
"GW190519_153544",
"GW190521",
"GW190521_074359",
"GW190527_092055",
"GW190602_175927",
"GW190620_030421",
"GW190630_185205",
"GW190701_203306",
"GW190706_222641",
"GW190707_093326", #lal
"GW190708_232457",
"GW190719_215514",
"GW190720_000836", #lal
"GW190725_174728", #lal
"GW190727_060333",
"GW190728_064510", #lal
"GW190731_140936",
"GW190803_022701",
"GW190805_211137",
"GW190814", #lal
"GW190828_063405",
"GW190828_065509",
"GW190910_112807",
"GW190915_235702",
"GW190917_114630", #lal
"GW190924_021846", #lal
"GW190925_232845",
"GW190929_012149",
"GW190930_133541",
"GW191103_012549",
"GW191105_143521", #8kHz
"GW191109_010717",
"GW191127_050227",
"GW191129_134029",
"GW191204_171526",
"GW191215_223052",
"GW191216_213338",
"GW191222_033537",
"GW191230_180458",
"GW200112_155838",
"GW200128_022011",
"GW200129_065458", #V1 Glitch # comment out for reweighted_kappa_samples_without_GW200129.feather
"GW200202_154313",
"GW200208_130117",
"GW200209_085452",
"GW200216_220804",
"GW200219_094415",
"GW200224_222234",
"GW200225_060421",
"GW200302_015811",
"GW200311_115853",
"GW200316_215756",

# "GW170817", # BNS
# "GW190425", # BNS
# "GW190426_152155", # NSBH
# "GW200105_162426", # NSBH
# "GW200115_042309" # NSBH
]

result_dict = {}
result_DataFrame = pd.DataFrame()
result_DataFrame = pd.read_feather(paths.data/'samples_posterior_birefringence.feather')
for event in result_DataFrame['event'].unique():
    result_dict[event] = result_DataFrame[result_DataFrame.event == event]

kappa_array = jnp.stack([result_dict[event]['kappa'].values for event in events])

def normal_distribution(x, mu, sigma):
    return (1/(sigma*jnp.sqrt(2*jnp.pi)))*jnp.exp(-0.5*((x-mu)/sigma)**2)

pop_likelihood = lambda x: jnp.sum(jnp.log(jnp.mean(normal_distribution(kappa_array, x[0], x[1]),axis=1)))

n_dim = 2
n_chains = 1000

rng_key_set = initialize_rng_keys(n_chains, seed=42)

initial_position = jax.random.normal(rng_key_set[0], shape=(n_chains, n_dim)) * 1
initial_position = initial_position.at[:,1].set(jnp.abs(initial_position[:,1]))

model = RQSpline(n_dim, 3, [64, 64], 8)

step_size = 5e-2
local_sampler_caller = MALA(pop_likelihood, True, {"step_size": step_size})

nf_sampler = Sampler(n_dim,
                    rng_key_set,
                    local_sampler_caller,
                    pop_likelihood,
                    model,
                    n_local_steps = 300,
                    n_global_steps = 300,
                    n_epochs = 30,
                    learning_rate = 1e-2,
                    batch_size = 1000,
                    n_chains = n_chains,
                    use_global = True)

nf_sampler.sample(initial_position)
chains,log_prob,local_accs, global_accs = nf_sampler.get_sampler_state().values()

corner.corner(np.array(chains.reshape(-1,2))).savefig(paths.static/"corner_Gaussian_test.pdf")

np.savez("./samples_Gaussian.npz", chains=chains, log_prob=log_prob, local_accs=local_accs, global_accs=global_accs)
# np.savez("./samples_Gaussian_without_GW200129.npz", chains=chains, log_prob=log_prob, local_accs=local_accs, global_accs=global_accs)
