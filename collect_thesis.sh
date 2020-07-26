
##### Rectangular figure, 4.3
cp 'collect/ThesisRect' Thesis/PDRect.json
# states
cp 'simulations/ThesisRect/0.0_[0.5, 0.5]/finalstate.json' Thesis/RectStateLow_0.5.json
cp 'simulations/ThesisRect/0.0_[0.66000000000000003, 0.66000000000000003]/finalstate.json' Thesis/RectStateCrit_0.66.json
cp 'simulations/ThesisRect/0.0_[0.80000000000000004, 0.80000000000000004]/finalstate.json' Thesis/RectStateHigh_0.88.json
# curie
cp 'simulations/ThesisRectCurie/41414141_0.0/output' Thesis/RectCurie0.0.output
cp 'simulations/ThesisRectCurie/41414141_0.1/output' Thesis/RectCurie0.1.output
cp 'simulations/ThesisRectCurie/41414141_-0.1/output' Thesis/RectCurie-0.1.output
# hysteresis
cp 'simulations/ThesisRectHysteresis/42424242_-0.4_[0.28999999999999998, 0.28999999999999998]/output' Thesis/RectHyst0.29.output
cp 'simulations/ThesisRectHysteresis/42424242_-0.4_[0.47999999999999998, 0.47999999999999998]/output' Thesis/RectHyst0.48.output
cp 'simulations/ThesisRectHysteresis/42424242_-0.4_[0.85999999999999999, 0.85999999999999999]/output' Thesis/RectHyst0.86.output


##### Quench figure 4.6
cp 'collect/ThesisRectFlat' Thesis/PDRectflat.json
cp 'collect/ThesisRectCrit' Thesis/PDRectCrit.json
cp 'collect/ThesisRectOff' Thesis/PDRectOff.json
# TODO: Copy one run.json from all sims


##### Exponential figure 4.8
cp 'collect/ThesisExponential' Thesis/PDExp.json
# states
cp 'simulations/ThesisExponential/-0.41_[0.69999999999999996, 0.69999999999999996]/finalstate.json' 'Thesis/ExpStateCrit_-0.41_0.7.json'
cp 'simulations/ThesisExponential/-0.41_[0.5, 0.5]/finalstate.json' 'Thesis/ExpStateLow_-0.41_0.5.json'
cp 'simulations/ThesisExponential/-0.44_[0.80000000000000004, 0.80000000000000004]/finalstate.json' 'Thesis/ExpStateHigh_-0.44_0.8.json'
# curie
cp 'simulations/ThesisExponentialCurie/41414141_-0.3/output' Thesis/ExpCurie0.3.output
cp 'simulations/ThesisExponentialCurie/41414141_-0.4/output' Thesis/ExpCurie0.4.output
cp 'simulations/ThesisExponentialCurie/41414141_-0.5/output' Thesis/ExpCurie0.5.output
# hysteresis
cp 'simulations/ThesisExponentialHysteresis/-0.4_[0.40000000000000002, 0.40000000000000002]/output' Thesis/ExpHyst0.4.output
cp 'simulations/ThesisExponentialHysteresis/-0.4_[0.59999999999999998, 0.59999999999999998]/output' Thesis/ExpHyst0.6.output
cp 'simulations/ThesisExponentialHysteresis/-0.4_[0.80000000000000004, 0.80000000000000004]/output' Thesis/ExpHyst0.8.output
#cp 'simulations/ThesisExponentialHysteresis/-0.4_[0.59999999999999998, 0.59999999999999998]/output' Thesis/ExpHyst0.6.output
#cp 'simulations/ThesisExponentialHysteresis/-0.4_[0.69999999999999996, 0.69999999999999996]/output' Thesis/ExpHyst0.7.output
#cp 'simulations/ThesisExponentialHysteresis/-0.4_[0.80000000000000004, 0.80000000000000004]/output' Thesis/ExpHyst0.8.output


##### Cuto figure 4.11
cp 'collect/ThesisCuto' Thesis/PDCuto.json
# states
cp 'simulations/ThesisCuto/0.15_[0.40000000000000002, 0.40000000000000002]/finalstate.json' Thesis/CutoStateCrit_0.15_0.4.json
cp 'simulations/ThesisCuto/0.12_[0.33000000000000002, 0.33000000000000002]/finalstate.json' Thesis/CutoStateLow_0.12_0.33.json
cp 'simulations/ThesisCuto/0.18_[0.59999999999999998, 0.59999999999999998]/finalstate.json' Thesis/CutoStateHigh_0.18_0.6.json
# curie
cp 'simulations/ThesisCutoCurie/41414141_0.1/output' Thesis/CutoCurie0.1.output
cp 'simulations/ThesisCutoCurie/41414141_0.15/output' Thesis/CutoCurie0.15.output
cp 'simulations/ThesisCutoCurie/41414141_0.2/output' Thesis/CutoCurie0.2.output
# hysteresis
cp 'simulations/ThesisCutoHysteresis/0.1_[0.10000000000000001, 0.10000000000000001]/output' Thesis/CutoHyst0.1.output
cp 'simulations/ThesisCutoHysteresis/0.1_[0.29999999999999999, 0.29999999999999999]/output' Thesis/CutoHyst0.3.output
cp 'simulations/ThesisCutoHysteresis/0.1_[0.5, 0.5]/output' Thesis/CutoHyst0.5.output


##### Tail figure 4.10
cp 'collect/ThesisTail' Thesis/PDTail.json
# states
cp 'simulations/ThesisTail/-0.42_[0.73499999999999999, 0.73499999999999999]/finalstate.json' Thesis/TailStateCrit_-0.42_0.735.json
cp 'simulations/ThesisTail/-0.35_[0.5, 0.5]/finalstate.json' Thesis/TailStateLow_-0.35_0.5.json
cp 'simulations/ThesisTail/-0.45_[0.90000000000000002, 0.90000000000000002]/finalstate.json' Thesis/TailStateHigh_-0.45_0.9.json
# curie
cp 'simulations/ThesisTailCurie/41414141_-0.35/output' Thesis/CutoCurie-0.35.output
cp 'simulations/ThesisTailCurie/41414141_-0.4/output' Thesis/CutoCurie-0.4.output
cp 'simulations/ThesisTailCurie/41414141_-0.45/output' Thesis/CutoCurie-0.45.output
# hysteresis
cp 'simulations/ThesisTailHysteresis/-0.4_[0.5, 0.5]/output' Thesis/CutoHyst0.5.output
cp 'simulations/ThesisTailHysteresis/-0.4_[0.69999999999999996, 0.69999999999999996]/output' Thesis/CutoHyst0.7.output
cp 'simulations/ThesisTailHysteresis/-0.4_[0.90000000000000002, 0.90000000000000002]/output' Thesis/CutoHyst0.9.output



