import numpy as np
import matplotlib.pyplot as plt
import bilby
from gwpy.timeseries import TimeSeries
import paths

def smooth(y):
    box_pts = 30
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

time_of_event = 1264316116.4
detectors={'L1', 'V1'}
ifos = bilby.gw.detector.InterferometerList(detectors)

duration = 8.0
post_trigger_duration = 2.
analysis_start = time_of_event + post_trigger_duration - duration

for detector in ifos:
    analysis_data = TimeSeries.fetch_open_data(detector.name, analysis_start, analysis_start + duration, sample_rate=4096., cache=True)
    detector.set_strain_data_from_gwpy_timeseries(analysis_data)

plt.figure(figsize=(5,11))
plt.subplot(311)
plt.plot(ifos[0].frequency_array, smooth(np.sqrt(np.square(ifos[0].frequency_domain_strain))))
plt.plot(ifos[1].frequency_array, smooth(np.sqrt(np.square(ifos[1].frequency_domain_strain))))
plt.yscale('log')
plt.xscale('log')
plt.xlim(20,896)
plt.ylim(10e-26,10e-20)
plt.title("GR")
plt.legend(["left-handed", "right-handed"])
plt.subplot(312)
plt.plot(ifos[0].frequency_array, smooth(np.sqrt(np.square(ifos[0].frequency_domain_strain)))*np.exp(0.3*0.9*ifos[0].frequency_array/100))
plt.plot(ifos[1].frequency_array, smooth(np.sqrt(np.square(ifos[1].frequency_domain_strain)))*np.exp(-0.3*0.9*ifos[1].frequency_array/100))
plt.yscale('log')
plt.xscale('log')
plt.xlim(20,896)
plt.ylim(10e-26,10e-20)
plt.ylabel("$h(f)$")
plt.title("Birefringence (left-handed)")
plt.subplot(313)
plt.plot(ifos[0].frequency_array, smooth(np.sqrt(np.square(ifos[0].frequency_domain_strain)))*np.exp(-0.3*0.9*ifos[0].frequency_array/100))
plt.plot(ifos[1].frequency_array, smooth(np.sqrt(np.square(ifos[1].frequency_domain_strain)))*np.exp(0.3*0.9*ifos[1].frequency_array/100))
plt.yscale('log')
plt.xscale('log')
plt.xlim(20,896)
plt.ylim(10e-26,10e-20)
plt.xlabel("$f$")
plt.title("Birefringence (right-handed)")
plt.subplots_adjust(hspace=0.3)
plt.savefig(fname=paths.figures/"birefringence.png", bbox_inches="tight", dpi=300)