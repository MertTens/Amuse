# Amuse
*Scripts for the Mind over Music project*

The goal for this project is to create a feedback loop where EEG signals influence a musical instrument that in turn influences a simulated [SWIM](http://wearcam.org/swim/) (SWIMulator). This feedback loop can be adjusted to optimize flow state, concentration, mindfulness, or any other psychological characteristic we can extract from the muse headset.

Goals for the project are as follows:
* (Done)Connect with the Muse
* (Done)Attain raw data from the Muse connection
* Process various psychological characteristics (flow state, concentration, etc.) from the raw EEG.
* Create a SWIMulator for virtual instruments.
* Set up a MIDI-controlled virtual synth that is parameterized by the EEG.
* Test simulated feedback system.
* Expand and diversify visualization systems.
* Expand and diversify sound synthesis methods.
* Investigate properties of final system(s) and present results.

# Scientific Background
## General EEG Analysis
[Paper](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3812603/)
* Alpha: `[8-13]`hz consciousness, quiet, or at rest. When thinking, blinking, or otherwise stimulated, α waves disappear.
* Beta: `[14-30]`hz particularly apparent when a person is thinking or receiving sensory stimulation.
* Theta: `[4-7]`hz Such waves are produced when people experience emotional pressure, interruptions of consciousness, or deep physical relaxation
* Gamma: `[31-50]`hz Recent studies have found that γ activity is related to selective attention. Other studies have also highlighted that this activity is related to cognition and perceptual activity..

## Live EEG Analysis Implementation
[Paper](https://www.notion.so/EEG-Generative-Ambient-Music-Flow-State-93657808b1bd430397646722199d66c8#6ae4c190672146d58b7d63a9859196d2)
* 512 Hz, 16-bit quantized input.
* Sub-50Hz frequencies were cut off.
* Every half second: Transform the last 512 samples to the frequency domain ⇒ record FFT.
    - This results in a 'window' that is 512 samples wide and is 'slid' 256 samples at a time.
