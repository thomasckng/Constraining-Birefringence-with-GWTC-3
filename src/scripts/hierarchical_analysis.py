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

result_dict = {}
result_DataFrame = pd.DataFrame()
result_DataFrame = pd.read_feather(paths.data/'samples_posterior_birefringence.feather')
events = result_DataFrame['event'].unique()
# events = events[events!='GW200129_065458'] # use this for reweighted_kappa_samples_without_GW200129.feather

for event in events:
    result_dict[event] = result_DataFrame[result_DataFrame.event == event]

kappa_array = jnp.stack([result_dict[event]['kappa'].values for event in events])

def normal_distribution(x, mu, sigma):
    return (1/(sigma*jnp.sqrt(2*jnp.pi)))*jnp.exp(-0.5*((x-mu)/sigma)**2)

Nsamp=len(kappa_array[0])
bws = np.std(kappa_array, axis=0)/Nsamp**(1.0/5.0)
pop_likelihood = lambda x: jnp.sum(jnp.log(jnp.mean(normal_distribution(kappa_array, x[0], jnp.sqrt(jnp.square(x[1]) + bws)),axis=1))) + jax.lax.cond(x[1]>=0, lambda: .0, lambda: -jnp.inf)

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
